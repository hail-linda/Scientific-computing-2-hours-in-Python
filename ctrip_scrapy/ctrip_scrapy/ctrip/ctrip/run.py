from scrapy import cmdline


name = 'detaild'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())