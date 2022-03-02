# Peek at DES data

library(tidyverse)

df <- read_csv('../all_results.csv')

df %>% glimpse()

df %>% view()

df %>% filter(P_ID == 5) %>% view()
  