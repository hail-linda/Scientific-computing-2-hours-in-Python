import requests
import re
import base64
from urllib import parse

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
}


def get_script_data(base_url,acw = ""):
    '''
    获取js相应参数
    '''
    headers = {
    'X-Airbnb-API-Key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
    'Cookie': 'acw_sc__v2='+acw
    }
    print(headers)


    response = requests.get(base_url, headers=headers)
    arg1 = re.search("arg1='([^']+)'", response.text).group(1)
    return arg1

def unsbox(arg1):
    box = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19, 0xd, 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c, 0x22, 0x25, 0xc, 0x24]
    res = list(range(0, len(arg1)))
    for i in range(0, len(arg1)):
        j = arg1[i]
        for k in range(0, 40):
            if box[k] == i+1:
                res[k] = j
    res = "".join(res)
    return res

def hexXor(arg2):
    box = "3000176000856006061501533003690027800375"
    res = ""
    for i in range(0, 40, 2):
        arg_H = int(arg2[i:i+2], 16)
        box_H = int(box[i:i+2], 16)
        res += hex(arg_H ^ box_H)[2:].zfill(2)
    # print(res)
    return res

if __name__ == '__main__':
    base_url = 'https://www.airbnb.cn/api/v3/PdpAvailabilityCalendar?operationName=PdpAvailabilityCalendar'
    arg1 = get_script_data(base_url)
    # arg1 = "BC5F184213CAF358078C4DC21664A8D6830567AA"
    _0x23a392 = unsbox(arg1)
    arg2 = 'acw_sc__v2=' + hexXor(_0x23a392) + ";"
    print(arg2)
    print(hexXor(_0x23a392))

    while():
        try:
            arg1 = get_script_data(base_url,hexXor(_0x23a392))
        except Exception as e:
            print(arg2,e)
            break
        # arg1 = get_script_data(base_url,hexXor(_0x23a392))
        # arg1 = "AF383E77A68EAA57773646A22DB6AF37B9015206"
        _0x23a392 = unsbox(arg1)
        arg2 = 'acw_sc__v2=' + hexXor(_0x23a392) + ";"
        print(arg2)
        headers['Cookie'] = arg2
        try:
            response = requests.get(base_url, headers=headers)
        except:
            print(arg2)
        print(hexXor(_0x23a392))

    # print(hexXor(unsbox("8238116EA5977D5D00672D1218A3A5588307482B")))
    # print("60a29ae85ae0dad7110c212de28b4c6826b33702")
    # # 8238116EA5977D5D00672D1218A3A5588307482B 	 acw_sc__v2=60a29ae85ae0dad7110c212de28b4c6826b33702
    # print(hexXor(unsbox("83B2B276D04CFD5DE80228C296E7A2068608AA1E")))
    # # 83B2B276D04CFD5DE80228C296E7A2068608AA1E 	 acw_sc__v2=60a29aea0d858e8a99311975e2655b72cc3769bd
    # print(hexXor(unsbox("8DA9ACE905C7E85D4AFB45D2E05CAC7B8A08AB65")))
    # # 8DA9ACE905C7E85D4AFB45D2E05CAC7B8A08AB65 	 acw_sc__v2=60a29aeb5072355be8d96beab4b3b5e96d2ca90d
