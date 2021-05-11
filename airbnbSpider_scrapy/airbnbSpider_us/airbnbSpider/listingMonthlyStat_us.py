import requests , sys ,json, time, re
import ssl
import pymysql
import dbSettings
import threading

def sql_listingMonthlyStatistics(listingId,statDate):
    sql = '''SELECT MAX(`house_id`) AS `house_id`,AVG(`price`) AS monthlyPurchasePrice ,SUM(`price`) AS monthlySumPrice , COUNT(`price`)/day(LAST_DAY('{}')) AS rentRate
    FROM (
        SELECT `lastprice`.*
          FROM(
                SELECT `order_us`.`house_id`, `order_us`.`order_date`
                  FROM `order_us`
                  LEFT JOIN `cancel_us` ON `order_us`.`order_date`= `cancel_us`.`order_date`
                   AND `order_us`.`house_id`= `cancel_us`.`house_id`
                 WHERE `order_us`.`house_id`= '{}'
                   AND YEAR(`order_us`.`order_date`)= YEAR('{}')
                   AND MONTH(`order_us`.`order_date`)= month('{}')
                   AND `cancel_us`.`id` IS NULL
                 ORDER BY `order_us`.`order_date` ASC) AS `orderwhitoutcancel`
          LEFT JOIN(
                SELECT `price_us` .`house_id`, `price_us` .`fetch_date`, `lastprice`.`order_date`, `price_us` .`price`
                  FROM(
                SELECT MAX(`id`) as `id`, MAX(`order_date`)  as `order_date`
                  FROM `price_us`
                 WHERE `house_id`= '{}' AND `fetch_date` >= '2021-02-20'
                 group by `order_date`)  AS `lastprice`
                  LEFT JOIN `price_us` ON `lastprice`.`id`= `price_us` .`id`) AS `lastprice` ON `orderwhitoutcancel`.`house_id`= `lastprice` .`house_id`
           AND `orderwhitoutcancel`.`order_date`= `lastprice` .`order_date`
            ) AS `listingOrder`
    '''.format(statDate,listingId,statDate,statDate,listingId)
    return sql

def sql_listingPriceMonthlyStatistics(listingId,statDate):
    sql = '''
    SELECT MAX(`house_id`)  AS `house_id`,
        AVG(`price`)  AS monthlyAvgPrice
    FROM(
            SELECT `price_us` .`house_id`, `price_us` .`fetch_date`, `lastprice`.`order_date`, `price_us` .`price`
            FROM(
                    SELECT MAX(`id`) as `id`, MAX(`order_date`)  as `order_date`
                    FROM `price_us`
                    WHERE `house_id`= '{}'
                    group by `order_date`)  AS `lastprice`
    LEFT JOIN `price_us`
        ON `lastprice`.`id`= `price_us` .`id`
    WHERE YEAR(`price_us`.`order_date`)= YEAR('{}')
    AND MONTH(`price_us`.`order_date`)= month('{}')
    AND `fetch_date` >= '2021-02-20')  AS `pricemonthlystat`
    '''.format(listingId,statDate,statDate)
    return sql

def sql_areaMonthlyStatistics(areaRow,statDate,dimension):
  if dimension == 'district':
    return '''
    SELECT Avg(`monthlystat`.`monthlyAvgPrice`) AS `monthlyAvgPrice`,Avg(`monthlystat`.`monthlyPurchasePrice`) AS `monthlyPurchasePrice`,AVG(`monthlystat`.`monthlySumPrice`) AS `monthlySumPrice`,AVG(`monthlystat`.`rentRate`) AS  `rentRate` FROM 
    (SELECT `listingid`  FROM `listing_location` WHERE `province` = '{province}' AND `city` = '{city}' AND  `district` = '{district}' )AS `district_location` 
    LEFT JOIN `monthlystat`
    ON `district_location` .`listingid` = `monthlystat`.`listingId`
    WHERE `monthlystat`.`year` = '{year}' AND `monthlystat`.`month` = '{month}' AND monthlyAvgPrice < 10000
    '''.format(province = areaRow['province'],city = areaRow['city'],district = areaRow['district'],year = statDate[2:4],month = statDate[5:7])

  if dimension == 'city':
    return '''
    SELECT Avg(`monthlystat`.`monthlyAvgPrice`) AS `monthlyAvgPrice`,Avg(`monthlystat`.`monthlyPurchasePrice`) AS `monthlyPurchasePrice`,AVG(`monthlystat`.`monthlySumPrice`) AS `monthlySumPrice`,AVG(`monthlystat`.`rentRate`) AS  `rentRate` FROM 
    (SELECT `listingid`  FROM `listing_location` WHERE `province` = '{province}' AND `city` = '{city}')AS `district_location` 
    LEFT JOIN `monthlystat`
    ON `district_location` .`listingid` = `monthlystat`.`listingId`
    WHERE `monthlystat`.`year` = '{year}' AND `monthlystat`.`month` = '{month}' AND monthlyAvgPrice < 10000
    '''.format(province = areaRow['province'],city = areaRow['city'],year = statDate[2:4],month = statDate[5:7])

  if dimension == 'province':
    return '''
    SELECT Avg(`monthlystat`.`monthlyAvgPrice`) AS `monthlyAvgPrice`,Avg(`monthlystat`.`monthlyPurchasePrice`) AS `monthlyPurchasePrice`,AVG(`monthlystat`.`monthlySumPrice`) AS `monthlySumPrice`,AVG(`monthlystat`.`rentRate`) AS  `rentRate` FROM 
    (SELECT `listingid`  FROM `listing_location` WHERE `province` = '{province}')AS `district_location` 
    LEFT JOIN `monthlystat`
    ON `district_location` .`listingid` = `monthlystat`.`listingId`
    WHERE `monthlystat`.`year` = '{year}' AND `monthlystat`.`month` = '{month}' AND monthlyAvgPrice < 10000
    '''.format(province = areaRow['province'],year = statDate[2:4],month = statDate[5:7])

# TODO  CN2US
def sql_areaFeatureStatistics(areaRow,statDate,dimension):
  if dimension == 'district':
    return '''
    SELECT  `district_location` .`listingid`, `detail`.* FROM
    (SELECT `listingid`  FROM `listing_location` WHERE `province` = '{province}' AND `city` = '{city}' AND  `district` = '{district}' )AS `district_location` 
    LEFT JOIN `detail` ON `district_location` .`listingid` = `detail`.`listingId` 
    '''.format(province = areaRow['province'],city = areaRow['city'],district = areaRow['district'])

  if dimension == 'city':
    return '''
   SELECT  `district_location` .`listingid`, `detail`.* FROM
    (SELECT `listingid`  FROM `listing_location` WHERE `province` = '{province}' AND `city` = '{city}')AS `district_location` 
    LEFT JOIN `detail` ON `district_location` .`listingid` = `detail`.`listingId` 
    '''.format(province = areaRow['province'],city = areaRow['city'])

  if dimension == 'province':
    return '''
  SELECT  `district_location` .`listingid`, `detail`.* FROM
    (SELECT `listingid`  FROM `listing_location` WHERE `province` = '{province}')AS `district_location` 
    LEFT JOIN `detail` ON `district_location` .`listingid` = `detail`.`listingId` 
    '''.format(province = areaRow['province'])
  
def sql_SELECTDistrict():
  return "SELECT `province` ,`city` ,    `district`, COUNT( `district`)   FROM `listing_location` WHERE `district` != ''  GROUP BY `province`, `city` , `district`;"

def sql_SELECTCity():
  return "SELECT `province` ,`city`,   ''`district`, COUNT( `district`)   FROM `listing_location` WHERE `district` != ''  GROUP BY `province`, `city`  ;"

def sql_SELECTProvince():
  return "SELECT `province`, ''`city`, ''`district`, COUNT( `district`)   FROM `listing_location` WHERE `district` != ''  GROUP BY `province` ;"

# TODO  CN2US
def areaMonthlyStatistics(areaRow,statDate,dimension):
    db = dbSettings.db_connect()
    cursor = db.cursor()
    # print(sql_areaMonthlyStatistics(areaRow,statDate))
    cursor.execute(sql_areaMonthlyStatistics(areaRow,statDate,dimension))
    print(areaRow)
    result = cursor.fetchall()[0]
    print(result)
    if result['monthlySumPrice'] == None:
      return
    statResult = result

    cursor.execute(sql_areaFeatureStatistics(areaRow,statDate,dimension))
    print(areaRow)
    result = cursor.fetchall()[0]
    FeatureResult = {}

    rentalType = {"Entire Home":0,"Private Room":0,"Shared Room":0}
    reviewSummary = {"reviewCount":0,"reviewSummary_wei_zhi_bian_li":0,"reviewSummary_ru_zhu_bian_jie":0,"reviewSummary_ru_shi_miao_shu":0,"reviewSummary_gan_jing_wei_sheng":0,"reviewSummary_gou_tong_shun_chang":0,"reviewSummary_gao_xing_jia_bi":0}
    for row in result :
      # rentalType
      if "整套" in row["propertyType"]:
        rentalType["Entire Home"] += 1
      if "独立" in row["propertyType"]:
        rentalType["Private Room"] += 1
      if "合住" in row["propertyType"]:
        rentalType["Shared Room"] += 1

      # reviewSummary
      for item in ["reviewSummary_wei_zhi_bian_li","reviewSummary_ru_zhu_bian_jie","reviewSummary_ru_shi_miao_shu","reviewSummary_gan_jing_wei_sheng","reviewSummary_gou_tong_shun_chang","reviewSummary_gao_xing_jia_bi"]:
        reviewSummary[item] += row[item]
      reviewSummary["reviewCount"] += 1

    for item in ["reviewSummary_wei_zhi_bian_li","reviewSummary_ru_zhu_bian_jie","reviewSummary_ru_shi_miao_shu","reviewSummary_gan_jing_wei_sheng","reviewSummary_gou_tong_shun_chang","reviewSummary_gao_xing_jia_bi"]:
        reviewSummary[item] = reviewSummary[item]/reviewSummary["reviewCount"]



    sql = "INSERT INTO `airbnb_scrapy_us`.`monthlystat_us` (`dimension`,`province` , `city`, `district`,`year`,`month`,`monthlyAvgPrice`,"+\
      "`monthlySumPrice`,`rentRate`,`repeat_flag`,`monthlyPurchasePrice`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(dimension,areaRow['province'],areaRow['city'],areaRow['district'],statDate[2:4],statDate[5:7],result['monthlyAvgPrice'],result['monthlySumPrice'],result['rentRate'],dimension+"-"+statDate[2:4]+"-"+statDate[5:7]+"-"+areaRow['province']+areaRow['city']+areaRow['district'],result['monthlyPurchasePrice'])
    cursor.execute(sql)
    db.commit()

def listingMonthlyStatistics(listingId,statDate):
    db = dbSettings.db_connect()
    cursor = db.cursor()
    start = time.time()
    cursor.execute(sql_listingMonthlyStatistics(listingId,statDate))
    item = cursor.fetchall()[0]

    monthlyPurchasePrice = item['monthlyPurchasePrice']
    monthlySumPrice = item['monthlySumPrice']
    rentRate        = item['rentRate']
    if monthlyPurchasePrice == None :
      monthlySumPrice = 0
      rentRate = 0
      monthlyPurchasePrice = 0
    cursor.execute(sql_listingPriceMonthlyStatistics(listingId,statDate))
    item = cursor.fetchall()[0]
    print(item)
    monthlyAvgPrice = item['monthlyAvgPrice'] if not item['monthlyAvgPrice'] == None else 0


    end = time.time()
    # print(1000*(end-start),"sql_listingMonthlyStatistics")
    sm.release()
    sql = """
    INSERT INTO `airbnb_scrapy_us`.`monthlystat_us`
     (`dimension`,`listingId`,`year`,`month`,`monthlyAvgPrice`,`monthlyPurchasePrice`,`monthlySumPrice`,`rentRate`,`repeat_flag`) 
     VALUES ('listing','{}','{}','{}'       ,'{}'             ,'{}'                  ,'{}'             ,'{}'      ,'{}')
     """.format(str(listingId),statDate[2:4],statDate[5:7],monthlyAvgPrice,monthlyPurchasePrice,monthlySumPrice,rentRate,statDate[2:4]+"-"+statDate[5:7]+"-"+str(listingId))
    # print(sql)
    cursor.execute(sql)
    db.commit()
    return {'listingId':listingId,'monthlyAvgPrice':monthlyAvgPrice,'monthlySumPrice':monthlySumPrice,'rentRate':rentRate}

sm = threading.Semaphore(30)

if __name__ == "__main__":
    statDate = '2021-04-01'

    db = dbSettings.db_connect()
    cursor = db.cursor()

    # YEAR & MONTH
    cursor.execute("SELECT YEAR('{}') as `YEAR`".format(statDate))
    YEAR = cursor.fetchall()[0]['YEAR']

    cursor.execute("SELECT MONTH('{}') as `MONTH`".format(statDate))
    MONTH = cursor.fetchall()[0]['MONTH']
    print(YEAR,MONTH)

    ########## listing start ##########
    cursor.execute("SELECT `house_id` FROM houselist_us")
    results = cursor.fetchall()
    start = time.time()
    count = 0
    for row in results :
      count += 1
      if count % 1000 == 0:
        print(count)
      # listingMonthlyStatistics(row['house_id'],statDate)
      sm.acquire()
      th = threading.Thread(target=listingMonthlyStatistics, args=(row['house_id'],statDate,))
      th.start()

    while not len(threading.enumerate()) == 1:
      time.sleep(0.01)
      print(len(threading.enumerate()))
    end = time.time()
    print(end-start)
    ########## listing end ##########

    ########## area start ##########
    # cursor.execute(sql_SELECTDistrict())
    # results = cursor.fetchall()
    # for row in results :
    #   areaMonthlyStatistics(row,statDate,"district")

    # cursor.execute(sql_SELECTCity())
    # results = cursor.fetchall()
    # for row in results :
    #   areaMonthlyStatistics(row,statDate,"city")

    # cursor.execute(sql_SELECTProvince())
    # results = cursor.fetchall()
    # for row in results :
    #   areaMonthlyStatistics(row,statDate,"province")

    ########## area end ##########



