count=`ps -ef | grep proxy | wc -l`

if [ $count -lt 2 ]
then
	nohup python3 /opt/airbnbSpider/proxyMaintainCookies.py &
fi