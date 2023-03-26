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

process_data <- function(factors, col, func){
  matrix <- matrix(ncol = col, nrow = 0)
  for (x in 1:length(levels(factors))){
    movie_filter <- as.integer(factors) == x
    matrix <- rbind(matrix, func(movie_filter))
  }
  data <- data.frame(matrix(ncol = 0, nrow = nrow(matrix)))
  data$original <- as.list(data.frame(t(matrix)))
  return (data)
}

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

order_genre <- function(){
  
}