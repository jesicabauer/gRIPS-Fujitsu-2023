library(tidyverse)

setwd('C:/Users/Jesica/Documents/grips-sendai/Fujitsu')
original = read_csv('animals_train (1).csv')


# Find the New Numeric "Factors" ------------------------------------------

reduce_numerics <- original %>% 
  select(Label, Legs) %>% 
  group_by_all() %>%
  summarise(n = n()) %>%
  ungroup() %>%
  complete(Label, Legs) %>%
  mutate_all(~replace(., is.na(.), 0)) %>%
  group_by(Legs) %>%
  mutate(maxn = ifelse(n == max(n), Label, abs(Label - 1)))

cutoffs <- reduce_numerics %>% 
  arrange(Legs, Label)
beforeLegs <- cutoffs$Legs[which(cutoffs$maxn != lag(cutoffs$maxn))-1]
afterLegs <- cutoffs$Legs[which(cutoffs$maxn != lag(cutoffs$maxn))]

beforeLegs + abs(beforeLegs - afterLegs)/2
newBreaks <- c(beforeLegs + abs(beforeLegs - afterLegs)/2)

animals <- original 

for (Breaks in newBreaks) {
  animals <- animals %>% 
    mutate(!!paste0("<", Breaks) := ifelse(Legs < Breaks, 
                                           paste0("Legs<", Breaks), 
                                           paste0("Legs>=", Breaks)))
}


# Make all values into Unique Factors -------------------------------------

animals <- animals %>%
  mutate(across(.cols = -c(Name, Label, Legs, all_of(paste0("<", newBreaks))),
                .fns = function(x) as.factor(paste(sep = "_", cur_column(), x)))) %>%
  mutate(across(all_of(paste0("<", newBreaks)), ~ as.factor(.x)))



# Pivot Wider to Create Binary Data ---------------------------------------

for (column_name in colnames(animals)) {
  if (is.factor(animals[[column_name]])) {
    animals <- animals %>%
      pivot_wider(names_from = column_name,
                  names_sort = TRUE,
                  values_from = column_name,
                  values_fn = ~1, 
                  values_fill = 0)
  }
}



# Find Occurrence Count by Solo Variables ---------------------------------

data1 <- animals %>%
  group_by(Label) %>%
  summarise(across(-c(Name), sum)) %>%
  complete(Label) %>% 
  select(-Label, -Legs) %>% 
  t() %>%
  data.frame() %>% 
  rename(NEG = X1, 
         POS = X2) %>% 
  mutate(percNEG = NEG/(NEG + POS),
         percPOS = POS/(NEG + POS),
         importPerc = ifelse(is.finite(pmax(percNEG, percPOS)),
                             pmax(percNEG, percPOS), NA),
         percRank = rank(-importPerc, ties.method = "random"))

importNum <- floor((nrow(data1) - 2*length(newBreaks) + (length(newBreaks) + 1))/2)

# animals2 <- animals %>% 
#   select(Name, Label, rownames(data1 %>% filter(percRank > importNum)))
notImportant <- colnames(animals %>%
                           select(Name,
                                  Label,
                                  rownames(data1 %>%
                                             filter(percRank > importNum))))

# combinations2 <- combn(colnames(animals2[,-c(1,2)]),2) %>% t()
# animals2[paste(combinations2[,1],"∧",combinations2[,2])] <- NA



# Creates Subset of Paired Data --------------------------------------------

combinations2 <- expand.grid(notImportant[-c(1,2)], colnames(animals[,-c(1,2,3)]),
                             stringsAsFactors = FALSE) %>%
  filter(Var1 != Var2)

animals2 <- animals[,c(1,3)]
animals2[paste(combinations2$Var1,"∧", combinations2$Var2)] <- NA

combn2 <- function(columnName,dataSet) {
  columnsWanted <- str_split(columnName, " ∧ ", simplify = TRUE)
  firstCol <- columnsWanted[1]
  secondCol <- columnsWanted[2]
  as.numeric(dataSet[[firstCol]] & dataSet[[secondCol]])
}



data2 <- animals2 %>%
  mutate(across(all_of(paste(combinations2[,1],"∧",combinations2[,2])), 
                ~ combn2(toString(cur_column()),animals))) %>%
  select(-Name) %>%
  group_by(Label) %>% 
  summarise(across(everything(), sum)) %>% 
  complete(Label) %>%
  select(-Label) %>% 
  t() %>%
  data.frame() %>% 
  rename(NEG = X1, 
         POS = X2) %>% 
  filter(!(NEG == POS & NEG == 0)) %>%
  mutate(percNEG = NEG/(NEG + POS),
         percPOS = POS/(NEG + POS),
         importPerc = ifelse(is.finite(pmax(percNEG, percPOS)),
                             pmax(percNEG, percPOS), NA),
         percRank = rank(-importPerc, ties.method = "random"))




 

# Jes Code which Isn't Important Anymore ----------------------------------






combinations1 <- combn(colnames(original[,-c(1,ncol(original))]),1) %>% t()
combinations2 <- combn(colnames(original[,-c(1,ncol(original))]),2) %>% t()
combinations3 <- combn(colnames(original[,-c(1,ncol(original))]),3) %>% t()


factorized[paste(combinations2[,1],"∧",combinations2[,2])] <- NA
factorized[paste(combinations3[,1],"∧",combinations3[,2],"∧",combinations3[,3])] <- NA


combn2 <- function(columnName,dataSet) {
  columnsWanted <- str_split(columnName, " ∧ ", simplify = TRUE)
  firstCol <- columnsWanted[1]
  secondCol <- columnsWanted[2]
  paste(dataSet[[firstCol]],"∧",dataSet[[secondCol]])
}

combn3 <- function(columnName,dataSet) {
  columnsWanted <- str_split(columnName, " ∧ ", simplify = TRUE)
  firstCol <- columnsWanted[1]
  secondCol <- columnsWanted[2]
  thirdCol <- columnsWanted[3]
  paste(dataSet[[firstCol]],"∧",dataSet[[secondCol]],"∧",dataSet[[thirdCol]])
}
 
fullCombinations <- factorized %>%
  mutate(across(all_of(paste(combinations2[,1],"∧",combinations2[,2])), ~ combn2(toString(cur_column()),factorized))) %>%
  mutate(across(all_of(paste(combinations3[,1],"∧",combinations3[,2],"∧",combinations3[,3])), ~ combn3(toString(cur_column()),factorized)))

pivoted <- fullCombinations %>%
  mutate(across(.cols = -c(Name, Label),
                .fns = function(x) as.factor(x)))

for (column_name in colnames(pivoted)) {
  if (is.factor(pivoted[[column_name]])) {
    pivoted <- pivoted %>%
      distinct %>% 
      pivot_wider(names_from = column_name,
                  names_sort = TRUE,
                  values_from = column_name,
                  values_fn = ~1, 
                  values_fill = 0,
                  names_repair = "minimal")
  }
}

bigdata <- pivoted %>%
  group_by(Label) %>%
  summarise(across(-c(Name), ~ sum(.x))) %>% 
  complete(Label) %>% 
  select(-Label) %>%
  t() %>% 
  data.frame() 

colnames(bigdata) <- c('NEG','POS')

bigdata <- bigdata %>% 
  mutate(ratioPN = POS/NEG,
         ratioNP = NEG/POS)  %>% 
  # filter(is.finite(ratioPN),
  #        is.finite(ratioNP)) %>%
  mutate(importance = pmax(ratioPN, ratioNP))
