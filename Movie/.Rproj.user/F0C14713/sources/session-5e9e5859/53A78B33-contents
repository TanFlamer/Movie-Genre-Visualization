filter_genre <- function(genre){
  if(genre == "All")
    return (rep(c(TRUE), times = nrow(Movies)))
  else{
    return (Movies$genre1 == genre | 
              (!is.na(Movies$genre2) & Movies$genre2 == genre) | 
              (!is.na(Movies$genre3) & Movies$genre3 == genre))
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