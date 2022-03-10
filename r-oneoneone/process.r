# Peek at DES data

library(tidyverse)
library(lubridate)
library(bupaR)
library(processanimateR)

df <- read_csv('../all_results.csv')

# df %>% glimpse()
# 
# df %>% view()
# 
# df %>% filter(P_ID == 5) %>% view()
# 
# df %>% count(n_distinct(P_ID))

start_dt = lubridate::ymd_hm("2022-01-31 09:00")


event_log_df <- df %>% filter(run_number == 5) %>%
  mutate(
    P_ID = as.character(P_ID),
    resource = NA,
    calc_dt = start_dt + (timestamp * 60),
    instance_id = as.character(instance_id),
  ) %>% 
  eventlog(
    case_id = "P_ID",
    activity_id = "activity",
    activity_instance_id = "instance_id",
    lifecycle_id = "status",
    timestamp = "calc_dt",
    resource_id = "resource",
    order = "auto",
    validate = FALSE
  )

event_log_df %>% process_map()


event_log_df %>%
  animate_process(duration = 240, jitter = 10, mapping = token_aes(size = token_scale(6)))


event_log_df %>%
  animate_process(duration = 240, jitter = 10,
                  mapping = token_aes(shape = 'image', size = token_scale(10), image = token_scale("https://upload.wikimedia.org/wikipedia/commons/5/5f/Pacman.gif")))

df %>% count(P_ID, run_number, day, hour)  %>% distinct() %>% count(run_number, day, hour) %>%
  group_by(day, hour) %>%
  summarise(
    cases = mean(n, na.rm = T)
  ) %>% ungroup() %>%
  ggplot(aes(x = hour, y = cases)) +
  geom_col() +
  facet_wrap(~day)
