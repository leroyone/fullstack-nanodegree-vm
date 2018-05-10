# "Database code" for the DB Forum.

import datetime
import psycopg2
import bleach

POSTS = [("This is the first post.", datetime.datetime.now())]

def get_posts():
  theDB = psycopg2.connect("dbname=forum")
  cursor = theDB.cursor()
  cursor.execute("select content, time from posts order by time desc")
  results = cursor.fetchall()
  theDB.close()
  return results

def add_post(content):
  content = bleach.clean(content)
  theDB = psycopg2.connect("dbname=forum")
  cursor = theDB.cursor()
  cursor.execute("insert into posts values (%s)", (content,))
  theDB.commit()