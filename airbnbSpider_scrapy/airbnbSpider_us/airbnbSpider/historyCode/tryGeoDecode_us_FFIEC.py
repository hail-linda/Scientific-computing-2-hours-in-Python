import requests , sys ,json, time
import ssl
import pymysql
import dbSettings
import threading
from tqdm import tqdm

def url_request(Lng,Lat):
    url = 'https://geomap.ffiec.gov/arcgiswa/rest/services/ffiec/Tract_2017/MapServer/0/query?'+ \
    'f=json&where=&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry={"x":'+str(Lng*100000)+',"y":'+str(Lat*100000)+','+ \
    '"spatialReference":{"wkid":102100,"latestWkid":3857}}&geometryType=esriGeometryPoint&inSR=102100&'+ \
    'outFields=TRACT,STATE_FIPS,CNTY_FIPS&outSR=102100'
    # print(url)

    return url

def geoDecode(listingId,Lng,Lat):
    html = requests.get(url = url_request(Lng,Lat))
    res = json.loads(html.content)
    locationInfor = {}
    if "features" in res:
        if len(res['features']) > 0 :
            attributes = {}
            attributes["sStateCode"] = res["features"][0]["attributes"]["STATE_FIPS"]
            attributes["sCountyCode"] = res["features"][0]["attributes"]["CNTY_FIPS"]
            attributes["sTractCode"] = res["features"][0]["attributes"]["TRACT"]
            attributes["iCensusYear"] = "2021"
            data = '{sStateCode: "'+attributes["sStateCode"]+'", sCountyCode: "'+attributes["sCountyCode"]+'", sTractCode: "'+attributes["sTractCode"]+'", iCensusYear: "2021"}'
            # print(data)
            url = "https://geomap.ffiec.gov/FFIECGeocMap/GeocodeMap1.aspx/GetMSAStCntyNames"
            headers = {
                        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Content-Type': 'application/json; charset=utf-8'
                        }
            # print(json.dumps(attributes),url)
            html = requests.post(url = url,data = data , headers = headers)
            res = json.loads(html.content)
            if "d" in res:
                locationInfor = res["d"]
                del locationInfor["__type"]
                del locationInfor["ExtensionData"]
                del locationInfor["intRC"]
                for k in locationInfor:
                    locationInfor[k] = locationInfor[k].strip()
                tqdm.write(str(locationInfor))
    if locationInfor == {} :
        # print("decodeFalse",listingId,Lng,Lat)
        dbInsert(listingId,Lng,Lat,None)
    else:
        dbInsert(listingId,Lng,Lat,locationInfor)
    sm.release()

def dbInsert(listingId,Lng,Lat,locationInfor):
    db = dbSettings.db_connect()
    cursor = db.cursor()
    if locationInfor == None:
        sql = '''
    INSERT INTO `airbnb_scrapy_us`.`listing_location_us` 
    (`listingid`,`lng`,`lat`,`country`) 
    VALUES ('{}',{},{},'abroad')
    '''.format(listingId,Lng,Lat)
    else :
        sql = '''
    INSERT INTO `airbnb_scrapy_us`.`listing_location_us` 
    (`listingid`,`lng`,`lat`,`country`,`state`,`city`,`MSACode`,`MSAName`) 
    VALUES ('{}',{},{},'{}','{}','{}','{}','{}');
    '''.format(listingId,Lng,Lat,"US",locationInfor['sStateName'],locationInfor['sCountyName'],locationInfor['sMSACode'],locationInfor['sMSAName'])
    cursor.execute(sql)
    db.commit()

sm = threading.Semaphore(1000)

if __name__ == "__main__":
    db = dbSettings.db_connect()
    cursor = db.cursor()
    sql = '''
    SELECT `listingId` FROM `listing_location_us`
    '''
    cursor.execute(sql)
    results = cursor.fetchall()

    existLocation = [row['listingId'] for row in results]
    existLocation = set(existLocation)
    print(len(existLocation))

    sql = '''
    SELECT `detail_us`.`listingId`,
        `detail_us`.`Lng`,
        `detail_us`.`Lat`
    FROM `detail_us`
    '''
    cursor.execute(sql)
    results = cursor.fetchall()
    print(len(results))
    rows = []
    for row in results:
        if not row['listingId'] in existLocation:
            rows.append(row)

    results = rows
    del rows
    with tqdm(total=len(results)) as pbar:
        pbar.set_description('Processing:')
        for row in results:
            if row['listingId'] in existLocation:
                continue
            sm.acquire()
            pbar.update(1)
            # time.sleep(0.002)
            # print("start:",row['listingId'],row['Lng'],row['Lat'])
            thread_run = threading.Thread(target=geoDecode , args=(row['listingId'],row['Lng'],row['Lat']))
            thread_run.start()

