import json,re,requests
from pprint import pprint

import os
import time
import random
import time
import pymysql
import dbSettings
import scrapy
import redis
import demjson
import traceback
from dbSettings import REDIS_URL


class decodeDetail:
    def __init__(self):
        self.meta = {}

    def decode(self,jsonData):
        meta = self.meta
        if "errors" in jsonData:
            # print("errors")
            return meta
        pdpSections = jsonData['data']['merlin']['pdpSections']['sections']
        # print(len(pdpSections))
        for pdpSection in pdpSections:
            pdpSectionId = pdpSection['id']
            if "OVERVIEW_DEFAULT" in pdpSectionId:
                if "section" in pdpSection:

                    # "detailItems"
                    if "detailItems" in pdpSection["section"]:
                        meta["titleDetails"] = [item["title"] for item in pdpSection["section"]["detailItems"]]
                       
                    # kicker is not found
                    # previewTags is not found
            if "HOST_PROFILE_DEFAULT" in pdpSectionId:
                if "section" in pdpSection:
                    try:
                        meta["hostAbout"] = pdpSection["section"]["hostProfileDescription"]["htmlText"]
                    except Exception as e:
                        pass
                        # print(e,"hostAbout")
                    if "hostAvatar" in pdpSection["section"]:
                        hostAvatar = pdpSection["section"]["hostAvatar"]
                        meta["hostId"] = self.ifin(hostAvatar,"userId")
                        meta["hostBadges"] = self.ifin(hostAvatar,"badge")
                    meta["hostIntroTags"]  = self.dig2layers(pdpSection["section"],"hostTags","title")
                    meta["hostName"] = pdpSection["section"]["title"][10:]

            if "AMENITIES_DEFAULT" in pdpSectionId:
                if "section" in pdpSection:
                    if "previewAmenitiesGroups" in pdpSection["section"]:
                        if "amenities" in pdpSection["section"]["previewAmenitiesGroups"][0]:
                            meta["amenity"] = self.dig2layers(pdpSection["section"]["previewAmenitiesGroups"][0],"amenities","title")

            
            if "REVIEWS_DEFAULT" in pdpSectionId:
                if "section" in pdpSection:
                    if "ratings" in pdpSection["section"]:
                        if not pdpSection["section"]["ratings"] == None:
                            meta["reviewSummary"] = self.map2layer(pdpSection["section"],"ratings","label","localizedRating")
                    meta["reviewCount"] = int(self.ifin(pdpSection["section"],"overallCount"))
                    meta["reviewScore"] = self.ifin(pdpSection["section"],"overallRating")

            if "DESCRIPTION_DEFAULT" in pdpSectionId:
                if "section" in pdpSection:
                    if "htmlDescription" in pdpSection["section"]:
                        meta["description"] = self.ifin(pdpSection["section"]["htmlDescription"],"htmlText")

            if "LOCATION_DEFAULT" in pdpSectionId:
                if "section" in pdpSection:
                    if "subtitle" in pdpSection["section"] and "formatted_address" not in meta:
                        if not pdpSection["section"]["subtitle"] == None:
                            meta["formatted_address"] = self.ifin(pdpSection["section"],"subtitle")

                    if "previewLocationDetails" in pdpSection["section"] and len(pdpSection["section"]["previewLocationDetails"])>0  and "formatted_address" not in meta:
                        previewLocationDetails = pdpSection["section"]["previewLocationDetails"]
                        meta["formatted_address"] = self.ifin(previewLocationDetails[0],"title")

                    if "address" in pdpSection["section"] and "formatted_address" not in meta:
                        if not pdpSection["section"]["address"] == None:
                            meta["formatted_address"] = self.ifin(pdpSection["section"],"address")
                            # print("\t\t\t\t\t\t address")

                    
                    # print(meta["formatted_address"])
                    

        pdpMetadata = jsonData['data']['merlin']['pdpSections']['metadata']
        if "loggingContext" in pdpMetadata:
            if "eventDataLogging" in pdpMetadata["loggingContext"]:
                eventDataLogging = pdpMetadata["loggingContext"]["eventDataLogging"]
                meta["listingId"] = self.ifin(eventDataLogging,"listingId")# 'listingId': '45633636',
                meta["Lat"] = self.ifin(eventDataLogging,"listingLat")# 'Lat': 30.68359,
                meta["Lng"] = self.ifin(eventDataLogging,"listingLng")# 'Lng': 104.0718,

        if "seoFeatures" in pdpMetadata:
            if "ogTags" in pdpMetadata["seoFeatures"]:
                ogTags = pdpMetadata["seoFeatures"]["ogTags"]
                meta["ogImage"] = ogTags["ogImage"]

        pdpMetaData = jsonData["data"]["merlin"]["pdpSections"]["metadata"]
        # title : Charming homestead with views, hot tub/fire pit
        if "sharingConfig" in pdpMetaData:
            # print(pdpMetaData["sharingConfig"])
            meta["title"] = self.ifin(pdpMetaData["sharingConfig"],"title")

        if "reviewSummary" in meta :
            for k, v in meta['reviewSummary'].items():
                # print(k,v)
                meta["reviewSummary_"+str(k)]=float(v)
            del meta['reviewSummary']

        if "titleDetails" in meta :
            for item in meta["titleDetails"]:
                if "guests" in item : meta["titleDetails_GUESTS"] = item
                if "bedroom" in item : meta["titleDetails_ROOM"] = item
                if "beds" in item : meta["titleDetails_BED"] = item
                if "bath" in item : meta["titleDetails_BATH"] = item
            del meta["titleDetails"]

        for item in ['amenity','hostIntroTags']:
            if item in meta:
                meta[item] = str(meta[item])

        # pprint(meta)
        return meta


    def decode_cn(self,jsonData):
        meta = self.meta
        StayPDPSections = jsonData['data']["presentation"]["stayProductDetailPage"]["sections"]["sections"]
        for StayPDPSection in StayPDPSections:
            StayPDPSectionsId =StayPDPSection["id"]
            #详情
            if "TITLE_CHINA" in StayPDPSectionsId :
                if "section" in StayPDPSection:

                    #  'chinaTitleDetails': ['2 间卧室', '2 张床', '1 间卫生间', '可住 4 人']
                    if "chinaTitleDetails" in StayPDPSection["section"]:
                        meta["chinaTitleDetails"] =self.map2layer(StayPDPSection["section"],"chinaTitleDetails","icon","title")

                    # 'kickers': '爱彼迎优质房源',
                    if "kickers" in StayPDPSection["section"]:
                        meta["kickers"] = StayPDPSection["section"]["kickers"][0]["content"]

                    #  'previewTags': ['4.9分 · 138条评论', '超赞房东', '优质房源', '近地铁站', '可以做饭', '可存行李'],
                    if "previewTags" in StayPDPSection["section"]:
                        meta["previewTags"] = self.dig2layers(StayPDPSection["section"],"previewTags","name")

                    # 'title': '漫漫|松露 新年特惠/天际观景LOFT/ 免费停车位/8分钟到春熙路/下楼地铁口/可开票'}
                    if "chinaListingTitle" in StayPDPSection["section"]:
                        meta["title"] = StayPDPSection["section"]["chinaListingTitle"]["original"]
            
            # 房东
            if "HOST_INTRO_CHINA" in StayPDPSectionsId :
                if "section" in StayPDPSection:
                    if "primaryHost" in StayPDPSection["section"]:
                        primaryHost = StayPDPSection["section"]["primaryHost"]
                        meta["hostAbout"]       = self.ifin(primaryHost,"about")# 'hostAbout': '漫漫设计师民宿每一间都由设计师团队精心打造｡房间配备投影仪､音响高及品质生活用品,注重美学设计,独具特色且宜 居､舒适｡我们欢迎每一位对生活充满美好期待的客人,漫漫人生､漫漫旅途､慢慢相遇｡在对的地方,遇见对的人,让我们用家的温暖让您的旅途成为温暖的回忆｡',
                        meta["hostBadges"]      = self.dig2layers(primaryHost,"badges","label")# 'hostBadges': ['超赞房东', '条评价', '已验证'],
                        meta["hostIntroTags"]   = self.ifin(primaryHost,"hostIntroTags")# 'hostIntroTags': ['414 条评价', '已验证身份', '超赞房东'],
                        meta["hostName"]        = self.ifin(primaryHost,"hostName")# 'Manmanhome',
                        meta["hostId"]           = self.ifin(primaryHost,"id") # 'hostId': 121674066,
                    # if "descriptions" in StayPDPSection["section"]:
            
            # 便利设施 
            if "LISTING_DETAIL_CHINA" in StayPDPSectionsId :
                if "section" in StayPDPSection:
                    listingDetail = StayPDPSection["section"]
                    # 'amenity': ['健身房','有线电视','电视','可预订长期住宿','暖气','热水','免费停车位','无线网络','网络连接','付费停车位','专门的工作区域','沐浴露','洗衣机',
                    # '床单','吹风机','一氧化碳报警器','遮光窗帘','附近的付费停车位','空调','窗户护栏','急救包','基本餐具','厨房','保安系统','生活必需品','热水壶','灭火器','独立入口',
                    # '冰箱','行李寄存','路边免费停车','衣架','保安','洗发水','烟雾报警器','洗手液'],
                    meta["amenity"] = self.dig2layers(listingDetail,"listingAmenities","title")

            # # 评价
            if "REVIEWS_CHINA" in StayPDPSectionsId :
                if "section" in StayPDPSection:
                    if "reviewDetails" in StayPDPSection["section"]:
                        reviewDetails = StayPDPSection["section"]["reviewDetails"]
                        meta["reviewCount"] = self.ifin(reviewDetails,"reviewCount")#  'reviewCount': 138,
                        meta["reviewScore"] = self.ifin(reviewDetails,"reviewScore")# 'reviewScore': 98,
                        meta["reviewSummary"] = self.map2layer(reviewDetails,"reviewSummary","label","localizedRating")# 'reviewSummary': {'位置便利': '5.0','入住便捷': '5.0','如实描述': '5.0','干净卫生': '4.9','沟通顺畅': '5.0','高性价比': '4.9'},
                        meta["reviewTagSummary"] = self.map2layer(reviewDetails,"reviewTagSummary","localized_tag_name","count")# 'reviewTagSummary': {'位置便利': 64,'入住体验好': 68,'全部': 138,'干净卫生': 47,'待改善': 2,'房东热情': 57,'有设计感': 14,'服务周到': 43,'环境安静': 5,'行李寄存': 2,'设施齐全': 32,'靠近地铁': 8,'靠近市场': 13},

            # 周边
            # if "LOCATION_CHINA" in StayPDPSectionsId :
            #     if "section" in StayPDPSection:
            #         if "pointsOfInterest" in StayPDPSection["section"]:
            #             pointsOfInterest = StayPDPSection["section"]["pointsOfInterest"]
            #             print("interest exist")
            #             meta["interestGroup"] = []
            #             for landmarkGroup in pointsOfInterest:
            #                 if "items" in landmarkGroup:
            #                     for item in landmarkGroup["items"]:
            #                         landmark = {}
            #                         landmark["type"] = landmarkGroup["type"]
            #                         landmark["name"] = item["name"]
            #                         landmark["lat"] = item["lat"]
            #                         landmark["lng"] = item["lng"]
            #                         meta["interestGroup"].append(landmark)



        StayPDPMetadata = jsonData['data']["presentation"]["stayProductDetailPage"]["sections"]["metadata"]
        # listingId 经纬度
        if "loggingContext" in StayPDPMetadata:
            if "eventDataLogging" in StayPDPMetadata["loggingContext"]:
                eventDataLogging = StayPDPMetadata["loggingContext"]["eventDataLogging"]
                meta["listingId"] = self.ifin(eventDataLogging,"listingId")# 'listingId': '45633636',
                meta["Lat"] = self.ifin(eventDataLogging,"listingLat")# 'Lat': 30.68359,
                meta["Lng"] = self.ifin(eventDataLogging,"listingLng")# 'Lng': 104.0718,
        
        # 主图
        if "seoFeatures" in StayPDPMetadata:
            if "ogTags" in StayPDPMetadata["seoFeatures"]:
                ogTags = StayPDPMetadata["seoFeatures"]["ogTags"]
                meta["ogImage"] = ogTags["ogImage"]
        
        if "sharingConfig" in StayPDPMetadata:
            if "propertyType" in StayPDPMetadata["sharingConfig"]:
                meta["propertyType"] = StayPDPMetadata["sharingConfig"]["propertyType"]

        for k, v in meta['reviewSummary'].items():
            # print(k,v)
            meta["reviewSummary"+str(k)]=float(v)
        del meta['reviewSummary']

        for item in meta['amenity']:
            # print(item)
            meta["amenity"+str(item)]=1
        del meta['amenity']

        # decode python obj to json
        for item in ['reviewTagSummary','chinaTitleDetails','hostBadges','hostIntroTags','previewTags']:
            meta[item] = str(meta[item])
        
        meta['hostId'] = str(meta['hostId'])


        self.meta = meta
        return meta

    def dig2layers(self,root,layer1,layer2):
        fruit = []
        if layer1 in root:
            leafs = root[str(layer1)]
            for leaf in leafs:
                if layer2 in leaf :
                    fruit.append(leaf[str(layer2)])
        if len(fruit) == 0:
            return None
        return fruit

    def ifin(self,root,leaf):
        try:
            if leaf in root :
                return root[str(leaf)]
            return None
        except Exception as e:
            print(e,"ifin",root)
    
    def map2layer(self,root,leaf,key,value):
        if leaf in root:
            map = {}
            for singleLeaf in root[leaf]:
                map[singleLeaf[key]] = singleLeaf[value]
        if len(map) == 0:
            return None
        return map

class detailParse:
    def __init__(self):
        self.db = dbSettings.db_connect()
        self.cursor = self.db.cursor()
        self.detailresponseTable = "`detailresponse_us`"

    def getItem(self,bias,landmark,amenity):
        sql = "SELECT * FROM " + self.detailresponseTable + \
            "WHERE id between {} and {}".format(bias, bias+1000)
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        numOfErr = 0
        for row in results:
            try:
                # print(row["id"])
                res = row["response"]
            except:
                print("replace err in ", row["id"])
                errIdList.append(row["id"])
                continue
            # try:
            # print(row["id"])
            meta = {}
            decode = decodeDetail()
            # meta = decode.decode(demjson.decode(res))
            if "429 Too Many Requests" in res :
                print(row["id"],"err : 429 Too Many Request")
                numOfErr += 1
            elif "<html>" in res or "<HTML>" in res:
                print(row["id"],"err : <html>",res)
                numOfErr += 1

            else:
                meta = decode.decode(json.loads(res,strict=False))

            for key ,value in meta.items():
                # print(key,value)
                if isinstance(value,str):
                    meta[str(key)] = value.replace("'","''")

            # pprint(meta["formatted_address"])
            # database location
            # if "listingId" in meta:
                
                
            #     # print(len(meta["formatted_address"].split(",")))
            #     if len(meta["formatted_address"])> 3:
            #         print(len(meta["formatted_address"]),"  ")
            #         for item in meta["formatted_address"][::-1]:
            #             print(item.strip(),end="-")
            #         print(row["id"])
            #     del meta["formatted_address"]
            


            if "listingId" in meta:
                sentence = "INSERT IGNORE INTO `listing_location_us`(`listingid`, `lng`, `lat`, `formatted_address`, `country`, `state`,`city`)\
            VALUE (%s,%s,%s,%s,%s,%s,%s)"
                formatted_address = meta["formatted_address"]
                meta["formatted_address"] = meta["formatted_address"].split(",")
                if len(meta["formatted_address"]) == 3 :
                    print(meta['listingId'],end = " ")
                    vals = (meta["listingId"],meta["Lat"],meta["Lng"], formatted_address,meta["formatted_address"][2],meta["formatted_address"][1],meta["formatted_address"][0])
                    cursor.execute(sentence,vals)
                    db.commit()
                else :
                    sentence = "INSERT IGNORE INTO `listing_location_us`(`listingid`, `lng`, `lat`, `formatted_address`)\
            VALUE (%s,%s,%s,%s)"
                    vals = (meta["listingId"],meta["Lat"],meta["Lng"], formatted_address)
                    cursor.execute(sentence,vals)
                    db.commit()
                del meta["formatted_address"]


            # database detail_us
            # dt = meta
            # tb = 'detail_us'
            # # dt['repeat_flag'] = l.replace("'","")
            # ls = [(k, v) for k, v in dt.items() if v is not None]
            # sentence = 'INSERT  %s (`' % tb + '`,`'.join([i[0] for i in ls]) +\
            #         '`) VALUES (' + ','.join(repr(i[1]) for i in ls) + ');'

            # if "listingId" in meta:
            #     print(meta['listingId'],end = " ")
            # try:
            #     # print(sentence)
            #     cursor.execute(sentence)
            #     db.commit()
            # except:
            #     continue

        print(numOfErr,"\terrs")
        return landmark,amenity




def getMaxNumOfDetailResponse(db,cursor):
    sql = "SELECT MAX(id) FROM `detailresponse_us` order by id desc limit 1"
    cursor.execute(sql)
    db.commit()
    num = cursor.fetchall()[0]["MAX(id)"]
    return num

def startParse(bias,landmark,amenity):
    try:
        parse = detailParse()
        return parse.getItem(bias,landmark,amenity)
    except Exception as e:
        print(e)
        traceback.print_exc()





if __name__ == "__main__":
    # f_in = open( 'src.json', 'r',encoding = 'utf-8' )
    # f_out = open( 'tgt.json', 'w',encoding = 'utf-8' )

    # jsonData =  json.loads(f_in.read())

    db = dbSettings.db_connect()
    cursor = db.cursor()

    startResponseId = 0
    endResponseId = getMaxNumOfDetailResponse(db,cursor)
    # endResponseId = 558

    landmark = set()
    amenity = set()

    for responseId in range(startResponseId, endResponseId+1,1000):
        landmark,amenity = startParse(responseId,landmark,amenity)
        print("landmark length:",len(landmark))
        print("amenity length:", len(amenity))

        # sql = ""
        # for l in list(landmark):
        #     # pprint(eval(l))
        #     tb = 'landmark'
        #     dt = eval(l)
        #     dt['repeat_flag'] = l.replace("'","")
        #     ls = [(k, v) for k, v in dt.items() if v is not None]
        #     sentence = 'INSERT IGNORE %s (' % tb + ','.join([i[0] for i in ls]) +\
        #             ') VALUES (' + ','.join(repr(i[1]) for i in ls) + ');'

        #     # print(sentence)
        #     try:
        #         cursor.execute(sentence)
        #         db.commit()
        #     except:
        #         continue



    # decode = decodeDetail()
    # meta = decode.decode(jsonData)

    # landmark |= set(meta['landmark'])
    # amenity |= set(meta['amenity'])



    # pprint(landmark,amenity)

