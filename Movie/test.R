# sum(grepl("Adventure", action$genre, fixed = TRUE))

# rm(list = ls())

# cat("\014")

year <- c(-Inf, seq(1910, 2030, 10)) # 13 breaks

sum(as.integer(decade) == 1) # 1 - 13

10^(0:10) # Generate powers of 10

decade <- cut(Movies$year, breaks = year, right = FALSE) # Partition into buckets

ratings <- seq(0, 10)

data.frame(table(decade))

demo$decade <- year[2:14] - 10

# Distribution of genre and rating vary with year/runtime/votes
