import psycopg2

def query_one():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute('''select articles.title, count(*) as views
                 from articles, log
                 where log.path like '%' || articles.slug
                 group by articles.title
                 order by views desc''')
    return c.fetchall()
    db.close()

def query_two():

results1 = query_one()
for row in results1:
    print "\"{}\" - {} views".format(row[0], row[1])
