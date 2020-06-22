import os
from flask import Flask, request
from flask.templating import render_template
import sqlite3
import time
import random
import redis

app = Flask(__name__)
port = int(os.getenv("PORT", 5000))

redisName = "hengchao.redis.cache.windows.net"
redisPort = 6380
password = "b1B4BSOWqY9cDv4q8c7OvbJafEB4CRAHfrV819RdLZQ="


def getData():
    conn = sqlite3.connect('data/test.db')
    print("Open database successfully")
    c = conn.cursor()
    starttime = time.time()
    c.execute("select * from all_month")
    data = c.fetchall()
    conn.close()
    endtime = time.time()
    timediff = endtime - starttime
    return data, timediff


def getIdList():
    conn = sqlite3.connect('data/test.db')
    print("Open database successfully")
    c = conn.cursor()
    starttime = time.time()
    c.execute("select id from all_month")
    idList = c.fetchall()
    conn.close()
    endtime = time.time()
    timediff = endtime - starttime
    return idList, timediff


random_id = []
random_sql = "0"
mags = []

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_redirect():
    idList, _ = getIdList()
    data, timediff = getData()
    global random_sql
    global random_id
    global mags
    if request.method == 'POST':
        if request.form['point'] == 'one':
            if request.form['sql_number'] == "":
                return render_template('home.html', result=data, k=len(data), time=timediff)
            sum_time = 0
            sql_number = int(request.form['sql_number'])
            if request.form['sql_number'] == '':
                sql_number = 3
            sub_data = []
            ids = []
            r = redis.StrictRedis(redisName, port=redisPort, password=password, ssl=True)
            starttime = time.time()
            for i in range(0, sql_number):
                index = random.randint(0, len(idList))
                tmpId = idList[index]
                ids.append(tmpId)
                conn = sqlite3.connect('data/test.db')
                c = conn.cursor()
                c.execute("select * from all_month where id = ?", (tmpId))
                row = c.fetchall()[0]
                sub_data.append(row)
                conn.close()
                # endtime = time.time()
                tmpId = tmpId[0]
                if r.exists(tmpId) == 0:
                    for i in row[1:]:
                        r.rpush(tmpId, str(i))
                # sum_time += endtime - starttime
                # global random_id
                random_id = ids
            endtime = time.time()
            sum_time = endtime - starttime
            print(1, len(random_id) > 0, random_sql == '')
            return render_template('home.html', result=sub_data, k=len(sub_data), time=sum_time, mags1=ids,
                                   len=sql_number, alartOne=0 if random_id is None else 1,
                                       alartTwo=0 if random_sql == '' else 1)
        if request.form['point'] == 'more':
            sum_time = 0
            if request.form['maxMag'] == '' and request.form['minMag'] == '':
                return render_template('home.html', result=data, k=len(data), time=timediff,)
            if request.form['maxMag'] == '':
                maxMag = 10
            else:
                maxMag = int(request.form['maxMag'])
            if request.form['minMag'] == '':
                minMag = 0
            else:
                minMag = int(request.form['minMag'])
            # if request.form['sql_number'] == '':
            #     sql_number = 3
            # else:
            #     sql_number = int(request.form['sql_number'])
            mags = [minMag, maxMag]
            r = redis.StrictRedis(redisName, port=redisPort, password=password, ssl=True)

            starttime = time.time()
            conn = sqlite3.connect('data/test.db')
            c = conn.cursor()
            c.execute("select * from all_month where mag< ? and ? <=mag", (maxMag, minMag))
            sub_data = c.fetchall()
            conn.close()
            endtime = time.time()
            if r.exists("select * from all_month where mag <" + str(maxMag) + " and " + str(minMag) + " <=mag") == 0:
                for row in sub_data[:100]:
                    r.hset("select * from all_month where mag <" + str(maxMag) + " and " + str(minMag) + " <=mag",
                           row[0], str(row[1:]))
            sum_time += endtime - starttime
            # global random_sql
            random_sql = "select * from all_month where mag <" + str(maxMag) + " and " + str(minMag) + " <=mag"
            print(2, len(random_id) > 0, random_sql == '')

            return render_template('home.html', result=sub_data, k=len(sub_data), time=sum_time, mags3=mags, len=2,
                                   alartOne=0 if random_id is None else 1,
                                   alartTwo=0 if random_sql == '' else 1)
        if request.form['point'] == 'oneredis':
            sum_time = 0
            if random_id is None:
                return render_template('home.html', result=data, k=len(data), time=timediff, alartOne=1, alartTwo=0)
            r = redis.StrictRedis(redisName, port=redisPort, password=password, ssl=True)
            sub_data = []
            # global random_id
            print(random_id)
            starttime = time.time()
            for tmpId in random_id:
                if r.exists(tmpId[0]) == 1:
                    sub_data.append(r.lrange(tmpId[0], 0, 30))
            endtime = time.time()
            sum_time += endtime - starttime
            print(3, len(random_id) > 0, random_sql == '')

            return render_template('home.html', result=sub_data, k=len(sub_data), time=sum_time, mags2=random_id,
                                   len=len(random_id), alartOne=0 if random_id is None else 1,
                                       alartTwo=0 if random_sql == '' else 1)
        if request.form['point'] == 'tworedis':
            r = redis.StrictRedis(redisName, port=redisPort, password=password, ssl=True)
            sub_data = []
            if random_sql == '':
                return render_template('home.html', result=data, k=len(data), time=timediff, alart=0)
            if r.exists(random_sql) == 1:
                map = r.hgetall(random_sql)  # map {id, str}
                idList = map.keys()
                for id in idList:  #
                    row = str(map[id])
                    row.replace("'", '')
                    tmp_data = row.split(',')
                    tmp_data[0].replace("b", "")
                    for i in tmp_data:
                        i.replace("\'", "")
                    sub_data.append(tmp_data)
                    # print(sub_data)
                    print(4, len(random_id) > 0, random_sql == '')

                return render_template('home.html', result=sub_data, k=len(sub_data), time=timediff, mags4=mags,
                                       len=2, alartOne=0 if random_id is None else 1,
                                       alartTwo=0 if random_sql == '' else 1)
        else:
            print(5, len(random_id) > 0, random_sql == '')

            return render_template('home.html', result=data, k=len(data), time=timediff, alartOne=0 if random_id is None else 1,
                                       alartTwo=0 if random_sql == '' else 1)
    else:
        print(6, len(random_id) > 0, random_sql == '')

        return render_template('home.html', result=data, k=len(data), time=timediff, alartOne=0 if random_id is None else 1,
                                       alartTwo=0 if random_sql == '' else 1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
