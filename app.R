# Import library
library(shiny)
library(plotly)
library(ggplot2)
library(stringr)
library(dplyr)
library(english)
library(reshape)

# Load functions
source("preprocessing.R", local = TRUE)
source("transformation.R", local = TRUE)
source("visualization.R", local = TRUE)

# Load data into app
source("data.R", local = TRUE)

# Define UI
ui = fluidPage(
  tabsetPanel(
    tabPanel("Plot", fluid = TRUE,
             titlePanel("Movie Plot"),
             
             column(12, fluidRow(column(6, selectInput(inputId = "plot",
                                                       label = "Plot Type",
                                                       choices = list(Count = "year",
                                                                      Rating = "rating",
                                                                      Runtime = "runtime",
                                                                      Votes = "votes"))),
                                 
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
             
             column(12, fluidRow(column(4, selectInput(inputId = "table2",
                                                       label = "Table",
                                                       choices = c("Certificate", "Decade",
                                                                   "Genre1", "Genre2", "Genre3",
                                                                   "Rating", "Runtime", "Votes"))),
                                 
                                 column(4, selectInput(inputId = "column2",
                                                       label = "Column",
                                                       choices = c("rating", "genres", "runtime",
                                                                   "votes", "decade", "certificate"))),
                                 
                                 column(4, selectInput(inputId = "position",
                                                       label = "Position",
                                                       choices = c("fill", "stack", "dodge")))
             )),
             
             column(12, submitButton(text = "Create chart"), offset = 5),
             
             plotOutput(outputId = "moviechart")
    )
  )
)

# Define server logic
server <- function(input, output){
  # Movie Plot
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
  
  # Movie Table
  output$table <- renderDataTable(list_to_table(input$table, input$column, input$type))
  
  # Movie Chart
  output$moviechart <- renderPlot({
    long_frame <- list_to_chart(input$table2, input$column2)
    ggplot(long_frame, aes(fill=variable, y=value, x=factors)) + 
      geom_bar(position=input$position, stat="identity")
  })
}

# Run the app
shinyApp(ui = ui, server = server)
