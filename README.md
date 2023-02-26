# Basic-data-analysis-in-Python
I translated some of my R tasks to Python, adding some features along the way

This is a Python equivalent of the code in initially wrote in R. For example:
The equivalent of the filter() function from R is done using boolean indexing in Python. 
The equivalent of the distinct() function is done using the drop_duplicates() function in pandas. 
The equivalent of the write_as_csv() function is the to_csv() function in pandas.
The difference here, is that I didn't enclose it in a function.

The data required for this task were gathered using rtweet package for R language via direct call to Twitter API. I find the equivalent Python implementation to be surprisingly cumbersome in comparison. Decided not to include it here.

The steps are as follows:

#### 0. Load from csv
```
path = input("Enter file path: ")
obs = pd.read_csv(path)
```
#### 1. Select needed dates.
```
dateTo = input("Enter the date to filter by: ")
obs = obs[obs['created_at'] < dateTo]
```

#### 1.6 Remove retweets
```
obs = obs[obs['is_retweet'] == False]
```

#### 2. Remove duplicated
```
obs = obs.drop_duplicates(subset=['status_id'], keep='first')
```

#### 2.25 Filter by favorite_count count and retweet_count

```
min_favorite_count = input("Enter the minimum favorite count: ")
min_retweet_count = input("Enter the minimum retweet count: ")
min_favorite_count = int(min_favorite_count)
min_retweet_count = int(min_retweet_count)

obs = obs[(obs['favorite_count'] > min_favorite_count) | (obs['retweet_count'] > min_retweet_count)]
```

#### 2.3 Select distinct by text so that there are no two identical tweets. 
It's not the same as removing duplicates, as here we can focus solely on text (if someone copied someone's else tweet or retweeted it)

```
obs = obs.drop_duplicates(subset=['text'], keep='first')

```

#### 2.4 Select distinct by users

```
obs = obs.drop_duplicates(subset=['user_id'], keep='first')

```

#### 3. Select needed variables

```
obs = obs[['user_id', 'status_id', 'created_at', 'screen_name', 'text']]

```

#### 4. Export to a desired csv file

```
file_title = input("Enter desired file name: ") + '.csv'
obs.to_csv(file_title, index=False, encoding='UTF-8')
print(file_title + ' saved successfully')

```
