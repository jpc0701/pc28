import urllib.request,json
from ysdm import *
import urllib.parse, urllib.error
import http.cookiejar,re,time

class xiyou(object):
	def __init__(self):
		pass
		
	def login(self,username='**********',password='********'):
		if self.is_login()==False:
			while 1:
				ysdm=self.get_verify_code()
				url='http://www.xiyou28.com/main/login'
				response =urllib.request.urlopen(url).read().decode('utf-8')
				_csrf=re.findall(r'<meta name="csrf-token" content="(.+)">',response)[0]
				url='http://www.xiyou28.com/main/login'
				param={'_csrf':_csrf,\
					   'LoginForm[username]':username,\
					   'LoginForm[password]':password,\
					   'LoginForm[verifyCode]':ysdm['Result'],\
					   'LoginForm[rememberMe]':'0',\
					   'LoginForm[rememberMe]':'1',\
					   'login-button':''}
				postdata = urllib.parse.urlencode(param).encode()
				request = urllib.request.Request(url,postdata)
				response =urllib.request.urlopen(request)
				if response.geturl()=='http://www.xiyou28.com/main/login':
					Submit_Error(ysdm['Id'])
					continue
				else:
					return 'login_ok'
		else:
			return 'login_ok'
				
	def is_login(self):
		url='http://www.xiyou28.com/user/account'
		request = urllib.request.Request(url)
		response =urllib.request.urlopen(url)
		return response.geturl()==url
		
	def get_verify_code(self):
		url='http://www.xiyou28.com/main/captcha'
		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request).read()
		return get_VerifyCode(response,{})
	
	def get_odds(self,id):
		try:
			url='http://www.xiyou28.com/game/egg/28/betting/%s/%d'%(self.get_num(id),int(id)-820962)
			response =urllib.request.urlopen(url).read().decode()
			_csrf=re.findall(r'<meta name="csrf-token" content="(.+)">',response)[0]
			odds=re.findall(r'<td class="text-center">(.{1,12})</td>\s+<td class="text-center betted">[\d,]+</td>\s+<td class="text-center"><input type="checkbox" class="quick_select" index="(\d{1,2})"></td>',response)
			temp=[0]*28
			for i in odds:
				temp[int(i[1])]=float(i[0])
			return {'status':'ok','odds':temp,'_csrf':_csrf}
		except Exception as e:
			return {'status':'no'}
			
	def get_num(self,id):
		url='http://www.xiyou28.com/game/egg/28/index'
		response =urllib.request.urlopen(url).read().decode()
		num=re.findall(r'href="/game/egg/28/betting/(\w+)/%d"'%(int(id)-820962),response)[0]
		return num
		
	def get_now(self):
		while 1:
			try:
				url='http://www.xiyou28.com/game/egg/28/index'
				r=urllib.request.urlopen(url,timeout=0.5)
				t=r.info().get('Date')
				response=r.read().decode()
				response=re.findall(r'<span id="latest_undraw_info" >第 <span id="draw_number">(\d{6,8})</span> 期，<span id="latest_undraw_close_at" style="display: none;">还有 <span id="close_at" seconds="\d{1,3}">(\d{1,3})</span> 秒停止投注。</span>',response)
				return response[0][0]
			except:
				pass
		
	#投注截止时间提前18s
	def get_time(self):
		while 1:
			try:
				url='https://ss2.bdstatic.com/kfoZeXSm1A5BphGlnYG/icon/weather/aladdin/png_18/a2.png'
				response=urllib.request.urlopen(url,timeout=0.1).info().get('Date')
				y=time.mktime(time.strptime(response,'%a, %d %b %Y %H:%M:%S GMT'))+28800
				return time.localtime(y)
			except:
				pass
		
	def bet(self,id,money,_csrf):
		money=[i if i!=0 else '' for i in money]
		url='http://www.xiyou28.com/game/egg/28/betting/%s/%d'%(self.get_num(id),int(id)-820962)
		param={'_csrf':_csrf,\
			   'showhand-points':'',\
			   'Game28BetsForm[bets0]':money[0],\
			   'Game28BetsForm[bets14]':money[14],\
			   'Game28BetsForm[bets1]':money[1],\
			   'Game28BetsForm[bets15]':money[15],\
			   'Game28BetsForm[bets2]':money[2],\
			   'Game28BetsForm[bets16]':money[16],\
			   'Game28BetsForm[bets3]':money[3],\
			   'Game28BetsForm[bets17]':money[17],\
			   'Game28BetsForm[bets4]':money[4],\
			   'Game28BetsForm[bets18]':money[18],\
			   'Game28BetsForm[bets5]':money[5],\
			   'Game28BetsForm[bets19]':money[19],\
			   'Game28BetsForm[bets6]':money[6],\
			   'Game28BetsForm[bets20]':money[20],\
			   'Game28BetsForm[bets7]':money[7],\
			   'Game28BetsForm[bets21]':money[21],\
			   'Game28BetsForm[bets8]':money[8],\
			   'Game28BetsForm[bets22]':money[22],\
			   'Game28BetsForm[bets9]':money[9],\
			   'Game28BetsForm[bets23]':money[23],\
			   'Game28BetsForm[bets10]':money[10],\
			   'Game28BetsForm[bets24]':money[24],\
			   'Game28BetsForm[bets11]':money[11],\
			   'Game28BetsForm[bets25]':money[25],\
			   'Game28BetsForm[bets12]':money[12],\
			   'Game28BetsForm[bets26]':money[26],\
			   'Game28BetsForm[bets13]':money[13],\
			   'Game28BetsForm[bets27]':money[27]}
		postdata = urllib.parse.urlencode(param).encode()
		request = urllib.request.Request(url,postdata)
		response =urllib.request.urlopen(request,timeout=10)
		return response.geturl()
		
	def get_userinfo(self):
		url='http://www.xiyou28.com/user/account'
		response =urllib.request.urlopen(url).read().decode()
		response=re.findall(r'<span style="line-height:20px;" class="navbar-brand c_fff f_14 pl20 m0">元宝：<span class=".+">([\d,]{1,20})</span></span>',response)[0]
		return int(response.replace(',',''))

	def ensure_bet(self,id):
		count=0
		while 1:
			count+=1
			if count>=3:
				return False
			try:
				url='http://www.xiyou28.com/game/egg/28/history'
				response=urllib.request.urlopen(url).read().decode()
				response=re.findall(r'<td>%s</td>\s+<td>\s+<span class="label label-default">待</span>\s+</td>\s+<td>[\d,]{1,15}</td>\s+<td>-</td>'%id,response)
				if response!=[]:
					return True
				else:
					return False
			except:
				pass
		
	def get_result(self,id):
		url='http://www.xiyou28.com/game/egg/28/history'
		response =urllib.request.urlopen(url).read().decode()
		response=re.findall(r'<td>%s</td>\s+<td>\s+<span class="label label-success .+">[是否]</span>\s+</td>\s+<td>([\d,]{1,15})</td>\s+<td><span class="iconfont icon-jinyuanbao001 .+">([\d,]{1,15})</span></td>'%id,response)[0]
		return {'record':int(response[0].replace(',','')),'draw':int(response[1].replace(',',''))}

	def sigin(self):
		url='http://www.xiyou28.com/user/account/reward/daily'
		response=urllib.request.urlopen(url).read().decode()
		_csrf=re.findall(r'<meta name="csrf-token" content="(.+)">',response)[0]
		param={'_csrf':_csrf}
		postdata = urllib.parse.urlencode(param).encode()
		request = urllib.request.Request(url,postdata)
		response =urllib.request.urlopen(request).read().decode()
		return response
		
	#亏损返利
	def deficit(self):
		url='http://www.xiyou28.com/user/account/reward/deficit'
		response=urllib.request.urlopen(url).read().decode()
		_csrf=re.findall(r'<meta name="csrf-token" content="(.+)">',response)[0]
		param={'_csrf':_csrf}
		postdata = urllib.parse.urlencode(param).encode()
		request = urllib.request.Request(url,postdata)
		response =urllib.request.urlopen(request).read().decode()
		return response
		
	#流水返利
	def prediem(self):
		url='http://www.xiyou28.com/user/account/reward/prediem'
		response=urllib.request.urlopen(url).read().decode()
		_csrf=re.findall(r'<meta name="csrf-token" content="(.+)">',response)[0]
		param={'_csrf':_csrf}
		postdata = urllib.parse.urlencode(param).encode()
		request = urllib.request.Request(url,postdata)
		response =urllib.request.urlopen(request).read().decode()
		return response
		
if __name__ == '__main__':
	cookie=cookie_operate()
	cookie.cookie_load()
	f=xiyou()
	print(f.login())
	#money=[0,0,0,0,0,30,0,0,0,0,10,0,0,0,0,20,0,0,0,50,0,0,0,0,0,0,0,0]
	print(f.get_odds('831606'))
	tt=time.time()
	#print(f.is_login())
	print(time.time()-tt)
	cookie.save_cookie()
























