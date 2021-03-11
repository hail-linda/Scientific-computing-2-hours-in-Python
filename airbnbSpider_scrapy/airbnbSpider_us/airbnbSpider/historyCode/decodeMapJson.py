import json,re,requests
from pprint import pprint


if __name__ == "__main__":
    f_in = open( 'mapRrsponse.json', 'r',encoding = 'utf-8' )
    f_out = open( 'tgt.json', 'w',encoding = 'utf-8' )

    jsonData =  json.loads(f_in.read())




