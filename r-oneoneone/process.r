# Load libraries ------------

library(tidyverse)
library(lubridate)
library(bupaR)
library(processanimateR)

# Helper functions ----------


# This function will return a date time that is closest to the start of any given year
# In this case, there is a 24 hour warm up period starting on the Sunday, so we'll start with Monday

getFirstDayOfYear <- function(hour="09", dow = 1, theyear = year(now())) {

  dt_string = glue::glue("{theyear}-01-01-{hour}:00")
  dt <- lubridate::ymd_hm(dt_string)
  day_of_week = wday(dt, week_start = 1)
  
  actual_dt <- case_when(
    day_of_week == dow ~ dt,
    day_of_week > dow ~ dt + days(7 - day_of_week + dow),
    day_of_week < dow ~ dt + days(dow - day_of_week),
    TRUE ~ NA_POSIXct_
  )
  
  return(actual_dt)
  
}

# getFirstDayOfYear()
# getFirstDayOfYear("01", 5, "2021") # First Friday in 2021
# getFirstDayOfYear("10", 2, "2021") # First Tuesday in 2021
# getFirstDayOfYear("10", 7, "2021") # First Sunday in 2021


# Primary care dispositions ----------

pc_disp_df <- tibble(
  disposition = c("Dx05", "Dx06", "Dx07", "Dx08", "Dx11", "Dx12", "Dx13", "Dx14", "Dx15", "Dx61", "Dx75","Dx116", "Dx117"),
  time_frame_hours = c(2, 6, 12, 24, 1, 2, 6, 12, 24, 0.3, 72, 6, 1),
  contact_speak = c("contact", "contact", "contact", "contact", "speak", "speak", "speak", "speak", "speak", "speak", "contact", "speak", "speak"),
)


# Let's go --------------

start_dt = getFirstDayOfYear()
warm_up = 1440 # Warm up time in minutes

df <- read_csv('../all_results.csv')

df1 <- df %>%
  mutate(
    dt_curr_activity = start_dt + minutes(round(timestamp - warm_up)),
    # Note values look like this: [0, 5)
    # This means 0 is included, but 5 is not i.e. 0, 1, 2, 3, 4
    age_range = cut(age, breaks = seq(0, 110, 5), right = F)
  ) %>% 
  group_by(run_number, P_ID, instance_id) %>%
  summarise(
    age = first(age),
    age_range = first(age_range),
    sex = first(sex),
    day = first(day),
    hour = first(hour),
    disposition = first(disposition),
    GP = first(GP),
    activity=first(activity),
    wait_time = interval(dt_curr_activity[status == "scheduled"], dt_curr_activity[status == "start"]) / minutes(1),
    activity_time = interval(dt_curr_activity[status == "start"], dt_curr_activity[status == "completed"]) / minutes(1)
  ) %>% 
  ungroup() %>%
  left_join(pc_disp_df, by="disposition") %>%
  mutate(
    time_frame_mins = time_frame_hours * 60,
    gp_in_time_frame = case_when(
      instance_id == 1 & activity == "GP" & wait_time <= time_frame_mins ~ "Yes",
      instance_id == 1 & activity == "GP" & wait_time > time_frame_mins ~ "No",
      instance_id == 1 & activity != "GP" ~ "Did not see GP",
      TRUE ~ NA_character_
    )
  )


df1 %>% count(gp_in_time_frame)



  