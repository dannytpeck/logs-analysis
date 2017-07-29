# Log Analysis Tool
Runs three preset reports from a database of news articles.

## Before Running
First, clone the Repo and change to the new directory.
```
git clone https://github.com/dannytpeck/logs-analysis.git
cd logs-analysis
```
Next, download [this file](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and unzip to the same directory the repo's in, then set up the DB and create the required Views.
```
psql -d news -f newsdata.sql
psql news
create view article_views as
  select title, author, log.time from articles, log
  where log.path like '%' || articles.slug;
create view error_rate as
  select errors.date, round((errors::numeric / requests::numeric * 100), 1) as error_percent
  from (select time::date as date, count(*) as errors
    from log where status != '200 OK' group by date) as errors,
    (select time::date as date, count(*) as requests
    from log group by date) as requests
  where errors.date = requests.date
  order by error_percent desc;
```

## Running the App
Finally, run the app (Python 2.7 required)
```
python analyze.py
```
