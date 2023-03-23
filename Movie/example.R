# Load shiny library
library(shiny)
library(tidyverse)
library(babynames)

# Define UI
ui <- fluidPage(
  titlePanel("Shiny App"),
  
  column(12, fluidRow(column(6, selectInput(inputId = "type",
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
                                           choices = c("All", GenreList))),
                     
                     column(4, selectInput(inputId = "genre2",
                                           label = "Second Genre",
                                           choices = c("All", GenreList))),
                     
                     column(4, selectInput(inputId = "genre3",
                                           label = "Third Genre",
                                           choices = c("All", GenreList)))
  )),
  
  column(12, submitButton(text = "Create plot"), offset = 5),
  
  plotOutput(outputId = "nameplot")
)

# Define server logic
server <- function(input, output){
  output$nameplot <- renderPlot({
    movie_filter <- filter_movie(input$genre1, input$genre2, input$genre3)
    filtered_movies <- movie_plot(input$type, movie_filter)
    names(filtered_movies) <- c("x_axis", "y_axis")
    filtered_movies %>%
      ggplot(aes(x=x_axis, y=y_axis))+
      geom_line()+
      scale_x_continuous(limits = input$year)+
      theme_minimal()
  })
}

# Run the app
shinyApp(ui = ui, server = server)