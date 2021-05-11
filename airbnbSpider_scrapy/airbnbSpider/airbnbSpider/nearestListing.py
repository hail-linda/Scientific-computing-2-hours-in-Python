import requests , sys ,json ,time ,random
import ssl
import pymysql
import dbSettings

def sql_nearestListing(Lat,Lng,radius):
    sql = '''
    SELECT *,
        SQRT(POW(`lat`-{Lat}, 2) +POW(`lng`-{Lng}, 2)) *10000 AS `distance(m) `
    FROM `listing_location`
    WHERE `lat` BETWEEN {Lat}-{radius}
    AND {Lat}+ {radius}
    AND `lng` BETWEEN {Lng}-{radius}
    and {Lng}+ {radius}
    ORDER BY `distance(m) ` ASC LIMIT 2
    '''.format(Lat=Lat,Lng=Lng,radius=radius)
    return sql

if __name__ == "__main__":
    db = dbSettings.db_connect()
    cursor = db.cursor()
    # print(sql_nearestListing(36.672066,114.459904,0.5))
    start = time.time()
    for index in range(1):
        cursor.execute(sql_nearestListing(36.672066+random.uniform(-10,10) ,114.459904+random.uniform(-10,10),0.5))
        results = cursor.fetchall()
        for row in results:
            print(row)
    print((time.time()-start)*1000)



