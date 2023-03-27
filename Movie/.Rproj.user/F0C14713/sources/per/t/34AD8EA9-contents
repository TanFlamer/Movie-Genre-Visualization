# Import library
library(stringr)
library(dplyr)

# Load functions
source("preprocess.R")
source("process.R")
source("plot.R")

# Load movies and genre
list2env(setNames(load_movies("archive.zip"), c("Movies", "genres")), envir = globalenv())

# Process movie data
Rating <- compare_data(FALSE, factors = addNA(cut(Movies$rating, breaks = seq(0, 10, 2))), func = rename_strings)
rating <- Rating$levels

Runtime <- compare_data(FALSE, factors = addNA(cut(Movies$runtime, breaks = c(seq(0, 240, 30), Inf))), func = rename_strings)
runtime <- Runtime$levels

Votes <- compare_data(FALSE, factors = addNA(cut(Movies$votes, breaks = 10^(0:7))), func = convert_exponent)
votes <- Votes$levels

Decade <- compare_data(FALSE, factors = cut(Movies$year, breaks = c(-Inf, seq(1910, 2030, 10)), right = FALSE), func = convert_exponent)
decade <- Decade$levels

Certificate <- compare_data(FALSE, factors = factor(Movies$certificate, unique(Movies$certificate)))
certificate <- Certificate$levels

# Process genre data
Genre1 <- compare_data(TRUE, x = 1)
Genre2 <- compare_data(TRUE, x = 2)
Genre3 <- compare_data(TRUE, x = 3)
