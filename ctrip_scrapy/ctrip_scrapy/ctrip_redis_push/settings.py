import const
import os

BASE_DIR = os.path.dirname(__file__)

ENV = const.ENV_DEVELOP

if const.ENV_DEVELOP == ENV:
    # local mysql server
    MYSQL_CONFIG = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "123456",
        "port": 3306,
        "db": "ctrip_scrapy",
        "charset": "UTF8MB4",
    }

    # REDIS_URL = 'redis://:password@127.0.0.1:6379/0'
    REDIS_URL = 'redis://:{psw}@{host}:{port}/{db}'.format(
        host='127.0.0.1',
        port='6379',
        psw='',
        db=0
    )

    LOG_LEVEL = 'DEBUG'
elif const.ENV_PRODUCT == ENV:
    LOG_LEVEL = 'ERROR'
    # mysql server
    MYSQL_CONFIG = {
        "host": "rm-2zere16fvfaicyn38125010.mysql.rds.aliyuncs.com",
        "user": "daduosu",
        "password": "Daduosu@)@)",
        "port": 3306,
        "db": "ctrip_scrapy",
        "charset": "UTF8MB4",
    }

    # REDIS_URL = 'redis://:password@127.0.0.1:6379/0'
    REDIS_URL = 'redis://:{psw}@{host}:{port}/{db}'.format(
        host='r-2zesb09yovvbwc4tw0.redis.rds.aliyuncs.com',
        port='6379',
        psw='Daduosu@)@)',
        db=0
    )
elif const.ENV_DEVELOP_ON_RDS == ENV:
    LOG_LEVEL = 'DEBUG'
    # mysql server
    MYSQL_CONFIG = {
        "host": "rm-2zesd1dlom704lm0a125010.mysql.rds.aliyuncs.com",
        "user": "daduosu",
        "password": "Daduosu@)@)",
        "port": 3306,
        "db": "ctrip_scrapy",
        "charset": "UTF8MB4",
    }

    # REDIS_URL = 'redis://:password@127.0.0.1:6379/0'
    REDIS_URL = 'redis://:{psw}@{host}:{port}/{db}'.format(
        host='r-2zeryyjl6mne2qqzhd.redis.rds.aliyuncs.com',
        port='6379',
        psw='Daduosu@)@)',
        db=0
    )
else:
    # remote mysql server
    pass


EMAIL_SENDER = "598566385@qq.com"
EMAIL_PWD = "ulwccnqefbpqbecd"
EMAIL_NAME = "Daduosu_Alert"

EMAIL_RECIPIENTS = ["jingle.mail@163.com"]

LOG_FILE = os.path.join(BASE_DIR, 'logs/task.log')
LOG_FORMAT = '%(levelname)s %(asctime)s [%(name)s:%(module)s:%(funcName)s:%(lineno)s] [%(exc_info)s] %(message)s'


# CITIES = {"hangzhou": "7", "zhoushan": "20", "huzhou": "111", "jiaxing": "110", "ningbo": "16",
#             "wenzhou": "109", "jinhua": "113", "taizhou": "115", "shaoxing": "112", "lishui": "116",
#             "quzhou": "114"}
CITIES = [{"id":107,"name":"阿坝"},{"id":374,"name":"阿克苏"},{"id":267,"name":"阿拉善"},{"id":382,"name":"阿勒泰"},{"id":307,"name":"安康"},{"id":227,"name":"安庆"},{"id":127,"name":"鞍山"},{"id":120,"name":"安顺"},{"id":173,"name":"安阳"},{"id":196,"name":"白城"},{"id":247,"name":"百色"},{"id":4052,"name":"白沙"},{"id":194,"name":"白山"},{"id":157,"name":"保定"},{"id":302,"name":"宝鸡"},{"id":360,"name":"保山"},{"id":4054,"name":"保亭"},{"id":257,"name":"包头"},{"id":263,"name":"巴彦淖尔"},{"id":377,"name":"巴音郭楞"},{"id":105,"name":"巴中"},{"id":251,"name":"北海"},{"id":48,"name":"北京"},{"id":225,"name":"蚌埠"},{"id":134,"name":"本溪"},{"id":122,"name":"毕节"},{"id":214,"name":"滨州"},{"id":379,"name":"博尔塔拉"},{"id":236,"name":"亳州"},{"id":159,"name":"沧州"},{"id":189,"name":"长春"},{"id":338,"name":"常德"},{"id":378,"name":"昌吉"},{"id":4051,"name":"昌江"},{"id":63,"name":"长沙"},{"id":272,"name":"长治"},{"id":21,"name":"常州"},{"id":83,"name":"潮州"},{"id":158,"name":"承德"},{"id":10,"name":"成都"},{"id":4047,"name":"澄迈"},{"id":339,"name":"郴州"},{"id":259,"name":"赤峰"},{"id":237,"name":"池州"},{"id":22,"name":"重庆"},{"id":254,"name":"崇左"},{"id":365,"name":"楚雄"},{"id":228,"name":"滁州"},{"id":36,"name":"大理州"},{"id":18,"name":"大连"},{"id":129,"name":"丹东"},{"id":3973,"name":"儋州"},{"id":202,"name":"大庆"},{"id":270,"name":"大同"},{"id":209,"name":"大兴安岭"},{"id":96,"name":"达州"},{"id":366,"name":"德宏"},{"id":91,"name":"德阳"},{"id":219,"name":"德州"},{"id":4049,"name":"定安"},{"id":296,"name":"定西"},{"id":4062,"name":"东方"},{"id":73,"name":"东莞"},{"id":211,"name":"东营"},{"id":368,"name":"迪庆"},{"id":261,"name":"鄂尔多斯"},{"id":330,"name":"恩施"},{"id":323,"name":"鄂州"},{"id":252,"name":"防城港"},{"id":68,"name":"佛山"},{"id":128,"name":"抚顺"},{"id":229,"name":"阜阳"},{"id":145,"name":"福州"},{"id":355,"name":"抚州"},{"id":299,"name":"甘南"},{"id":352,"name":"赣州"},{"id":108,"name":"甘孜"},{"id":3996,"name":"高雄"},{"id":102,"name":"广安"},{"id":99,"name":"广元"},{"id":45,"name":"广州"},{"id":245,"name":"贵港"},{"id":32,"name":"桂林"},{"id":117,"name":"贵阳"},{"id":285,"name":"固原"},{"id":64,"name":"哈尔滨"},{"id":311,"name":"海北"},{"id":310,"name":"海东"},{"id":255,"name":"海口"},{"id":313,"name":"海南州"},{"id":316,"name":"海西"},{"id":372,"name":"哈密"},{"id":155,"name":"邯郸"},{"id":7,"name":"杭州"},{"id":305,"name":"汉中"},{"id":171,"name":"鹤壁"},{"id":248,"name":"河池"},{"id":50,"name":"合肥"},{"id":205,"name":"黑河"},{"id":161,"name":"衡水"},{"id":335,"name":"衡阳"},{"id":80,"name":"河源"},{"id":221,"name":"菏泽"},{"id":253,"name":"贺州"},{"id":364,"name":"红河州"},{"id":140,"name":"淮安"},{"id":234,"name":"淮北"},{"id":344,"name":"怀化"},{"id":233,"name":"淮南"},{"id":3997,"name":"花莲"},{"id":327,"name":"黄冈"},{"id":312,"name":"黄南"},{"id":6,"name":"黄山"},{"id":317,"name":"黄石"},{"id":256,"name":"呼和浩特"},{"id":72,"name":"惠州"},{"id":133,"name":"葫芦岛"},{"id":262,"name":"呼伦贝尔"},{"id":111,"name":"湖州"},{"id":204,"name":"佳木斯"},{"id":353,"name":"吉安"},{"id":70,"name":"江门"},{"id":170,"name":"焦作"},{"id":110,"name":"嘉兴"},{"id":4000,"name":"嘉义"},{"id":300,"name":"嘉峪关"},{"id":84,"name":"揭阳"},{"id":190,"name":"吉林"},{"id":3998,"name":"基隆"},{"id":19,"name":"济南"},{"id":288,"name":"金昌"},{"id":273,"name":"晋城"},{"id":347,"name":"景德镇"},{"id":322,"name":"荆门"},{"id":320,"name":"荆州"},{"id":113,"name":"金华"},{"id":215,"name":"济宁"},{"id":4027,"name":"金门"},{"id":275,"name":"晋中"},{"id":130,"name":"锦州"},{"id":349,"name":"九江"},{"id":294,"name":"酒泉"},{"id":199,"name":"鸡西"},{"id":176,"name":"济源"},{"id":177,"name":"开封"},{"id":375,"name":"喀什"},{"id":370,"name":"克拉玛依"},{"id":31,"name":"昆明"},{"id":249,"name":"来宾"},{"id":213,"name":"莱芜"},{"id":160,"name":"廊坊"},{"id":287,"name":"兰州"},{"id":389,"name":"拉萨"},{"id":3993,"name":"乐东"},{"id":93,"name":"乐山"},{"id":97,"name":"凉山"},{"id":39,"name":"连云港"},{"id":220,"name":"聊城"},{"id":12,"name":"丽江"},{"id":278,"name":"临汾"},{"id":4048,"name":"临高"},{"id":5,"name":"陵水(三亚)"},{"id":298,"name":"临夏"},{"id":218,"name":"临沂"},{"id":395,"name":"林芝"},{"id":116,"name":"丽水"},{"id":232,"name":"六安"},{"id":118,"name":"六盘水"},{"id":242,"name":"柳州"},{"id":297,"name":"陇南"},{"id":151,"name":"龙岩"},{"id":341,"name":"娄底"},{"id":174,"name":"漯河"},{"id":168,"name":"洛阳"},{"id":90,"name":"泸州"},{"id":279,"name":"吕梁"},{"id":226,"name":"马鞍山"},{"id":71,"name":"茂名"},{"id":103,"name":"眉山"},{"id":78,"name":"梅州"},{"id":92,"name":"绵阳"},{"id":4001,"name":"苗栗"},{"id":208,"name":"牡丹江"},{"id":346,"name":"南昌"},{"id":94,"name":"南充"},{"id":9,"name":"南京"},{"id":250,"name":"南宁"},{"id":52,"name":"南通"},{"id":4002,"name":"南投"},{"id":175,"name":"南阳"},{"id":101,"name":"内江"},{"id":16,"name":"宁波"},{"id":152,"name":"宁德"},{"id":367,"name":"怒江"},{"id":132,"name":"盘锦"},{"id":98,"name":"攀枝花"},{"id":4003,"name":"澎湖"},{"id":169,"name":"平顶山"},{"id":4004,"name":"屏东（垦丁）"},{"id":293,"name":"平凉"},{"id":348,"name":"萍乡"},{"id":61,"name":"普洱"},{"id":146,"name":"莆田"},{"id":178,"name":"濮阳"},{"id":124,"name":"黔东南"},{"id":125,"name":"黔南"},{"id":123,"name":"黔西南"},{"id":8,"name":"青岛"},{"id":82,"name":"清远"},{"id":65,"name":"秦皇岛"},{"id":244,"name":"钦州"},{"id":407,"name":"琼海"},{"id":4053,"name":"琼中"},{"id":198,"name":"齐齐哈尔"},{"id":148,"name":"泉州"},{"id":358,"name":"曲靖"},{"id":114,"name":"衢州"},{"id":392,"name":"日喀则"},{"id":217,"name":"日照"},{"id":180,"name":"三门峡"},{"id":147,"name":"三明"},{"id":1,"name":"三亚"},{"id":23,"name":"上海"},{"id":308,"name":"商洛"},{"id":181,"name":"商丘"},{"id":356,"name":"上饶"},{"id":69,"name":"汕头"},{"id":79,"name":"汕尾"},{"id":75,"name":"韶关"},{"id":112,"name":"绍兴"},{"id":336,"name":"邵阳"},{"id":332,"name":"神农架"},{"id":126,"name":"沈阳"},{"id":49,"name":"深圳"},{"id":383,"name":"石河子"},{"id":153,"name":"石家庄"},{"id":319,"name":"十堰"},{"id":283,"name":"石嘴山"},{"id":201,"name":"双鸭山"},{"id":191,"name":"四平"},{"id":195,"name":"松原"},{"id":100,"name":"遂宁"},{"id":329,"name":"随州"},{"id":142,"name":"宿迁"},{"id":11,"name":"苏州"},{"id":230,"name":"宿州"},{"id":216,"name":"泰安"},{"id":4005,"name":"台北"},{"id":4006,"name":"台东"},{"id":4007,"name":"台南"},{"id":269,"name":"太原"},{"id":4008,"name":"台中"},{"id":141,"name":"泰州"},{"id":115,"name":"台州"},{"id":154,"name":"唐山"},{"id":4009,"name":"桃园"},{"id":66,"name":"天津"},{"id":290,"name":"天水"},{"id":136,"name":"铁岭"},{"id":193,"name":"通化"},{"id":260,"name":"通辽"},{"id":235,"name":"铜陵"},{"id":121,"name":"铜仁"},{"id":371,"name":"吐鲁番"},{"id":386,"name":"图木舒克"},{"id":43,"name":"万宁"},{"id":212,"name":"潍坊"},{"id":30,"name":"威海"},{"id":304,"name":"渭南"},{"id":4,"name":"文昌"},{"id":363,"name":"文山"},{"id":109,"name":"温州"},{"id":258,"name":"乌海"},{"id":55,"name":"武汉"},{"id":53,"name":"芜湖"},{"id":387,"name":"五家渠"},{"id":264,"name":"乌兰察布"},{"id":369,"name":"乌鲁木齐"},{"id":291,"name":"武威"},{"id":14,"name":"无锡"},{"id":3,"name":"五指山"},{"id":284,"name":"吴忠"},{"id":243,"name":"梧州"},{"id":33,"name":"厦门"},{"id":17,"name":"西安"},{"id":396,"name":"香港"},{"id":334,"name":"湘潭"},{"id":345,"name":"湘西"},{"id":4031,"name":"襄阳"},{"id":328,"name":"咸宁"},{"id":324,"name":"仙桃"},{"id":303,"name":"咸阳"},{"id":326,"name":"孝感"},{"id":266,"name":"锡林郭勒"},{"id":265,"name":"兴安盟"},{"id":156,"name":"邢台"},{"id":309,"name":"西宁"},{"id":4010,"name":"新北"},{"id":172,"name":"新乡"},{"id":182,"name":"信阳"},{"id":350,"name":"新余"},{"id":277,"name":"忻州"},{"id":4012,"name":"新竹"},{"id":58,"name":"西双版纳"},{"id":238,"name":"宣城"},{"id":179,"name":"许昌"},{"id":139,"name":"徐州"},{"id":104,"name":"雅安"},{"id":25,"name":"延安"},{"id":197,"name":"延边"},{"id":54,"name":"盐城"},{"id":81,"name":"阳江"},{"id":271,"name":"阳泉"},{"id":26,"name":"扬州"},{"id":44,"name":"烟台"},{"id":95,"name":"宜宾"},{"id":321,"name":"宜昌"},{"id":203,"name":"伊春"},{"id":354,"name":"宜春"},{"id":4013,"name":"宜兰"},{"id":380,"name":"伊犁"},{"id":282,"name":"银川"},{"id":35,"name":"营口"},{"id":351,"name":"鹰潭"},{"id":343,"name":"益阳"},{"id":340,"name":"永州"},{"id":337,"name":"岳阳"},{"id":246,"name":"玉林"},{"id":306,"name":"榆林"},{"id":276,"name":"运城"},{"id":85,"name":"云浮"},{"id":4014,"name":"云林"},{"id":315,"name":"玉树"},{"id":359,"name":"玉溪"},{"id":38,"name":"枣庄"},{"id":342,"name":"张家界"},{"id":60,"name":"张家口"},{"id":292,"name":"张掖"},{"id":149,"name":"漳州"},{"id":76,"name":"湛江"},{"id":77,"name":"肇庆"},{"id":361,"name":"昭通"},{"id":167,"name":"郑州"},{"id":27,"name":"镇江"},{"id":74,"name":"中山"},{"id":286,"name":"中卫"},{"id":183,"name":"周口"},{"id":20,"name":"舟山"},{"id":51,"name":"珠海"},{"id":184,"name":"驻马店"},{"id":333,"name":"株洲"},{"id":210,"name":"淄博"},{"id":89,"name":"自贡"},{"id":106,"name":"资阳"},{"id":119,"name":"遵义"}]

