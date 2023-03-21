# Import library
library(stringr)
library(dplyr)

# Load all csv files
genres <- list.files(pattern = "*.csv")

# Create empty data frame
Movies <- data.frame()

# Genre list
GenreList <- c()

# Loop through movie list
for (genre in genres) {
  # Load in csv file
  temp <- read.csv(genre)
  
  # Extract number from string
  temp$runtime <- sub(' min', '', temp$runtime)
  
  # Convert string to integer
  temp$runtime <- strtoi(temp$runtime)
  
  # Convert year to integer
  temp$year <- strtoi(temp$year)
  
  # Remove unmade movies
  temp <- temp[!is.na(temp$year) & !(is.na(temp$runtime) & is.na(temp$rating)), ]
  
  # Drop unused columns
  temp <- subset(temp, select = -c(movie_id, description, director_id, star_id, gross.in...))
  
  # Extract genre name
  genreName <- sub('.csv', '', genre)
  
  # Capitalize first letter
  genreName <- str_to_title(genreName)
  
  # Handle special case
  genreName <- gsub("(-[a-z])","\\U\\1", genreName, perl=TRUE)
  
  # Add to genre list
  GenreList <- c(GenreList, genreName)
  
  # Add movies to data frame
  Movies <- rbind(Movies, temp)
}

# Remove duplicates
Movies <- Movies %>% distinct()

# Get genre list
genreList <- strsplit(Movies$genre, ", ")

# Remove genre
Movies <- subset(Movies, select = -c(genre))

# Add genre list
for (genreName in GenreList){
  # Append column to temp
  Movies[,genreName] <- data.frame(rep(c(FALSE), times = nrow(Movies)))
}

# Mark movie genre
for (x in 1:nrow(Movies)){
  # Loop through genre tags
  for (genreTag in genreList[[x]]){
    # Check if genre tag exists
    if (genreTag %in% colnames(Movies)){
      # Set genre to TRUE
      Movies[,genreTag][x] = TRUE
    }
  }
}

# Remove unused variables
rm(x)
rm(temp)
rm(genre)
rm(genres)
rm(genreTag)
rm(genreName)
rm(genreList)