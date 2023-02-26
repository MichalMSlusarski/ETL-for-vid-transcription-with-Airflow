library(data.table)
library(readr)
library(rtweet)

#LOGIN PROCEDURE

app_name = readline("Enter app_name: ")
api_key <- readline("Enter api_key: ")
api_secret_key <- readline("Enter api_secret_key: ")
access_token <- readline("Enter access_token: ")
access_secret <- readline("Enter access_secret: ")

token <- create_token(
  app = app_name,
  consumer_key = api_key,
  consumer_secret = api_secret_key,
  access_token = access_token,
  access_secret = access_secret)

token
t <- Sys.time() #202112310001 #202112312359

#TWEET RETRIVAL

query <- readline("Search query: ")

tweetTable <- search_tweets(query, n = 100000, type = "recent", include_rts = FALSE, retryonratelimit = F)

#SAVE TO CSV

file_name = readline("Enter desired file name: ")

write_as_csv(tweetTable, file_name, prepend_ids = TRUE, na = "", fileEncoding = "UTF-8") #tweets are encoded with utf-8
