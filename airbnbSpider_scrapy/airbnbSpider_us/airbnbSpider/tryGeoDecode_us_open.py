import requests , sys ,json, time
import ssl
import pymysql
import dbSettings
import threading
from tqdm import tqdm
import random
class proxyPool:
    def __init__(self):
        self.proxyId = 0
        self.ip = ""
        self.table = "`proxypool_us`"
        # print("middleline-proxyPool1")
        self.db = dbSettings.db_connect()
        # print("middline-proxyPool2")
        self.cursor = self.db.cursor()

    def dbInsert(self, proxy):
        sql = "INSERT INTO "+self.table + \
            " (`ip`, `numused`, `state`) VALUES ('{}', '0', 'new')".format(proxy)
        self.cursor.execute(sql)
        self.db.commit()

    def IP(self):
        # print("\tip start\t: ",time.time())
        sql = "SELECT id,ip,cookies from "+self.table+"WHERE `state` != 'del' limit 30"
        # print("\tip sql   \t: ",time.time())
        self.cursor.execute(sql)
        # print("\tip cursor\t: ",time.time())
        self.db.commit()
        # print("\tip commit\t: ",time.time())
        results = self.cursor.fetchall()
        # print("\tip result\t: ",time.time())
        if(len(results) < 5):
            pass
            # self.get()
            time.sleep(2)
            return self.IP()
        rand = random.randint(0, len(results)-1)
        # print(results[rand]['id'],results[rand]['ip'])
        tqdm.write(str(results[rand]['id'])+" "+results[rand]['ip'])
        self.ip = results[rand]['ip']

        self.cookies = results[rand]['cookies']
        # print("self.ip",self.ip)
        self.proxyId = results[rand]['id']
        # print("\tip end\t: ",time.time())

        # sql = "UPDATE "+self.table + \
        #     " SET `numused` = `numused` + 1 WHERE `id` = " + \
        #     str(results[rand]['id'])
        # self.cursor.execute(sql)
        # self.db.commit()

        return self.IP

    def proxies(self):
        self.IP()
        # print("proxy ip:\t\t\t",self.ip)
        username = "1282255404"
        password = "123456"
        self.proxies = {
            "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": self.ip},
            "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": self.ip}
        }
        # self.proxies = " http://{}".format(self.ip)
        return self.proxies
    
    def getCookies(self):
        return self.cookies

    def get(self, num=20):
        url = "http://dps.kdlapi.com/api/getdps/?orderid=970736318449376&num={}&pt=1&format=json&sep=1&dedup=1".format(
            str(num))
        print(url)
        proxies = {"http": None, "https": None}
        html = requests.get(url, timeout=5, proxies=proxies)

        # print(html)
        res = json.loads(html.content)
        print("get proxy ", time.asctime(
            time.localtime(time.time())))
        if 'data' in res:
            res = res['data']
        else:
            print("get proxy err in data")
        count = res['count']

        if 'proxy_list' in res:
            proxys = res['proxy_list']
        else:
            print("get proxy err in proxy_list")

        for proxy in proxys:
            self.dbInsert(proxy)

    def delete(self, proxy, delReason):
        delReason = delReason.replace("'", "''")
        delReason = delReason.replace('"', '""')
        sql = "UPDATE "+self.table + \
            " SET `state` = 'del' WHERE `ip`='{}'".format(proxy)
        self.cursor.execute(sql)
        self.db.commit()
        sql = "UPDATE "+self.table + \
            " SET `delreason` = '{}' WHERE `ip`='{}'".format(
                delReason, proxy)

        print(sql)
        self.cursor.execute(sql)
        self.db.commit()


def url_request(Lng,Lat):
    url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat='+str(Lat)+'&lon='+str(Lng)+'&zoom=18&addressdetails=1&accept-language=en'
    return url

def url_headers():
    headers = {
        'Proxy-Authorization':'Basic MTI4MjI1NTQwNDoxMjM0NTY=',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
        'Accept':'*/*',
        'Accept-Language':'q=0.5,en-US;q=0.3,en;q=0.2'
    }
    return headers

def geoDecode(listingId,Lng,Lat,proxies):
    # proxypool = proxyPool()
    # proxies = proxypool.proxies()
    # print(proxies,url_headers())
    proxies = {
            "http": "http://{}".format(proxies),
            "https": "https://{}".format(proxies)
        }
    try:
        html = requests.get(url = url_request(Lng,Lat),proxies = proxies,headers = url_headers(),timeout = 8)
    except Exception as e:
        # if "Cannot connect to proxy" in str(e):
            # print(e.args)
            # print(proxies["http"].split("@")[1][:-1])
            # proxy_ip = proxies["http"].split("@")[1][:-1]
            # proxypool.delete(proxy_ip,"Cannot connect to proxy")
        sm.release()
        return
    sm.release()
    try:
        res = json.loads(html.content)
    except Exception as e:
        # print(html.content)
        tqdm.write("++++++++++++++++++++++ overusing OSM ++++++++++++++++++++++++++")
        return
    locationInfor = {}
    if "address" in res:
        address = res["address"]
        locationInfor["display_name"] = res["display_name"].replace("'","''")
        for item in ["town","county","state","postcode","country"]:
            if item in address:
                locationInfor[item] = address[item].replace("'","''")
            else:
                locationInfor[item] = ''
        tqdm.write(str(locationInfor["display_name"]))
    if locationInfor == {} :
        # print("decodeFalse",listingId,Lng,Lat)
        dbInsert(listingId,Lng,Lat,None)
    else:
        dbInsert(listingId,Lng,Lat,locationInfor)
    

def dbInsert(listingId,Lng,Lat,locationInfor):
    db = dbSettings.db_connect()
    cursor = db.cursor()
    if locationInfor == None:
        sql = '''
    INSERT INTO `airbnb_scrapy_us`.`listing_location_us` 
    (`listingid`,`lng`,`lat`,`country`) 
    VALUES ('{}',{},{},'unknown')
    '''.format(listingId,Lng,Lat)
    else :
        sql = '''
    INSERT INTO `airbnb_scrapy_us`.`listing_location_us` 
    (`listingid`,`lng`,`lat`,`country`,`state`,`county`,`postcode`,`town`,`formatted_address`) 
    VALUES ('{}',{},{},'{}','{}','{}','{}','{}','{}');
    '''.format(listingId,Lng,Lat,locationInfor['country'],locationInfor['state'],locationInfor['county'],locationInfor['postcode'],locationInfor['town'],locationInfor['display_name'])
    # print(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e.args)
        print(sql)

def getFromKuaidaili(proxiesList):
    url = "http://svip.kdlapi.com/api/getproxy/?orderid=911944114211460&num=400&protocol=2&method=1&quality=1&format=json&sep=1"
    print(url)
    proxies = {"http": None, "https": None}
    html = requests.get(url, timeout=5, proxies=proxies)

    res = json.loads(html.content)
    print("get proxy ", time.asctime(
        time.localtime(time.time())))
    if 'data' in res:
        res = res['data']
    else:
        print("get proxy err in data")
    count = res['count']

    if 'proxy_list' in res:
        proxys = res['proxy_list']
    else:
        print("get proxy err in proxy_list")

    for proxy in proxys:
        proxiesList.append(proxy)
    return proxiesList

sm = threading.Semaphore(500)

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
        proxiesList = []
        for row in results:
            if len(proxiesList) < 10:
                proxiesList = getFromKuaidaili(proxiesList)
            proxies = proxiesList.pop()
            # time.sleep(0.03)
            if row['listingId'] in existLocation:
                continue
            sm.acquire()
            pbar.update(1)
            thread_run = threading.Thread(target=geoDecode , args=(row['listingId'],row['Lng'],row['Lat'],proxies))
            thread_run.start()

