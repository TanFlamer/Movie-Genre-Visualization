# Functions used in Data Visualization

# Filter movie by genre
filter_genre <- function(genre, movie_list = Movies){
  
  if(genre == "-")
    # Return all TRUE
    return (rep(c(TRUE), times = nrow(movie_list)))
  else{
    
    # Filter genre in given movie list
    return (movie_list$genre1 == genre | 
              (!is.na(movie_list$genre2) & movie_list$genre2 == genre) | 
              (!is.na(movie_list$genre3) & movie_list$genre3 == genre))
  }
}

# Filter movie by genres
filter_movies <- function(row){
  
  # Get number of columns
  columnCount <- length(row)
  
  if (columnCount == 1)
    # Filter one genre
    movie_filter <- filter_genre(row[1])
  else if (columnCount == 2)
    # Filter two genres
    movie_filter <- filter_genre(row[1]) & filter_genre(row[2])
  else
    # Filter three genres
    movie_filter <- filter_genre(row[1]) & filter_genre(row[2]) & filter_genre(row[3])
  
  # Return movie filter
  return (movie_filter)
}

# Plot line graph
movie_plot <- function(type, movie_filter){
  
  if (sum(movie_filter) == 0)
    # Return empty data frame
    return (data.frame(matrix(ncol = 2, nrow = 0)))
  else{
    
    # Get filtered movies
    filtered_movies <- Movies[movie_filter,]
    
    # Get filtered row
    filtered_row = filtered_movies[,type]
    
    # Get list of years
    year_list = list(filtered_movies$year)
    
    if (type == "year")
      # Return movie count
      return (aggregate(filtered_row, year_list, length))
    else
      # Return average of given type
      return (aggregate(filtered_row, year_list, mean, na.rm = TRUE))
  }
}

# Convert data frame list to table
list_to_table <- function(table, column, type){
  
  # Get factors from 1st column
  factors <- get(table)[,1]
  
  # Convert column to matrix
  column_matrix <- column_to_matrix(table, column)
  
  if (type == "total")
    # Return total and percentage
    return (data.frame(factors, get(table)[,2:3]))
  else if (type == "original")
    # Return original data
    return (data.frame(factors, matrix_to_frame(column_matrix, column)))
  else if (type == "row")
    # Return row percentages
    return (data.frame(factors, process_row(column_matrix, column)))
  else if (type == "column")
    # Return column percentages
    return (data.frame(factors, process_column(column_matrix, column)))
  else
    # Return row order
    return (data.frame(factors, process_order(column_matrix, column)))
}

# Convert data frame list to chart
list_to_chart <- function(table, column){
  
  # Get factors from 1st column
  factors <- get(table)[,1]
  
  # Convert column to matrix
  column_matrix <- column_to_matrix(table, column)
  
  # Get original data 
  wide_frame <- data.frame(factors, matrix_to_frame(column_matrix, column))
  
  # Convert data from wide to long format
  long_frame <- melt(wide_frame, id = "factors")
  
  # Return data in long format
  return (long_frame)
}

# Convert column to matrix
column_to_matrix <- function(table, column){
  
  # Get column from table
  column <- get(table)[,column]
  
  # Convert column to matrix
  column_matrix <- t(sapply(column, unlist))
  
  # Return column matrix
  return (column_matrix)
}

# Convert matrix to data frame
matrix_to_frame <- function(matrix, column){
  
  # Convert matrix to data frame
  data_frame <- data.frame(matrix)
  
  # Rename data frame column names
  colnames(data_frame) <- get(column)
  
  # Return new data frame
  return (data_frame)
}

# Return row percentages
process_row <- function(matrix, column){
  
  # Get row count of matrix
  row_total <- rowSums(matrix)
  
  # Get percentage by dividing row count
  row_percentage <- round(sweep(matrix, 1, row_total, '/') * 100, 2)
  
  # Convert NA to 0
  row_percentage[is.nan(row_percentage)] <- 0
  
  # Convert matrix to data frame
  return (matrix_to_frame(row_percentage, column))
}

# Return column percentages
process_column <- function(matrix, column){
  
  # Get column count of matrix
  column_total <- colSums(matrix)
  
  # Get percentage by dividing column count
  column_percentage <- round(sweep(matrix, 2, column_total, '/') * 100, 2)
  
  # Convert matrix to data frame
  return (matrix_to_frame(column_percentage, column))
}

# Return row order
process_order <- function(matrix, column){
  
  # Get row order
  row_order <- apply(matrix, 1, order, decreasing = TRUE)
  
  # Convert row order to factors
  row_labels <- apply(row_order, 1, function(x) get(column)[x])
  
  # Return row percentages
  row_percentages <- process_row(matrix, column)
  
  # Sort rows in descending order
  row_sorted <- t(apply(row_percentages, 1, sort, decreasing = TRUE))
  
  # Combine row factors with sorted row
  row_combined <- paste(row_labels, row_sorted, sep = " | ")
  
  # Convert combined rows to matrix
  row_combined <- matrix(row_combined, ncol = ncol(matrix))
  
  # Convert matrix to data frame
  final_table <- data.frame(row_combined)
  
  # Get ordinals for column names
  col_names <- ordinal(1:ncol(matrix))
  
  # Rename data frame columns
  names(final_table) <- str_to_title(col_names)
  
  # Return new data frame
  return (final_table)
}
