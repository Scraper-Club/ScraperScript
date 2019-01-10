import sqlite3

DATABASE_NAME = 'scraper.db'
db_conn = sqlite3.connect(DATABASE_NAME)


def get_search_url():
    sql = 'SELECT * FROM search_urls'
    cur = db_conn.cursor()

    cur.execute(sql)
    return cur.fetchone()


def delete_search_url():
    sql = 'DELETE FROM search_urls'
    cur = db_conn.cursor()

    cur.execute(sql)
    db_conn.commit()


def save_search_url(url_id):
    sql = 'INSERT INTO search_urls VALUES (?)'
    cursor = db_conn.cursor()

    cursor.execute(sql, (url_id,))
    db_conn.commit()


def save_target_url(target_url_id, target_url):
    sql = 'INSERT INTO target_urls VALUES (?,?,?,?)'
    cursor = db_conn.cursor()

    cursor.execute(sql, (target_url_id, target_url, 0, None))
    db_conn.commit()


def get_scraped_target_urls():
    sql = 'SELECT * FROM target_urls WHERE status = 1'
    cursor = db_conn.cursor()

    cursor.execute(sql)
    return cursor.fetchall()


def get_not_scraped_target_urls():
    sql = 'SELECT * FROM target_urls WHERE status = 0'
    cursor = db_conn.cursor()

    cursor.execute(sql)
    return cursor.fetchall()


def update_target_url_result(target_url_id, result):
    sql = 'UPDATE target_urls SET status = 1, result = ? WHERE url_id = ?'
    cursor = db_conn.cursor()

    cursor.execute(sql, (result, target_url_id,))
    db_conn.commit()


def save_company(name, location, description, website, employees):
    sql = 'INSERT INTO companies VALUES (?,?,?,?,?)'
    cursor = db_conn.cursor()

    cursor.execute(sql, (name, location, description, website, employees,))
    db_conn.commit()
