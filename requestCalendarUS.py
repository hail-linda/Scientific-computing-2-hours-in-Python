import requests
 
# 中文网页：https://baike.so.com/doc/24386561-25208408.html
url1='https://www.airbnb.com/api/v3/PdpAvailabilityCalendar?operationName=PdpAvailabilityCalendar&locale=en&currency=USD&extensions=%7B%22persistedQuery%22:%7B%22version%22:1,%22sha256Hash%22:%22dc360510dba53b5e2a32c7172d10cf31347d3c92263f40b38df331f0b363ec41%22%7D%7D&_cb=1sm426g16se018&variables=%7B%22request%22:%7B%22count%22:3,%22listingId%22:%2237995245%22,%22month%22:3,%22year%22:2021%7D%7D'
#添加请求头
headers = {
    'Host':'www.airbnb.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'X-Airbnb-GraphQL-Platform':'web',
    'X-CSRF-Without-Token':'1',
    'X-Airbnb-GraphQL-Platform-Client':'minimalist-niobe',
    'X-CSRF-Token':'V4$.airbnb.com$opm5kBq-0g0$8lJYwSL1f0shxuWB0W0qspYwHd0v2xVVobVIanuD-AY=',
    'X-Airbnb-API-Key':'d306zoyjsyarp7ifhu67rjxn52tv0t20'
}

response_1=requests.get(url1,headers=headers)
 
response_1.encoding='utf-8'

f1=open('steve_jobs2.html','w',encoding='utf-8')
f1.write(response_1.text)
 
