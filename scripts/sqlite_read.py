import sqlite3
import sys

slack_id = sys.stdin.readline().rstrip()
con = sqlite3.connect('sample.db')
cursor = con.cursor()

cursor.execute('SELECT * FROM data_set')
for row in cursor:
    if row[1] == slack_id:
        print(row[2])
