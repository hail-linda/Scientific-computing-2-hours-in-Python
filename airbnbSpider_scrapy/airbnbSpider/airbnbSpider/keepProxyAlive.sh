count=`ps -ef | grep /opt/airbnbSpider/proxyMaintainCookies | wc -l`
killPid=`ps -ef | grep /opt/airbnbSpider/proxyMaintainCookies | grep -v "grep" -m 1 | awk '{print $2}'`
if [ $count -lt 2 ]
then
	nohup python3 /opt/airbnbSpider/proxyMaintainCookies.py &
fi

if [ $count -eq 3 ]
then
 	echo "$killPid"
	kill $killPid
	#nohup python3 /opt/airbnbSpider/proxyMaintainCookies.py &
fi

#ps -ef | grep proxy | grep -v "grep" -m 1 | awk '{print $2}'
#echo "$count"
