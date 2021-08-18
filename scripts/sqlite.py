import sqlite3

con = sqlite3.connect('sample.db', isolation_level=None)
cursor = con.cursor()
cursor.execute("CREATE TABLE data_set(id, slack_id, github_name)")
data = [
    (1, "U01JTK31B2N", "kobakobashu"),
    (2, "U026HP6S08K", "tkkawa"), # example
    (3, "0123", "ryuji0123") # example
]
cursor.executemany("INSERT INTO data_set VALUES(?,?,?)", data)

cursor.execute("select * from data_set")
for row in cursor:
    print(row[0], row[1], row[2])

con.close()
