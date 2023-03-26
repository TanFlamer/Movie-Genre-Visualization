# sum(grepl("Adventure", action$genre, fixed = TRUE))

# rm(list = ls())

# cat("\014")

# Genre vs rating/ Rating vs genre

order(x, decreasing =TRUE)

apply(Genre_1[3:7], 1, order, decreasing = TRUE)

system.time()

data.frame(test, t(sapply(test$list, unlist))) # List to columns

get("Genre_1")

lapply(temp, toString)

t(sapply(combn(GenreList, 1, simplify = FALSE), count_combination))

levels <- levels(as.factor(Movies$certificate))

process_matrix <- function(matrix){
  list_of_lists <- data.frame(matrix(ncol = 0, nrow = nrow(matrix)))
  list_of_lists$original <- matrix_to_list(matrix)
  
  row_total <- rowSums(matrix)
  row_percentage <- round(sweep(matrix, 1, row_total, '/') * 100, 2)
  row_percentage[is.nan(row_percentage)] <- 0
  list_of_lists$row <- matrix_to_list(row_percentage)
  
  column_total <- colSums(matrix)
  column_percentage <- round(sweep(matrix, 2, column_total, '/') * 100, 2)
  list_of_lists$column <- matrix_to_list(column_percentage)
  
  genre_order <- apply(matrix, 1, order, decreasing = TRUE)
  list_of_lists$order <- as.list(data.frame(genre_order))
  
  return (list_of_lists)
}
