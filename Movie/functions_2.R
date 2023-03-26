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

get_runtime <- function(movie_filter){
  if (sum(movie_filter) == 0)
    return (rep(0, 10))
  else{
    filtered_movies <- Movies[movie_filter,]
    runtime <- addNA(cut(filtered_movies$runtime, breaks = c(seq(0, 240, 30), Inf)))
    runtime <- data.frame(table(runtime))
    runtime <- runtime$Freq
    return (runtime)
  }
}

get_votes <- function(movie_filter){
  if (sum(movie_filter) == 0)
    return (rep(0, 8))
  else{
    filtered_movies <- Movies[movie_filter,]
    votes <- addNA(cut(filtered_movies$votes, breaks = 10^(0:7)))
    votes <- data.frame(table(votes))
    votes <- votes$Freq
    return (votes)
  }
}

get_decades <- function(movie_filter){
  if (sum(movie_filter) == 0)
    return (rep(0, 13))
  else{
    filtered_movies <- Movies[movie_filter,]
    decades <- cut(filtered_movies$year, breaks = c(-Inf, seq(1910, 2030, 10)), right = FALSE)
    decades <- data.frame(table(decades))
    decades <- decades$Freq
    return (decades)
  }
}

get_certificates <- function(movie_filter){
  if (sum(movie_filter) == 0)
    return (rep(0, 11))
  else{
    filtered_movies <- Movies[movie_filter,]
    certificates <- factor(filtered_movies$certificate, levels)
    certificates <- data.frame(table(certificates))
    certificates <- certificates$Freq
    return (certificates)
  }
}

compare_data <- function(factors){
  func <- list(get_ratings = get_ratings, get_genres = get_genres, get_runtime= get_runtime,
               get_votes = get_votes, get_decades = get_decades, get_certificates = get_certificates)
  col <- list(6, 16, 10, 8, 13, 11)
  data_frame <- data.frame(levels(factors), process_total(factors))
  for (x in 1:6){
    data_frame <- data.frame(data_frame, process_data(factors, col[[x]], func[[x]]))
  }
  names(data_frame) <- c("levels", "total", "percentage", "rating", "genre", "runtime", "votes", "decade", "certificate")
  return (data_frame)
}

compare_genre <- function(x){
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
  
  # Rename columns
  names(rating_data)[1] <- "rating"
  
  # Return data frame
  return (data.frame(demo, total, percentage, rating_data))
}