import sqlite3

conn = sqlite3.connect('carBase.db')
c = conn.cursor()

c.execute("""Create TABLE NissanAltima(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    contact TEXT,
    year TEXT,
    price TEXT,
    date TEXT,
    urls TEXT
)""")

c.execute("INSERT INTO NissanAltima VALUES (?,?,?,?,?,?,?)",(None,'jose','instagram','2005','5000','10-12-2022','https://res.cloudinary.com/dkqd7276t/image/upload/v1678852956/icons.png.png https://res.cloudinary.com/dkqd7276t/image/upload/v1678852957/dragon.png.png'))
c.execute("INSERT INTO NissanAltima VALUES (?,?,?,?,?,?,?)",(None,'jesus','twitter','2005','4000','11-19-2022','https://res.cloudinary.com/dkqd7276t/image/upload/v1678852956/icons.png.png https://res.cloudinary.com/dkqd7276t/image/upload/v1678852957/dragon.png.png'))
c.execute("INSERT INTO NissanAltima VALUES (?,?,?,?,?,?,?)",(None,'joe','facebook','2004','3500','12-23-2022','https://res.cloudinary.com/dkqd7276t/image/upload/v1678852956/icons.png.png https://res.cloudinary.com/dkqd7276t/image/upload/v1678852957/dragon.png.png'))

conn.commit()

for row in c.execute("SELECT * FROM NissanAltima"):
    print(row)