# Sankey diagram

library(tidyverse)
library(plotly)
library(viridis)

df <- read_csv('../all_results.csv')

df1 <- df %>%
  filter(status == "scheduled") %>%
  select(P_ID, instance_id, activity) %>%
  distinct() %>%
  unite("node", c(instance_id, activity), sep="-", remove = F)

nodes <- df1 %>% select(node) %>% distinct() %>% mutate(id = row_number() - 1)

df2 <- df1 %>%
  arrange(P_ID, instance_id) %>%
  group_by(P_ID) %>%
  mutate(
    next_node = lead(node)
  ) %>% ungroup() %>%
  filter(!is.na(next_node))

df3 <- df2 %>%
  count(node, next_node)

source = df3 %>% inner_join(nodes, by="node") %>% pull(id)
target = df3 %>% inner_join(nodes, by=c("next_node" = "node")) %>% pull(id)
value = df3 %>% pull(n)
nodes_label = nodes %>% pull(node)


fig <- plot_ly(
  type = "sankey",
  orientation = "h",
  
  node = list(
    label = nodes_label,
    pad = 15,
    thickness = 20,
    line = list(
      color = "black",
      width = 0.5
    )
  ),
  
  link = list(
    source = source,
    target = target,
    value =  value
    )
)


fig <- fig %>% layout(
  title = "Basic Sankey Diagram",
  font = list(
    size = 10
  )
)

fig

