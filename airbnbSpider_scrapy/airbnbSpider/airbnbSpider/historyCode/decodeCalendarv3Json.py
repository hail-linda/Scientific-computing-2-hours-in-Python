import json,re,requests
from pprint import pprint


if __name__ == "__main__":
    f_in = open( 'calendarv3response.json', 'r',encoding = 'utf-8' )
    f_out = open( 'tgt.json', 'w',encoding = 'utf-8' )

    jsonData =  json.loads(f_in.read())

    src = jsonData
    pdpAvailabilityCalendar = src['data']['merlin']['pdpAvailabilityCalendar']
    for month in pdpAvailabilityCalendar["calendarMonths"]:
        for day in month["days"]:
            available = day["available"]
            date = day["calendarDate"]
            price = day["price"]["localPriceFormatted"]
            print(available,date,price)




