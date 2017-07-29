#!/usr/bin/env python2.7

import psycopg2

# Connect to news db and start cursor
db = psycopg2.connect("dbname=news")
c = db.cursor()


# What are the most popular three articles of all time?
def three_most_popular_articles():
    c.execute('''select title, count(*) as views
        from article_views
        group by title
        order by views desc
        limit 3''')
    return c.fetchall()


# Who are the most popular article authors of all time?
def most_popular_authors():
    c.execute('''select authors.name, count(*) as views
        from authors, article_views
        where authors.id = article_views.author
        group by authors.name
        order by views desc''')
    return c.fetchall()


# On which days did more than 1% of requests lead to errors?
def most_daily_errors():
    c.execute('''select * from error_rate where error_percent > 1''')
    return c.fetchall()


# Print the three queries, nicely formatted
print
for row in three_most_popular_articles():
    print "\"{}\" - {} views".format(row[0], row[1])
print
for row in most_popular_authors():
    print "{} - {} views".format(row[0], row[1])
print
for row in most_daily_errors():
    print "{:%B %d, %Y} - {}% errors".format(row[0], row[1])
print


# Close db now that we're done with it
db.close()
