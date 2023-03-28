# Import library
library(shiny)
library(shinyjs)
library(plotly)
library(stringr)
library(dplyr)
library(english)
library(reshape)

# Load functions
source("preprocess.R", local = TRUE)
source("process.R", local = TRUE)
source("plot.R", local = TRUE)

# Load movies and genre
list2env(setNames(load_movies("archive.zip"), c("Movies", "genres")), envir = globalenv())

# Process movie data
Rating <- compare_data(FALSE, factors = addNA(cut(Movies$rating, breaks = seq(0, 10, 2))), func = rename_strings)
rating <- Rating$levels

Runtime <- compare_data(FALSE, factors = addNA(cut(Movies$runtime, breaks = c(seq(0, 240, 30), Inf))), func = rename_strings)
runtime <- Runtime$levels

Votes <- compare_data(FALSE, factors = addNA(cut(Movies$votes, breaks = 10^(0:7))), func = convert_exponent)
votes <- Votes$levels

Decade <- compare_data(FALSE, factors = cut(Movies$year, breaks = c(-Inf, seq(1910, 2030, 10)), right = FALSE), func = convert_exponent)
decade <- Decade$levels

Certificate <- compare_data(FALSE, factors = factor(Movies$certificate, unique(Movies$certificate)))
certificate <- Certificate$levels

# Process genre data
Genre1 <- compare_data(TRUE, x = 1)
Genre2 <- compare_data(TRUE, x = 2)
Genre3 <- compare_data(TRUE, x = 3)

css <- "
.nowrap {
  white-space: nowrap;
}"

# Define UI
ui = fluidPage(
  tabsetPanel(
    tabPanel("Plot", fluid = TRUE,
             titlePanel("Movie Plot"),
             
             column(12, fluidRow(column(6, selectInput(inputId = "plot",
                                                       label = "Plot Type",
                                                       choices = list(NumberofMovies = "year",
                                                                      RatingofMovies = "rating",
                                                                      RuntimeofMovies = "runtime",
                                                                      VotesofMovies = "votes"))),
                                 
                                 column(6, sliderInput(inputId = "year",
                                                       label = "Year Range",
                                                       min = min(Movies$year),
                                                       max = max(Movies$year),
                                                       value = c(min(Movies$year),
                                                                 max(Movies$year)),
                                                       sep = ""))
             )),
             
             column(12, fluidRow(column(4, selectInput(inputId = "genre1",
                                                       label = "First Genre",
                                                       choices = c("-", genres))),
                                 
                                 column(4, selectInput(inputId = "genre2",
                                                       label = "Second Genre",
                                                       choices = c("-", genres))),
                                 
                                 column(4, selectInput(inputId = "genre3",
                                                       label = "Third Genre",
                                                       choices = c("-", genres)))
             )),
             
             column(12, submitButton(text = "Create plot"), offset = 5),
             
             plotOutput(outputId = "movieplot")
    ),
    tabPanel("Table", fluid = TRUE,
             titlePanel("Movie Table"),
             
             column(12, fluidRow(column(4, selectInput(inputId = "table",
                                                       label = "Table",
                                                       choices = c("Certificate", "Decade",
                                                                   "Genre1", "Genre2", "Genre3",
                                                                   "Rating", "Runtime", "Votes"))),
                                 
                                 column(4, selectInput(inputId = "column",
                                                       label = "Column",
                                                       choices = c("rating", "genres", "runtime",
                                                                   "votes", "decade", "certificate"))),
                                 
                                 column(4, selectInput(inputId = "type",
                                                       label = "Type",
                                                       choices = c("total", "original", "row",
                                                                   "column", "order")))
             )),
             
             column(12, submitButton(text = "Create table"), offset = 5),
             
             tags$head(tags$style("#table  {white-space: nowrap;  }")),
             column(12, dataTableOutput('table'))
    ),
    tabPanel("Chart", fluid = TRUE,
             titlePanel("Movie Chart"),
             
             column(12, fluidRow(column(6, selectInput(inputId = "table2",
                                                       label = "Table",
                                                       choices = c("Certificate", "Decade",
                                                                   "Genre1", "Genre2", "Genre3",
                                                                   "Rating", "Runtime", "Votes"))),
                                 
                                 column(6, selectInput(inputId = "column2",
                                                       label = "Column",
                                                       choices = c("rating", "genres", "runtime",
                                                                   "votes", "decade", "certificate")))
             )),
             
             column(12, submitButton(text = "Create chart"), offset = 5),
             
             plotOutput(outputId = "moviechart")
    )
  )
)

# Define server logic
server <- function(input, output){
  output$movieplot <- renderPlot({
    movie_filter <- filter_movies(c(input$genre1, input$genre2, input$genre3))
    filtered_movies <- movie_plot(input$plot, movie_filter)
    names(filtered_movies) <- c("year", "value")
    filtered_movies %>%
      ggplot(aes(x=year, y=value))+
      geom_line()+
      scale_x_continuous(limits = input$year)+
      theme_minimal()
  })
  
  output$table <- renderDataTable(list_to_table(input$table, input$column, input$type))
  
  output$moviechart <- renderPlot({
    long_frame <- list_to_chart(input$table2, input$column2)
    ggplot(long_frame, aes(fill=variable, y=value, x=levels)) + 
      geom_bar(position="stack", stat="identity")
  })
}

# Run the app
shinyApp(ui = ui, server = server)
