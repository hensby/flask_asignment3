import sqlite3
from datetime import datetime, timedelta

import redis


def test1():
    # dis = hello.get_distance_hav(34.0522342, -118.2436849)
    # print(dis)

    # conn = sqlite3.connect('test.db')
    # print("Open database successfully")
    # c = conn.cursor()
    # c.execute("select * from all_month")
    # # c.executescript("INSERT INTO distance VALUES ('nc73409661',1212,1223,232);")
    # # "select * from all_month"
    # data = c.fetchall()
    # conn.close()

    conn = sqlite3.connect('data/test.db')
    print("Open database successfully")

    c = conn.cursor()
    # sql = "update all_month set gap = '2' where id = 'ak0207rpmj1w'"
    # c.execute(sql)
    c.execute("select * from all_month where mag< ? and ? <=mag", (1, 0))
    idList = c.fetchall()
    # data = []
    # for id in idList:
    #     c.execute("select * from all_month where id = ?", (id))
    #     data.append(c.fetchall())
    print(idList)
    # conn.commit()
    conn.commit()
    conn.close()


#     (id, distance_from_Arlington, distance_from_Anchorage, distance_from_Dallas)


def test2():
    part = []
    max = []
    max_mag = 0
    conn = sqlite3.connect('test.db')
    print("Open database successfully")
    c = conn.cursor()
    c.execute("select id from gapNull ")
    idList = c.fetchall()
    for id in idList:
        c.execute("select * from all_month where id = ?", (id))
        part.append(c.fetchall()[0]);
    # for i in part:
    #     if float(i[5]) > max_mag:
    #         if len(max) != 0:
    #             max.pop(0)
    #         max.append(i)
    #         max_mag = float(i[5])
    # c.execute(
    #     "select * from (select * from all_month left join distance on all_month.id = all_month.id) where distance_from_Dallas <= 500 order by mag DESC limit 1")
    # idList = c.fetchall()
    print(part)


def test3():
    conn = sqlite3.connect('data/test.db')
    print("Open database successfully")
    c = conn.cursor()
    c.execute("select id from all_month where gap is null")
    # c.executescript("INSERT INTO distance VALUES ('nc73409661',1212,1223,232);")
    # "select * from all_month"
    idList = c.fetchall()
    conn.close()

    conn = sqlite3.connect('test.db')
    print("Open database successfully")
    for id in idList:
        sql = "INSERT INTO gapNull VALUES (?)"
        c = conn.cursor()
        c.execute(sql, (id))
        conn.commit()
    conn.close()


def test4():
    r = redis.StrictRedis("hengchao.redis.cache.windows.net", port=6380,
                          password="b1B4BSOWqY9cDv4q8c7OvbJafEB4CRAHfrV819RdLZQ=", ssl=True)
    # r.set("2", "200")
    # print(r.get("2"))
    # print(r.exists("select * from all_month where all_month.mag>0"))
    print(r.exists('ak0207yg14f6') == 0)


if __name__ == '__main__':
    # today = datetime.today()
    # endDate = datetime(2030, 1, 1)
    # item = ["2020-06-15T22:21:16.200Z"]
    #
    # print(today - datetime.strptime(item[0:10], '%Y-%m-%d') <= timedelta(days=1))
    test1()
