import requests , sys ,json
import ssl
# import pymysql
# import dbSettings

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
    print(html.content.decode('utf-8'))
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
    for item in ["city","township","province","district"]:
        if addressComponent[item] == []:
            addressComponent[item] = ""
    if addressComponent["country"] == []:
        addressComponent = "境外"
        print(addressComponent)
    else:
        print(addressComponent["province"]+"|"+addressComponent["city"]+"|"+addressComponent["district"]+"|"+addressComponent["township"]+"|"+formatted_address)
     

if __name__ == "__main__":
    # db = dbSettings.db_connect()
    # cursor = db.cursor()
    # cursor.execute("SELECT id,listingid,lat,lng FROM `detail` order by RAND() limit 100")
    # results = cursor.fetchall()
    # for row in results:
    #     print(decodeLocation(row["lng"],row["lat"]))
    decodeLocation(127.5227400000 , 50.2704700000)





