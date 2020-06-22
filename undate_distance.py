import re
import sqlite3

import redis


def update_sql():
    conn = sqlite3.connect('data/test.db')
    print("Open database successfully")
    c = conn.cursor()
    c.execute("select * from all_month")
    # c.executescript("INSERT INTO distance VALUES ('nc73409661',1212,1223,232);")
    # "select * from all_month"
    data = c.fetchall()
    conn.close()

    conn = sqlite3.connect('test.db')
    print("Open database successfully")
    for row in data:
        id = str(row[0])
        if re.findall("[0-9]*", row[7], flags=0):
            distance = re.findall("[0-9]*", row[7], flags=0)[0]
        else:
            distance = -1
        if (re.findall("of .*?,", row[7], flags=0)):
            city = re.findall("of .*?,", row[7], flags=0)[0].replace("of ", "").replace(",", "")
        else:
            city = ""
        if row[2]:
            mag = row[2]
        else:
            mag = -1

        # print(id, city, distance)
        sql = "INSERT INTO distance VALUES (?, ?, ?, ?)"
        c = conn.cursor()
        c.execute(sql, (id, city, distance, mag))
        conn.commit()
    conn.close()


def update_redis():
    # pool = redis.ConnectionPool"hengchao.redis.cache.windows.net", port=6380, password="b1B4BSOWqY9cDv4q8c7OvbJafEB4CRAHfrV819RdLZQ=", ssl=True)
    # r = redis.Redis(connection_pool=pool)
    r = redis.StrictRedis("hengchao.redis.cache.windows.net", port=6380,
                          password="b1B4BSOWqY9cDv4q8c7OvbJafEB4CRAHfrV819RdLZQ=", ssl=True)
    conn = sqlite3.connect('data/test.db')
    print("Open database successfully")
    c = conn.cursor()
    c.execute("select * from all_month")
    data = c.fetchall()
    conn.close()

    for row in data:
        # print(row[0])
        for i in row[1:]:
            # print(i)
            r.rpush(row[0], str(i))
    # newRow = r.get(row[0])
    # print(r.lrange(row[0], 0, 100))
    # newRow.replace(" ", "")
    # print(newRow)
    # print(newRow)
    # r.delete(row[0])



if __name__ == '__main__':
    # update_sql()
    update_redis()

    # dis = hello.get_distance_hav(34.0522342, -118.2436849)
    # print(dis)

#     (id, distance_from_Arlington, distance_from_Anchorage, distance_from_Dallas)
