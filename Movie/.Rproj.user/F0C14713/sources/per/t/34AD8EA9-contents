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

# Create genre combinations
for (x in 1:3){
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
  
  # Get movie count
  count <- apply(demo, 1, count_combination)
  
  # Append movie count to table
  demo$count <- sapply(count, "[[", 1)
  
  # Assign table name
  assign(tableName, demo)
}

# Remove unused variables
rm(x)
rm(y)
rm(csv)
rm(temp)
rm(demo)
rm(count)
rm(zip_file)
rm(csv_files)
rm(tableName)
rm(genreList)
rm(genreName)
rm(columnName)
