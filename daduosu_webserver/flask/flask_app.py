from flask import Flask, request, render_template
import json, time
import dbSettings
app = Flask(__name__)
app.debug = True

db = dbSettings.db_connect()
cursor = db.cursor()

@app.route('/api/v1/')
def index():
    return "hello flask!"

@app.route('/api/v1/stat/')
def stat():
    sql = "SELECT * from `proxypool` WHERE `state` != 'del'"
    cursor.execute(sql)
    db.commit()
    results = cursor.fetchall()
    return str([row['ip'] for row in results])

@app.route('/api/v1/listing/')
def listing():
    sql = "SELECT * from `houselist` limit 100"
    cursor.execute(sql)
    db.commit()
    results = cursor.fetchall()
    return str([row['house_id'] for row in results])

@app.route('/api/v1/detail/<listingid>/<item>')
def detail_item(listingid,item):
    sql = "SELECT * from `detail` where `listingid` = "+listingid
    cursor.execute(sql)
    db.commit()
    results = cursor.fetchall()
    return str(results[0][item])


@app.route('/api/v1/detail/<listingid>')
def detail(listingid):
    sql = "SELECT * from `detail` where `listingid` = "+listingid
    cursor.execute(sql)
    db.commit()
    results = cursor.fetchall()
    return str(results[0])

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=5005)
