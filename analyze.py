#!/usr/bin/env python

import psycopg2

def connect(dbname):
    try:
        db = psycopg2.connect("dbname={}".format(dbname))
        cursor = db.cursor()
        return db, cursor
    except:
        db = None;
        print("Unable to connect to {} database.".format(dbname))

# Connect to news db and start cursor
db, cursor = connect("news")

# What are the most popular three articles of all time?
def three_most_popular_articles():
    cursor.execute('''select title, count(*) as views
        from article_views
        group by title
        order by views desc
        limit 3''')
    return cursor.fetchall()


# Who are the most popular article authors of all time?
def most_popular_authors():
    cursor.execute('''select authors.name, count(*) as views
        from authors, article_views
        where authors.id = article_views.author
        group by authors.name
        order by views desc''')
    return cursor.fetchall()


# On which days did more than 1% of requests lead to errors?
def most_daily_errors():
    cursor.execute('''select * from error_rate where error_percent > 1''')
    return cursor.fetchall()


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
if (db):
    db.close()
