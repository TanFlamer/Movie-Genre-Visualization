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

count_combination <- function(row){
  columnCount <- length(row)
  if (columnCount == 1)
    movie_filter <- filter_genre(row[1])
  else if (columnCount == 2)
    movie_filter <- filter_genre(row[1]) & filter_genre(row[2])
  else
    movie_filter <- filter_genre(row[1]) & filter_genre(row[2]) & filter_genre(row[3])
  return (c(sum(movie_filter), get_ratings(movie_filter)))
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

get_ratings <- function(movie_filter){
  if (sum(movie_filter) == 0)
    return (rep(0, 6))
  else{
    filtered_movies <- Movies[movie_filter,]
    ratings <- addNA(cut(filtered_movies$rating, breaks = seq(0, 10, 2)))
    ratings <- data.frame(table(ratings))
    ratings <- ratings$Freq
    return (ratings)
  }
}

get_genres <- function(movie_filter){
  if (sum(movie_filter) == 0)
    return (rep(0, 16))
  else{
    filtered_movies <- Movies[movie_filter,]
    movie_count <- c()
    for (genre in GenreList){
      genre_count <- sum(filter_genre(genre, filtered_movies))
      movie_count <- c(movie_count, genre_count)
    }
    return (movie_count)
  }
}

get_certificate <- function(){
  certificates = c("G", "R", "PG", "PG-13", "TV-14", "TV-MA", "TV-PG", "Passed", "Unrated", "Approved")
  unrated = c("", "Unrated", "Not Rated")
  
  total <- c()
  rating_matrix <- matrix(ncol = 6, nrow = 0)
  genre_matrix <- matrix(ncol = 16, nrow = 0)
  
  other_filter = rep(c(FALSE), times = nrow(Movies))
  unrated_filter = rep(c(FALSE), times = nrow(Movies))
  
  for (certificate in certificates){
    movie_filter <- Movies$certificate == certificate
    total <- c(total, sum(movie_filter))
    rating_matrix <- rbind(rating_matrix, get_ratings(movie_filter))
    genre_matrix <- rbind(genre_matrix, get_genres(movie_filter))
    other_filter <- other_filter | movie_filter
  }
  
  for (certificate in unrated){
    movie_filter <- Movies$certificate == certificate
    unrated_filter = unrated_filter | movie_filter
  }
  
  total <- c(total, sum(unrated_filter))
  rating_matrix <- rbind(rating_matrix, get_ratings(unrated_filter))
  genre_matrix <- rbind(genre_matrix, get_genres(unrated_filter))
  
  other_filter <- other_filter | unrated_filter
  other_filter = !other_filter
  
  total <- c(total, sum(other_filter))
  rating_matrix <- rbind(rating_matrix, get_ratings(other_filter))
  genre_matrix <- rbind(genre_matrix, get_genres(other_filter))
  percentage <- round((total / sum(total)) * 100, 2)
  
  names <- c("original", "row", "column", "order")
  certificates <- c(certificates, "Unrated", "Other")
  
  rating_data <- process_matrix(rating_matrix)
  names(rating_data) <- paste("rating", names, sep = "_")
  genre_data <- process_matrix(rating_matrix)
  names(genre_data) <- paste("genre", names, sep = "_")
  
  return (data.frame(certificates, total, percentage, rating_data, genre_data))
}

get_decade <- function(){
  decade <- cut(Movies$year, breaks = c(-Inf, seq(1910, 2030, 10)), right = FALSE) # Partition into buckets
  total_data <- process_total(decade)
  rating_data <- process_rating(decade)
  genre_data <- process_genre(decade)
  interval <- levels(decade)
  return (data.frame(interval, total_data, rating_data, genre_data))
}

get_runtime <- function(){
  runtime <- addNA(cut(Movies$runtime, breaks = c(seq(0, 240, 30), Inf))) # Partition into buckets
  total_data <- process_total(runtime)
  rating_data <- process_rating(runtime)
  genre_data <- process_genre(runtime)
  interval <- levels(runtime)
  return (data.frame(interval, total_data, rating_data, genre_data))
}

get_votes <- function(){
  votes <- addNA(cut(Movies$votes, breaks = 10^(0:7))) # Partition into buckets
  total_data <- process_total(votes)
  rating_data <- process_rating(votes)
  genre_data <- process_genre(votes)
  interval <- levels(votes)
  return (data.frame(interval, total_data, rating_data, genre_data))
}

compare_ratings <- function(){
  ratings <- addNA(cut(Movies$rating, breaks = seq(0, 10, 2))) # Partition into buckets
  total_data <- process_total(ratings)
  genre_data <- process_genre(ratings)
  interval <- levels(ratings)
  return (data.frame(interval, total_data, genre_data))
}

compare_genre <- function(x){
  # Get column name
  tableName <- paste("Genre_", x, sep = "")
  
  # Generate genre combination
  temp <- combn(GenreList, x, simplify = FALSE)
  
  # Convert to data frame
  demo <- data.frame(matrix(nrow = length(temp), ncol = 0))
  
  # Separate genre list
  for (y in 1:x){
    # Get column name
    columnName <- paste("genre", y, sep = "")
    
    # Append new column
    demo[,columnName] <- sapply(temp, "[[", y)
  }
  
  # Get movie count and ratings
  count <- t(apply(demo, 1, count_combination))
  
  # Get total data
  total <- count[,1]
  
  # Get percentage data
  percentage <- round((total / nrow(Movies)) * 100, 2)
  
  # Get rating data
  rating_data <- process_matrix(count[, c(2:7)])
  
  # List of column names
  names <- c("original", "row", "column", "order")
  
  # Rename columns
  names(rating_data) <- paste("rating", names, sep = "_")
  
  # Return data frame
  return (data.frame(demo, total, percentage, rating_data))
}

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

matrix_to_list <- function(matrix){
  data_frame <- data.frame(t(matrix))
  return (as.list(data_frame))
}

list_to_frame <- function(column){
  matrix <- t(sapply(column, unlist))
  return (data.frame(matrix))
}

process_total <- function(factors){
  total <- c()
  for (x in 1:length(levels(factors))){
    movie_filter <- as.integer(factors) == x
    total <- c(total, sum(movie_filter))
  }
  percentage <- round((total / sum(total)) * 100, 2)
  return (data.frame(total, percentage))
}

process_rating <- function(factors){
  rating_matrix <- matrix(ncol = 6, nrow = 0)
  for (x in 1:length(levels(factors))){
    movie_filter <- as.integer(factors) == x
    rating_matrix <- rbind(rating_matrix, get_ratings(movie_filter))
  }
  names <- c("original", "row", "column", "order")
  rating_data <- process_matrix(rating_matrix)
  names(rating_data) <- paste("rating", names, sep = "_")
  return (rating_data)
}

process_genre <- function(factors){
  genre_matrix <- matrix(ncol = 16, nrow = 0)
  for (x in 1:length(levels(factors))){
    movie_filter <- as.integer(factors) == x
    genre_matrix <- rbind(genre_matrix, get_genres(movie_filter))
  }
  names <- c("original", "row", "column", "order")
  genre_data <- process_matrix(genre_matrix)
  names(genre_data) <- paste("genre", names, sep = "_")
  return (genre_data)
}