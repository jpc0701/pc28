from compute import *
from xiyou28 import xiyou
from SendMsg_QQ import *
from database import *
from tiantianzhuan import tiantianzhuan
import http.cookiejar,urllib.request,time,threading,re

class RedirectHandler(urllib.request.HTTPRedirectHandler):
	def http_error_301(self, req, fp, code, msg, hdrs):
		return fp    
	def http_error_302(self, req, fp, code, msg, hdrs):
		return fp


class cookie_operate(object):
	def __init__(self):
		self.__cookie_filename = 'cookie.txt'
		self.__cookie = http.cookiejar.MozillaCookieJar(self.__cookie_filename)
		handler = urllib.request.HTTPCookieProcessor(self.__cookie)
		opener = urllib.request.build_opener(handler)
		urllib.request.install_opener(opener)
		
	def cookie_load(self):
		self.__cookie.load(self.__cookie_filename, ignore_discard=True, ignore_expires=True)

	def save_cookie(self):
		self.__cookie.save(ignore_discard=True, ignore_expires=True)

class Thread_Odds (threading.Thread):   #继承父类threading.Thread
	def __init__(self,get_odds,id):
		threading.Thread.__init__(self)
		self.__get_odds=get_odds
		self.__id=id
		self.__odds=[]

	def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
		self.__odds=self.__get_odds(self.__id)

	def get(self):
		return self.__odds
		
def get_odds(plat1,plat2,id):
	plat1=Thread_Odds(plat1.get_odds,id)
	plat2=Thread_Odds(plat2.get_odds,id)
	plat1.start()
	plat2.start()
	plat1.join()
	plat2.join()
	odds1=plat1.get()
	odds2=plat2.get()
	if odds1!=[] and odds2!=[]:
		if odds1['status']=='ok' and odds2['status']=='ok':
			return {'status':'ok','odds1':odds1['odds'],'odds2':odds2['odds'],'_csrf':odds2['_csrf']}
		else:
			return {'status':'no'}
	else:
		return {'status':'no'}

def betting(plat1,id,money1):
	plat1.bet(id,money1)
	time.sleep(3)
	result=plat1.ensure_bet(id)
	temp=''
	if result==True:
		temp='天天赚投注成功！'
		print('天天赚投注成功！')
	else:
		temp='天天赚投注失败！'
		print('天天赚投注失败！')
	return temp
	
def get_time():
	while 1:
		try:
			return time.localtime(time.time())
		except:
			pass
			
def wait(ttz):
	while 1:
		h=ttz.get_time()
		print(h)
		if h==3:
			time.sleep(0.5)
			return True
		if h==2:
			#time.sleep(0.2)
			return True
		if h==1:
			return True
		elif h<=0:
			return False
			
def work():
	cookie=cookie_operate()
	cookie.cookie_load()
	ttz=tiantianzhuan()
	xy=xiyou()
	print(ttz.login())
	print(xy.login())
	cookie.save_cookie()
	while 1:
		utc_time=get_time()
		print(time.strftime("%Y-%m-%d %H:%M:%S",utc_time)+'\r',end='')
		if utc_time.tm_hour>=9:
			if utc_time.tm_hour==23 and utc_time.tm_min>=57:
				time.sleep(300)
				continue
			if (utc_time.tm_min+1)%5==0:
				if utc_time.tm_sec>=0 and utc_time.tm_sec<=5:
					money1=ttz.get_userinfo()
					money2=xy.get_userinfo()
					#money_info=get_money(int(money1/1.18),int(money2*100/1.02))
					money_info={'status':'ok','money':1000000}
					id=ttz.get_now()['lotteryIssue']
					time.sleep(6)
				if utc_time.tm_sec==25:
					if wait(ttz)==False:
						send_qq('哥斯达黎加', '第'+id+'期\n获取时间出错')
						continue
					if money_info['status']=='ok':
						database_info ={'id':0,\
										'ttz_odds1':[],\
										'xy_odds1':[],\
										'ttz_odds2':[],\
										'xy_odds2':[],\
										'ttz_money':[],\
										'xy_money':[],\
										'b_ttz_balance':0,\
										'b_xy_balance':0,\
										'a_ttz_balance':0,\
										'a_xy_balance':0}
						print('')
						print('第%s期'%id)
						database_info['id']=int(id)
						print('当前余额：')
						print('    天天赚：%.3f 元'%round(money1/100000/1.18,3))
						print('    嘻游网：%.3f 元'%round(money2/1000/1.02,3))
						database_info['b_ttz_balance']=round(money1/100000/1.18,3)
						database_info['b_xy_balance']=round(money2/1000/1.02,3)
						sum1=round(money1/100000/1.18,3)+round(money2/1000/1.02,3)
						print('    总计：%.3f 元'%sum1)
						money=money_info['money']
						odds=get_odds(ttz,xy,id)
						if odds['status']=='ok':
							print('本期赔率：')
							print('    天天赚：',odds['odds1'])
							print('    嘻游网：',odds['odds2'])
							database_info['ttz_odds1']=odds['odds1']
							database_info['xy_odds1']=odds['odds2']
							result=compute(odds['odds1'],odds['odds2'],money)
							print('理论返奖率：%f'%result['reward'])
							if result['status']=='ok':
								print('投注方案：')
								print('    计划投注总金额：%.3f 元'%round(money/100000,3))
								print('    天天赚：',result['odds_money'])
								print('      小计：%d'%sum(result['odds_money']))
								
								database_info['ttz_money']=result['odds_money']
								#database_info['xy_money']=result['odds2_money']
								
								msg='理论返奖率：%f'%result['reward']
								
								#此处投注
								msg=msg+'\n'+betting(ttz,id,result['odds_money'])
								#msg=msg+'\n'+betting1(ttz,xy,id,result['odds1_money'])
								################
								
								'''
								odds=get_odds(ttz,xy,id)
								m=recompute(odds['odds1'],odds['odds2'],result['odds1_money'])
								print(sum(m['money']))
								print(m)
								result=compute(odds['odds1'],odds['odds2'],money)
								print(result['reward'])
								'''
								
								#print(reward(reorganization(odds['odds1'],odds['odds2'])['odds']))
								################
								
								for k in range(180):
									print('                 \r',end='')
									print('开奖倒计时 %d 秒\r'%(180-k),end='')
									time.sleep(1)		
								print('                 \r',end='')
								a_money1=ttz.get_userinfo()
								a_money2=xy.get_userinfo()
								sum2=round(a_money1/100000/1.18,3)+round(a_money2/1000/1.02,3)
								msg=msg+'\n投注结果：\n    天天赚：%.3f 元\n    嘻游网：%.3f 元\n    总计：%.3f 元\n本期盈利：%.3f 元'%(round(a_money1/100000/1.18,3),round(a_money2/1000/1.02,3),sum2,sum2-sum1)
								print('投注结果：')
								print('    天天赚：%.3f 元'%round(a_money1/100000/1.18,3))
								print('    嘻游网：%.3f 元'%round(a_money2/1000/1.02,3))
								print('    总计：%.3f 元'%sum2)
								print('本期盈利：%.3f 元'%(sum2-sum1))
								database_info['a_ttz_balance']=round(a_money1/100000/1.18,3)
								database_info['a_xy_balance']=round(a_money2/1000/1.02,3)
								print('')
								Insert(database_info)
							else:
								msg='返奖率未达到要求'
								print('返奖率未达到要求')
						else:
							msg='获取赔率失败'
							print('获取赔率失败')
					else:
						msg='计划投注金额过小'
						print('计划投注金额过小')
					send_qq('哥斯达黎加', '第'+id+'期\n'+msg)
					time.sleep(1)
		elif utc_time.tm_hour==8:
			if utc_time.tm_min==50:
				print(ttz.login())
				print(xy.login())
				ttz.sigin()
				xy.sigin()
				xy.deficit()
				xy.prediem()
				time.sleep(60)
		else:
			break
	
def test():
	cookie=cookie_operate()
	cookie.cookie_load()
	ttz=tiantianzhuan()
	xy=xiyou()
	print(ttz.login())
	print(xy.login())
	cookie.save_cookie()
	for i in range(20):
		print(ttz.get_time())
	
def run():
	while 1:
		try:
			while 1:
				utc_time=get_time()
				print(time.strftime("%Y-%m-%d %H:%M:%S",utc_time)+'\r',end='')
				if utc_time.tm_hour>=8:
					break
			work()
		except Exception as e:
			print(e)
			send_qq('我', str(e))
	
if __name__ == '__main__':
	run()


	
