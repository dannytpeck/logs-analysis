# Log Analysis Tool
Runs a set of 3 pre-set reports from the database.

## Before Running
```
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
Clone the github repository and run using Python 2.7
```
git clone https://github.com/dannytpeck/logs-analysis.git
cd logs-analysis
python analyze.py
```
