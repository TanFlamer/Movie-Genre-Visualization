filter_genre <- function(genre, movie_list = Movies){
  if(genre == "-")
    return (rep(c(TRUE), times = nrow(movie_list)))
  else{
    return (movie_list$genre1 == genre | 
              (!is.na(movie_list$genre2) & movie_list$genre2 == genre) | 
              (!is.na(movie_list$genre3) & movie_list$genre3 == genre))
  }
}

filter_movies <- function(row){
  columnCount <- length(row)
  if (columnCount == 1)
    movie_filter <- filter_genre(row[1])
  else if (columnCount == 2)
    movie_filter <- filter_genre(row[1]) & filter_genre(row[2])
  else
    movie_filter <- filter_genre(row[1]) & filter_genre(row[2]) & filter_genre(row[3])
  return (movie_filter)
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
  levels <- get(table)[,1]
  column_matrix <- t(sapply(get(table)[,column], unlist))
  if (type == "total")
    return (data.frame(get(table)[,1:3]))
  else if (type == "original")
    return (data.frame(levels, process_matrix(column_matrix, column)))
  else if (type == "row")
    return (data.frame(levels, process_row(column_matrix, column)))
  else if (type == "column")
    return (data.frame(levels, process_column(column_matrix, column)))
  else
    return (data.frame(levels, process_order(column_matrix, column)))
}

list_to_chart <- function(table, column){
  levels <- get(table)[,1]
  column_matrix <- t(sapply(get(table)[,column], unlist))
  wide_frame <- data.frame(levels, process_row(column_matrix, column))
  long_frame <- melt(wide_frame, id = "levels")
  return (long_frame)
}

process_matrix <- function(matrix, column){
  data_frame <- data.frame(matrix)
  colnames(data_frame) <- get(column)
  return (data_frame)
}

process_row <- function(matrix, column){
  row_total <- rowSums(matrix)
  row_percentage <- round(sweep(matrix, 1, row_total, '/') * 100, 2)
  row_percentage[is.nan(row_percentage)] <- 0
  return (process_matrix(row_percentage, column))
}

process_column <- function(matrix, column){
  column_total <- colSums(matrix)
  column_percentage <- round(sweep(matrix, 2, column_total, '/') * 100, 2)
  return (process_matrix(column_percentage, column))
}

process_order <- function(matrix, column){
  row_order <- apply(matrix, 1, order, decreasing = TRUE)
  row_labels <- apply(row_order, 1, function(x) get(column)[x])
  row_sorted <- t(apply(process_row(matrix, column), 1, sort, decreasing = TRUE))
  row_combined <- matrix(paste(row_labels, row_sorted, sep = " | "), ncol = ncol(matrix))
  final_table <- data.frame(row_combined)
  names(final_table) <- str_to_title(ordinal(1:ncol(matrix)))
  return (final_table)
}
