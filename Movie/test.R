# sum(grepl("Adventure", action$genre, fixed = TRUE))

# rm(list = ls())

# cat("\014")

mapply(count_combination, Genre_1$genre1, Genre_1$genre2, Genre_1$genre3)

names(count) <- seq(1, length(count))

Genre_1$count <- sapply(count, "[[", 1)
