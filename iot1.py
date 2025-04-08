import time,random,sqlite3

LIMIT=35.0

conn=sqlite3.connect("teju.db")
cursor=conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS readings(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               times REAL,
               temp REAL,
               hum REAL,
               )''')
conn.commit()

def read_sensor():
    temp=round(random.uniform(20,45),2)
    hum=round(random.uniform(30,90),2)
    return temp,hum

while True:
    temp,hum=read_sensor()
    times=time.time()

    cursor.execute('''
                    INSERT INTO readings(times,temp,hum)
                   values(?,?,?)''',(times,temp,hum))
    conn.commit()

    print(f"Logged: tempature={temp}c,humidity={hum}%")

    if temp>LIMIT:
        print("alert HIGH TEMP!!!!")

    time.sleep(2)



# 
# ranjit2798