# Functions used in Data Transformation

# Factor movies further by rating
get_ratings <- function(movie_filter){
  
  if (sum(movie_filter) == 0)
    # All 0s if empty filter
    return (rep(0, 6))
  else{
    
    # Get filtered movies
    filtered_movies <- Movies[movie_filter,]
    
    # Buckets of 2
    buckets <- seq(0, 10, 2)
    
    # Factor movies further by rating
    ratings <- addNA(cut(filtered_movies$rating, breaks = buckets))
    
    # Return frequency
    return (factors_to_frequency(ratings))
  }
}

# Factor movies further by genre
get_genres <- function(movie_filter){
  
  if (sum(movie_filter) == 0)
    # All 0s if empty filter
    return (rep(0, 16))
  else{
    
    # Get filtered movies
    filtered_movies <- Movies[movie_filter,]
    
    # Vector to store movie count
    movie_count <- c()
    
    # Loop through genres
    for (genre in genres){
      
      # Count number of movies with genre
      genre_count <- sum(filter_genre(genre, filtered_movies))
      
      # Append movie number to vector
      movie_count <- c(movie_count, genre_count)
    }
    
    # Return vector of movie count
    return (movie_count)
  }
}

# Factor movies further by runtime
get_runtime <- function(movie_filter){
  
  if (sum(movie_filter) == 0)
    # All 0s if empty filter
    return (rep(0, 10))
  else{
    
    # Get filtered movies
    filtered_movies <- Movies[movie_filter,]
    
    # Buckets of 30 minutes
    buckets <- c(seq(0, 240, 30), Inf)
    
    # Factor movies further by runtime
    runtime <- addNA(cut(filtered_movies$runtime, breaks = buckets))
    
    # Return frequency
    return (factors_to_frequency(runtime))
  }
}

# Factor movies further by votes
get_votes <- function(movie_filter){
  
  if (sum(movie_filter) == 0)
    # All 0s if empty filter
    return (rep(0, 8))
  else{
    
    # Get filtered movies
    filtered_movies <- Movies[movie_filter,]
    
    # Buckets of powers of 10
    buckets <- 10^(0:7)
    
    # Factor movies further by votes
    votes <- addNA(cut(filtered_movies$votes, breaks = buckets))
    
    # Return frequency
    return (factors_to_frequency(votes))
  }
}

# Factor movies further by decade
get_decades <- function(movie_filter){
  
  if (sum(movie_filter) == 0)
    # All 0s if empty filter
    return (rep(0, 13))
  else{
    
    # Get filtered movies
    filtered_movies <- Movies[movie_filter,]
    
    # Buckets of 10 years
    buckets <- c(-Inf, seq(1910, 2030, 10))
    
    # Factor movies further by decade
    decades <- cut(filtered_movies$year, breaks = buckets, right = FALSE)
    
    # Return frequency
    return (factors_to_frequency(decades))
  }
}

# Factor movies further by certificate
get_certificates <- function(movie_filter){
  
  if (sum(movie_filter) == 0)
    # All 0s if empty filter
    return (rep(0, 11))
  else{
    
    # Get filtered movies
    filtered_movies <- Movies[movie_filter,]
    
    # Factors of movie certificates
    factors <- unique(Movies$certificate)
    
    # Factor movies further by certificate
    certificates <- factor(filtered_movies$certificate, factors)
    
    # Return frequency
    return (factors_to_frequency(certificates))
  }
}

# Get frequency of factors
factors_to_frequency <- function(factors){
  
  # Convert factors to table
  table <- table(factors)
  
  # Convert table to data frame
  data_frame <- data.frame(table)
  
  # Return frequency of data frame
  return (data_frame$Freq)
}

# Divide data further by secondary factor
compare_data <- function(genre, x = 0, factors = NULL, func = NULL){
  
  # Vector of primary factor count
  total <- c()
  
  # Matrices of secondary factor count
  rating_matrix = matrix(ncol = 6, nrow = 0)
  genre_matrix = matrix(ncol = 16, nrow = 0)
  runtime_matrix = matrix(ncol = 10, nrow = 0)
  votes_matrix = matrix(ncol = 8, nrow = 0)
  decade_matrix = matrix(ncol = 13, nrow = 0)
  certificate_matrix = matrix(ncol = 11, nrow = 0)
  
  # Generate combinations of genres (16Cx)
  genres <- combn(genres, x, simplify = FALSE)
  
  if (genre == TRUE)
    # Genre length
    length <- length(genres)
  else
    # Factor length
    length <- length(levels(factors))
  
  # Loop through genre/factor length
  for (x in 1:length){
    
    if (genre == TRUE)
      # Filter movies by genre combinations
      movie_filter <- filter_movies(genres[[x]])
    else
      # Filter movies by factors
      movie_filter <- as.integer(factors) == x
    
    # Append count of primary factor
    total <- c(total, sum(movie_filter))
    
    # Append count of secondary factors
    rating_matrix = rbind(rating_matrix, get_ratings(movie_filter))
    genre_matrix = rbind(genre_matrix, get_genres(movie_filter))
    runtime_matrix = rbind(runtime_matrix, get_runtime(movie_filter))
    votes_matrix = rbind(votes_matrix, get_votes(movie_filter))
    decade_matrix = rbind(decade_matrix, get_decades(movie_filter))
    certificate_matrix = rbind(certificate_matrix, get_certificates(movie_filter))
  }
  
  # Create new data frame to store data
  data <- data.frame(matrix(ncol = 0, nrow = length))
  
  if (genre == TRUE)
    # Use genres as factors
    data$factors <- unlist(lapply(genres, toString))
  else if (is.null(func))
    # Use factors as factors
    data$factors <- levels(factors)
  else
    # Use function to rename factors
    data$factors <- func(levels(factors))
  
  # Column to save primary factor count
  data$total <- total
  
  if (genre == TRUE)
    # Calculate percentage by Movies length (207919)
    data$percentage <- round((total / nrow(Movies)) * 100, 2)
  else
    # Calculate percentage by column length
    data$percentage <- round((total / sum(total)) * 100, 2)
  
  # Columns to save secondary factor count as lists
  data$rating <- matrix_to_list(rating_matrix)
  data$genres <- matrix_to_list(genre_matrix)
  data$runtime <- matrix_to_list(runtime_matrix)
  data$votes <- matrix_to_list(votes_matrix)
  data$decade <- matrix_to_list(decade_matrix)
  data$certificate <- matrix_to_list(certificate_matrix)
  
  if (genre == TRUE)
    # Return new data frame
    return (data)
  else
    # Return new data frame and factors
    return (list(data, data$factors))
}

# Convert matrix to list
matrix_to_list <- function(matrix){
  
  # Convert matrix to data frame
  data_frame <- data.frame(t(matrix))
  
  # Return data frame as list
  return (as.list(data_frame))
}

# Rename factors as strings
rename_strings <- function(strings){
  
  # Remove brackets from factors
  strings <- gsub("\\(|\\)|\\[|\\]", "", strings)
  
  # Change -Inf to 1900 (Only for decade)
  strings <- gsub("-Inf", "1900", strings)
  
  # Change , to -
  strings <- gsub(",", "-", strings)
  
  # Return new strings
  return (strings)
}

# Convert numbers from exponent to normal form
convert_exponent <- function(strings){
  
  # Rename factors as strings
  strings <- rename_strings(strings)
  
  # Check if last element is NA
  contains_na <- is.na(strings[length(strings)])
  
  # Remove NA from vector
  strings <- na.omit(strings)
  
  # Split strings by -
  strings <- strsplit(strings, "-")
  
  # Convert strings to numbers
  string_matrix <- sapply(strings, strings_to_numbers)
  
  # Append two number lists
  string_list <- apply(string_matrix, 2, append_numbers)
  
  # Add back NA to vector
  if (contains_na) string_list <- c(string_list, NA)
  
  # Return new strings
  return (string_list)
}

# Convert strings to numbers
strings_to_numbers <- function(strings){
  
  # Convert strings to number list
  list <- lapply(strings, string_to_number)
  
  # Return number list
  return (list)
}

# Convert string to number
string_to_number <- function(string){
  
  # Parse string
  parsed_string <- parse(text = string)
  
  # Evaluate string as number
  number <- eval(parsed_string)
  
  # Return evaluated number
  return (number)
}

# Append two numbers to list
append_numbers <- function(column){
  
  # First number in normal form
  num1 <- format(column[1], scientific = FALSE)
  
  # Second number in normal form
  num2 <- format(column[2], scientific = FALSE)
  
  # Append both numbers
  num_append <- paste(num1, num2, sep = "-")
  
  # Return appended numbers
  return (num_append)
}
