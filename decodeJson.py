import json,re,requests

class decodejson:
    def __init__(self,jsonData):
        jsonData = jsonData['data']['merlin']['pdpSections']

        for data in jsonData:
            print(str(data))

if __name__ == "__main__":
    f_in = open( 'src.json', 'r',encoding = 'utf-8' )
    f_out = open( 'tgt.json', 'w',encoding = 'utf-8' )


    jsonData =  json.loads(f_in.read())

    decodejson(jsonData)




