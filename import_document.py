import mysql.connector

db_scrap = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="asdasd",
  database="rumahginjal"
)

cursor = db_scrap.cursor()

query = ("SELECT content FROM detail_news")

cursor.execute(query)

contents = cursor.fetchall()

db_stemm = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="asdasd",
    database="stki_stemming"
)

cursor2 = db_stemm.cursor()
for (content) in contents:
    escaped_content = content[0].replace("'", "\\\'")
    query = "INSERT INTO dokumen (text) VALUES ('%s')"  % (escaped_content)
    cursor2.execute(query)

db_stemm.commit()

print("import database selesai")
