import requests , sys ,json
import ssl
import pymysql
import dbSettings

def getLocation(lat,lng):
    lat = str(lat) # 124.1116
    lng = str(lng) # 41.68295
    location = lat+","+lng
    host = 'https://regeo.market.alicloudapi.com'
    path = '/v3/geocode/regeo'
    method = 'GET'
    appcode = 'f1dd5539a8fe4ab59d108e3d8d23f06b'
    querys = 'batch=false&extensions=base&location={}&output=json&radius=1000'.format(location)
    bodys = {}
    url = host + path + '?' + querys

    headers = {'Authorization': 'APPCODE ' + appcode}
    html = requests.get(url,headers = headers)
    res = json.loads(html.content)
    if res['status'] == 1: 
        return html.content.decode('utf-8')
    else :
        return html.content.decode('utf-8')

def decodeLocation(lat,lng):
    res = json.loads(getLocation(lat,lng))
    formatted_address = res["regeocode"]["formatted_address"]
    addressComponent = res["regeocode"]["addressComponent"]
    
    if res["regeocode"]["formatted_address"] == []:
        formatted_address = ""
    addressComponent["formatted_address"] = formatted_address
    for item in ["city","township","province","district"]:
        if addressComponent[item] == []:
            addressComponent[item] = ""
    if addressComponent["country"] == []:
        formatted_address = "境外"
        print(formatted_address)
    else:
        print(addressComponent["province"]+"|"+addressComponent["city"]+"|"+addressComponent["district"]+"|"+addressComponent["township"]+"|"+addressComponent["formatted_address"])
    addressComponent["formatted_address"] = formatted_address
    return addressComponent

def batchGeoEncode(bias,existLocation):
    db = dbSettings.db_connect()
    cursor = db.cursor()
    cursor.execute("SELECT id,listingid,lat,lng FROM `detail` where id between {} and {}".format(bias,bias+100))
    print("SELECT id,listingid,lat,lng FROM `detail` where id between {} and {}".format(bias,bias+100))
    results = cursor.fetchall()

    sql = "INSERT INTO `listing_location`(`listingid`, `lng`, `lat`, `formatted_address`, `province`, `city`, `district`, `township`)\
         VALUE (%s,%s,%s,%s,%s,%s,%s,%s)"

    vals = []
    count = 0
    for row in results:
        # count += 1
        # print(count)
        if row["listingid"] in existLocation:
            continue
        print(row["lng"],",",row["lat"])
        addressComponent = decodeLocation(row["lng"],row["lat"])
        vals.append((row["listingid"],row["lng"],row["lat"],addressComponent["formatted_address"],addressComponent["province"],addressComponent["city"],addressComponent["district"],addressComponent["township"]))

        # print(row["listingid"],row["lng"],row["lat"],addressComponent["formatted_address"],addressComponent["province"],addressComponent["city"],addressComponent["district"],addressComponent["township"])

    cursor.executemany(sql, vals)
    db.commit()

if __name__ == "__main__":
    db = dbSettings.db_connect()
    cursor = db.cursor()
    cursor.execute("SELECT listingId FROM `listing_location`")
    results = cursor.fetchall()
    existLocation = set([item['listingId'] for item in results])
    for i in range(0,16000):
       batchGeoEncode(i*100,existLocation)



