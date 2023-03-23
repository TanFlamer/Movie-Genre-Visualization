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
    return (sum(filter_genre(row[1])))
  else if (columnCount == 2)
    return (sum(filter_genre(row[1]) & filter_genre(row[2])))
  else
    return (sum(filter_genre(row[1]) & filter_genre(row[2]) & filter_genre(row[3])))
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
    return (rep(0, 10))
  else{
    filtered_movies <- Movies[movie_filter,]
    ratings <- cut(filtered_movies$rating, breaks = seq(0, 10))
    ratings <- data.frame(table(ratings))
    ratings <- ratings$Freq
    total <- sum(ratings)
    ratings <- round((ratings / total) * 100, 2)
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