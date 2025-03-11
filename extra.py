def baimenmotak_lortu(mysql):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM baimenmotak''')
    results = cur.fetchall()
    return results