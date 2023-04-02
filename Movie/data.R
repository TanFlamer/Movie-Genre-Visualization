# Load data into app

# Load movies
message("Loading movies")
data <- load_movies("archive.zip")
data <- setNames(data, c("Movies", "genres"))
list2env(data, globalenv())

# Load rating
message("Loading ratings")
factor = addNA(cut(Movies$rating, breaks = seq(0, 10, 2)))
data <- compare_data(FALSE, factors = factor, func = rename_strings)
data <- setNames(data, c("Rating", "rating"))
list2env(data, globalenv())

# Load runtime
message("Loading runtime")
factor = addNA(cut(Movies$runtime, breaks = c(seq(0, 240, 30), Inf)))
data <- compare_data(FALSE, factors = factor, func = rename_strings)
data <- setNames(data, c("Runtime", "runtime"))
list2env(data, globalenv())

# Load votes
message("Loading votes")
factor = addNA(cut(Movies$votes, breaks = 10^(0:7)))
data <- compare_data(FALSE, factors = factor, func = convert_exponent)
data <- setNames(data, c("Votes", "votes"))
list2env(data, globalenv())

# Load decades
message("Loading decades")
factor = cut(Movies$year, breaks = c(-Inf, seq(1910, 2030, 10)), right = FALSE)
data <- compare_data(FALSE, factors = factor, func = convert_exponent)
data <- setNames(data, c("Decade", "decade"))
list2env(data, globalenv())

# Load certificates
message("Loading certificates")
factor = factor(Movies$certificate, unique(Movies$certificate))
data <- compare_data(FALSE, factors = factor)
data <- setNames(data, c("Certificate", "certificate"))
list2env(data, globalenv())

# Load genres
message("Loading genres")
data <- list()
for (count in 1:3) data <- c(data, list(compare_data(TRUE, x = count)))
data <- setNames(data, c("Genre1", "Genre2", "Genre3"))
list2env(data, globalenv())

# Success message
message("Data loaded successfully")
