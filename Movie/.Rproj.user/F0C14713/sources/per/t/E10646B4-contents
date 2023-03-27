extract_movies <- function(zip_file){
  # Load all csv files
  csv_files <- unzip(zip_file, list = TRUE)$Name
  
  # Create empty data frame
  movies <- data.frame()
  
  # Genre list
  genre_list <- c()
  
  # Loop through movie list
  for (csv in csv_files) {
    # Load in csv file
    temp <- read.csv(unzip(zip_file, csv))
    
    # Drop unused columns
    temp <- subset(temp, select = -c(movie_id, description, director_id, star_id, gross.in...))
    
    # Extract genre name
    genreName <- sub('.csv', '', csv)
    
    # Handle sci-fi case
    genreName <- gsub("scifi", "sci-fi", genreName)
    
    # Handle sport case
    genreName <- gsub("sports", "sport", genreName)
    
    # Capitalize first letter
    genreName <- str_to_title(genreName)
    
    # Handle special case
    genreName <- gsub("(-[a-z])", "\\U\\1", genreName, perl=TRUE)
    
    # Add to genre list
    genre_list <- c(genre_list, genreName)
    
    # Add movies to data frame
    movies <- rbind(movies, temp)
    
    # Remove csv file
    file.remove(csv)
  }
  # Return extracted movies
  return (list(movies, genre_list))
}

process_runtime <- function(runtime){
  # Extract number from string
  runtime <- sub(' min', '', runtime)
  # Convert string to integer
  runtime <- strtoi(runtime)
  
  # Return processed runtime
  return (runtime)
}

process_year <- function(movies){
  # Convert year to integer
  movies$year <- strtoi(movies$year)
  
  # Remove unmade movies
  movies <- movies[!is.na(movies$year) & movies$year <= 2023, ]
  
  # Return processed movies
  return (movies)
}

process_genre <- function(movies){
  # Get genre list
  genreList <- strsplit(movies$genre, ", ")
  
  # Pad genre list with NA
  genreList <- lapply(genreList, "length<-", 3)
  
  # Separate genre list
  for (x in 1:3){
    # Get column name
    columnName <- paste("genre", x, sep = "")
    
    # Append new column
    movies[,columnName] <- sapply(genreList, "[[", x)
  }
  
  # Drop genre column
  movies <- subset(movies, select = -c(genre))
  
  # Return processed movies
  return (movies)
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

load_movies <- function(zip_file){
  # Extract movies
  data <- extract_movies(zip_file)
  
  # Get movies from list
  movies <- data[[1]]
  
  # Process movie runtime
  movies$runtime <- process_runtime(movies$runtime)
  
  # Process movie year
  movies <- process_year(movies)
  
  # Process movie genre
  movies <- process_genre(movies)
  
  # Remove duplicates
  movies <- movies %>% distinct()
  
  # Assign new certificates
  movies$certificate <- sapply(movies$certificate, assign_certificates)
  
  # Replace old movies list
  data[[1]] <- movies
  
  # Return movies
  return (data)
}