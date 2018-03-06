import pymysql,time

#地址
host='mysql.20vps.xrnet.net'
#用户名
username='ww0701'
#密码
password='ww0701'
#数据表
db='ww0701'

l={'id':511423,\
	'ttz_odds1':[1000,333.3333,166.6667,100,66.6667,47.619,35.7143,27.7778,22.2222,18.1818,15.873,14.4928,13.6986,13.3333,13.3333,13.6986,14.4928,15.873,18.1818,22.2222,27.7778,35.7143,47.619,66.6667,100,166.6667,333.333,1000],\
	'xy_odds1':[1000,333.3333,166.6667,100,66.6667,47.619,35.7143,27.7778,22.2222,18.1818,15.873,14.4928,13.6986,13.3333,13.3333,13.6986,14.4928,15.873,18.1818,22.2222,27.7778,35.7143,47.619,66.6667,100,166.6667,333.333,1000],\
	'ttz_odds2':[1000,333.3333,166.6667,100,66.6667,47.619,35.7143,27.7778,22.2222,18.1818,15.873,14.4928,13.6986,13.3333,13.3333,13.6986,14.4928,15.873,18.1818,22.2222,27.7778,35.7143,47.619,66.6667,100,166.6667,333.333,1000],\
	'xy_odds2':[1000,333.3333,166.6667,100,66.6667,47.619,35.7143,27.7778,22.2222,18.1818,15.873,14.4928,13.6986,13.3333,13.3333,13.6986,14.4928,15.873,18.1818,22.2222,27.7778,35.7143,47.619,66.6667,100,166.6667,333.333,1000],\
	'ttz_money':[1000,333.3333,166.6667,100,66.6667,47.619,35.7143,27.7778,22.2222,18.1818,15.873,14.4928,13.6986,13.3333,13.3333,13.6986,14.4928,15.873,18.1818,22.2222,27.7778,35.7143,47.619,66.6667,100,166.6667,333.333,1000],\
	'xy_money':[],\
	'b_ttz_balance':5.36,\
	'b_xy_balance':50.2,\
	'a_ttz_balance':85.6,\
	'a_xy_balance':0}

def Insert(info):
	try:
		conn = pymysql.connect(host=host, user=username, passwd=password,db=db)
		cur = conn.cursor()
		cur.execute("INSERT INTO `ttzxy` (`id`, \
										  `ttz_odds1`, \
										  `xy_odds1`, \
										  `ttz_odds2`, \
										  `xy_odds2`, \
										  `ttz_money`, \
										  `xy_money`, \
										  `a_ttz_balance`, \
										  `a_xy_balance`, \
										  `b_ttz_balance`, \
										  `b_xy_balance`, \
										  `profit`, \
										  `dt`) VALUES \
										  (%s, '%s', '%s', '%s', '%s', '%s', '%s', %f, %f, %f, %f, %f, '%s');"%(\
										  info['id'], \
										  ','.join([str(i) for i in info['ttz_odds1']]), \
										  ','.join([str(i) for i in info['xy_odds1']]), \
										  ','.join([str(i) for i in info['ttz_odds2']]), \
										  ','.join([str(i) for i in info['xy_odds2']]), \
										  ','.join([str(i) for i in info['ttz_money']]), \
										  ','.join([str(i) for i in info['xy_money']]), \
										  info['a_ttz_balance'], \
										  info['a_xy_balance'], \
										  info['b_ttz_balance'], \
										  info['b_xy_balance'], \
										  info['a_ttz_balance']+info['a_xy_balance']-info['b_ttz_balance']-info['b_xy_balance'], \
										  time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))))
		conn.commit()
	except Exception as e:
		print(e)
	conn.close()
	
if __name__ == '__main__':
	Insert(l)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
