# Load shiny library
library(shiny)
library(tidyverse)
library(babynames)

# Define UI
ui <- fluidPage(
  titlePanel("Shiny App"),
  
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
  
  column(12, dataTableOutput('table'))
)

# Define server logic
server <- function(input, output){
  output$table <- renderDataTable(list_to_table(input$table, input$column, input$type))
}

# Run the app
shinyApp(ui = ui, server = server, options = list(scrollX = TRUE))