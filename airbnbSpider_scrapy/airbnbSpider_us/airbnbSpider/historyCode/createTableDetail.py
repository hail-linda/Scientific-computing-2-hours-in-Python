from pypinyin import pinyin, lazy_pinyin, Style

def pinyin2str(str):
    strList = lazy_pinyin(str,style = 0)
    piny = ""
    for item in strList:
        piny  = piny + "_" +item
    return piny

amenity =   ['健身房','有线电视','电视','可预订长期住宿','暖气','热水','免费停车位','无线网络','网络连接','付费停车位','专门的工作区域','沐浴露','洗衣机',\
                    '床单','吹风机','一氧化碳报警器','遮光窗帘','附近的付费停车位','空调','窗户护栏','急救包','基本餐具','厨房','保安系统','生活必需品','热水壶','灭火器','独立入口',\
                    '冰箱','行李寄存','路边免费停车','衣架','保安','洗发水','烟雾报警器','洗手液']

previewTags = ['优质房源', '可存行李', '日本特惠', '免费接机', '低价优势', '爱彼迎独享', '新上线', '付费接机', '超赞房东', '华人精选', '近地铁站', '中文房东', '可以做饭', '自助入住', '可开发票']
chinaTitleDetails = ['_BED', '_GUESTS', '_BATH', '_ROOM']
reviewSummary = ['位置便利','入住便捷','如实描述','干净卫生','沟通顺畅','高性价比']

amenityCol = ""
for item in amenity:
    amenityCol += 	'`amenity{}` tinyint(1) NULL DEFAULT 0 COMMENT "{}",\n'.format(pinyin2str(item),item)

previewTagsCol = ""
for item in previewTags:
    previewTagsCol += 	'`previewTags{}` tinyint(1) NULL DEFAULT 0 COMMENT "{}",\n'.format(pinyin2str(item),item)

chinaTitleDetailsCol = ""
for item in chinaTitleDetails:
    chinaTitleDetailsCol += 	'`chinaTitleDetails{}` tinyint(1) NULL DEFAULT 0 COMMENT "{}",\n'.format(item,item)

reviewSummaryCol = ""
for item in reviewSummary:
    reviewSummaryCol += 	'`reviewSummary{}` tinyint(1) NULL DEFAULT 0 COMMENT "{}",\n'.format(pinyin2str(item),item)

# print(amenityCol,previewTagsCol,chinaTitleDetailsCol,reviewSummaryCol)


srcStr = '''CREATE TABLE `detail` (
	`id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`listingId` varchar(80) CHARACTER SET utf8 COLLATE utf8_bin NULL,
	`title` varchar(511) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
	`Lat` decimal(16,10)  NULL,
	`Lng` decimal(16,10)  NULL,
	`chinaTitleDetails` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
	`kickers` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
	`ogImage` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
	`previewTags` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
	`propertyType` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
	`reviewCount` int(10) UNSIGNED NULL,
	`reviewScore` int(10) UNSIGNED NULL,
	`reviewTagSummary` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
	`hostAbout` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
	`hostBadges` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
	`hostId` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
	`hostIntroTags` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
	`hostName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
    {}
	PRIMARY KEY (`id`)
) ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=0
ROW_FORMAT=DYNAMIC
AVG_ROW_LENGTH=1582;
'''.format(amenityCol+previewTagsCol+chinaTitleDetailsCol+reviewSummaryCol)

print(srcStr)



