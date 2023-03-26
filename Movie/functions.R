assign_certificates <- function(row){
  if (row == "" | row == "Not Rated" | row == "Unrated")
    return ("Unrated")
  else if (row == "G" | row == "R" | row == "PG" | row == "PG-13" | 
           row == "TV-14" | row == "TV-MA" | row == "TV-PG" | row == "Passed" |
           row == "Unrated" | row == "Approved")
    return (row)
  else
    return ("Other")
}

filter_genre <- function(genre, movie_list = Movies){
  if(genre == "All")
    return (rep(c(TRUE), times = nrow(movie_list)))
  else{
    return (movie_list$genre1 == genre | 
              (!is.na(movie_list$genre2) & movie_list$genre2 == genre) | 
              (!is.na(movie_list$genre3) & movie_list$genre3 == genre))
  }
}

filter_movie <- function(genre1, genre2, genre3){
  return (filter_genre(genre1) & filter_genre(genre2) & filter_genre(genre3))
}

movie_plot <- function(type, movie_filter){
  filtered_movies <- Movies[movie_filter,]
  if (nrow(filtered_movies) == 0)
    return (data.frame(matrix(ncol = 2, nrow = 0)))
  else{
    filtered_row = filtered_movies[,type]
    year_list = list(filtered_movies$year)
    if (type == "year")
      return (aggregate(filtered_row, year_list, length))
    else
      return (aggregate(filtered_row, year_list, mean, na.rm = TRUE))
  }
}

list_to_table <- function(table, column, type){
  final_table <- get(table)[,1:3]
  column_list <- get(table)[,column]
  column_matrix <- t(sapply(column_list, unlist))
  process_order(column_matrix)
  if (type == "original")
    return (data.frame(final_table, column_matrix))
  else if (type == "row")
    return (data.frame(final_table, process_row(column_matrix)))
  else if (type == "column")
    return (data.frame(final_table, process_column(column_matrix)))
  else
    return (data.frame(final_table, process_order(column_matrix)))
}

process_row <- function(matrix){
  row_total <- rowSums(matrix)
  row_percentage <- round(sweep(matrix, 1, row_total, '/') * 100, 2)
  row_percentage[is.nan(row_percentage)] <- 0
  return (row_percentage)
}

process_column <- function(matrix){
  column_total <- colSums(matrix)
  column_percentage <- round(sweep(matrix, 2, column_total, '/') * 100, 2)
  return (column_percentage)
}

process_order <- function(matrix){
  row_order <- apply(matrix, 1, order, decreasing = TRUE)
  row_labels <- apply(row_order, 1, function(x) ratings[x])
  row_sorted <- t(apply(process_row(matrix), 1, sort, decreasing = TRUE))
  matrix_order <- matrix(1:(2*ncol(matrix)), nrow = ncol(matrix), ncol = 2)
  column_order <- c(t(matrix_order))
  final_table <- cbind(row_labels, row_sorted)[,column_order]
  return (final_table)
}

list_to_frame <- function(column){
  matrix <- t(sapply(column, unlist))
  return (data.frame(matrix))
}
