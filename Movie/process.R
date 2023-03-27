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
    for (genre in genres){
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
    certificates <- factor(filtered_movies$certificate, unique(Movies$certificate))
    certificates <- data.frame(table(certificates))
    certificates <- certificates$Freq
    return (certificates)
  }
}

compare_data <- function(genre, x = 0, factors = NULL, func = NULL){
  total <- c()
  rating_matrix = matrix(ncol = 6, nrow = 0)
  genre_matrix = matrix(ncol = 16, nrow = 0)
  runtime_matrix = matrix(ncol = 10, nrow = 0)
  votes_matrix = matrix(ncol = 8, nrow = 0)
  decade_matrix = matrix(ncol = 13, nrow = 0)
  certificate_matrix = matrix(ncol = 11, nrow = 0)
  
  genres <- combn(genres, x, simplify = FALSE)
  if (genre == TRUE)
    length <- length(genres)
  else
    length <- length(levels(factors))
  
  for (x in 1:length){
    if (genre == TRUE)
      movie_filter <- filter_movies(genres[[x]])
    else
      movie_filter <- as.integer(factors) == x
    
    total <- c(total, sum(movie_filter))
    rating_matrix = rbind(rating_matrix, get_ratings(movie_filter))
    genre_matrix = rbind(genre_matrix, get_genres(movie_filter))
    runtime_matrix = rbind(runtime_matrix, get_runtime(movie_filter))
    votes_matrix = rbind(votes_matrix, get_votes(movie_filter))
    decade_matrix = rbind(decade_matrix, get_decades(movie_filter))
    certificate_matrix = rbind(certificate_matrix, get_certificates(movie_filter))
  }
  
  data <- data.frame(matrix(ncol = 0, nrow = length))
  if (genre == TRUE)
    data$levels <- unlist(lapply(genres, toString))
  else if (is.null(func))
    data$levels <- levels(factors)
  else
    data$levels <- func(levels(factors))
  
  data$total <- total
  data$percentage <- round((total / sum(total)) * 100, 2)
  data$rating <- matrix_to_list(rating_matrix)
  data$genres <- matrix_to_list(genre_matrix)
  data$runtime <- matrix_to_list(runtime_matrix)
  data$votes <- matrix_to_list(votes_matrix)
  data$decade <- matrix_to_list(decade_matrix)
  data$certificate <- matrix_to_list(certificate_matrix)
  
  return (data)
}

rename_strings <- function(strings){
  strings <- gsub("\\(|\\)|\\[|\\]", "", strings)
  strings <- gsub("-Inf", "1900", strings)
  strings <- gsub(",", "-", strings)
  return (strings)
}

convert_exponent <- function(strings){
  strings <- rename_strings(strings)
  contains_na <- is.na(strings[length(strings)])
  strings <- na.omit(strings)
  string_matrix <- sapply(strsplit(rename_strings(strings), "-"), function(x) lapply(x, function(y) eval(parse(text = y))))
  string_list <- apply(string_matrix, 2, function(column) paste(format(column[1], scientific = FALSE), format(column[2], scientific = FALSE), sep = "-"))
  if (contains_na) string_list <- c(string_list, NA)
  return (string_list)
}

matrix_to_list <- function(matrix){
  list <- as.list(data.frame(t(matrix)))
  return (list)
}
