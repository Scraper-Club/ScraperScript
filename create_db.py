import sqlite3
from db import DATABASE_NAME

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE search_urls (url_id INT)''')
cursor.execute('''CREATE TABLE target_urls (url_id INT, url TEXT, status INT, result TEXT)''')
cursor.execute('''CREATE TABLE companies (name TEXT, location TEXT, description TEXT, website TEXT, employees TEXT)''')
conn.commit()
conn.close()
