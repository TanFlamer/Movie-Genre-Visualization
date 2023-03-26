# Import library
library(stringr)
library(dplyr)

# Zip file name
zip_file <- "archive.zip"

# Load all csv files
csv_files <- unzip(zip_file, list = TRUE)$Name

# Create empty data frame
Movies <- data.frame()

# Genre list
GenreList <- c()

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
  GenreList <- c(GenreList, genreName)
  
  # Add movies to data frame
  Movies <- rbind(Movies, temp)
  
  # Remove csv file
  file.remove(csv)
}

# Extract number from string
Movies$runtime <- sub(' min', '', Movies$runtime)

# Convert string to integer
Movies$runtime <- strtoi(Movies$runtime)

# Convert year to integer
Movies$year <- strtoi(Movies$year)

# Remove unmade movies
Movies <- Movies[!is.na(Movies$year) & Movies$year <= 2023, ]

# Get genre list
genreList <- strsplit(Movies$genre, ", ")

# Pad genre list with NA
genreList <- lapply(genreList, "length<-", 3)

# Separate genre list
for (x in 1:3){
  # Get column name
  columnName <- paste("genre", x, sep = "")
  
  # Append new column
  Movies[,columnName] <- sapply(genreList, "[[", x)
}

# Drop genre column
Movies <- subset(Movies, select = -c(genre))

# Remove duplicates
Movies <- Movies %>% distinct()

# Assign new certificates
Movies$certificate <- sapply(Movies$certificate, assign_certificates)

# Remove unused variables
rm(x)
rm(csv)
rm(temp)
rm(zip_file)
rm(csv_files)
rm(genreList)
rm(genreName)
