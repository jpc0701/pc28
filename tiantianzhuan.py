import urllib.request,json,re,http.cookiejar
from ysdm import *

class RedirectHandler(urllib.request.HTTPRedirectHandler):
	def http_error_301(self, req, fp, code, msg, hdrs):
		return fp    
	def http_error_302(self, req, fp, code, msg, hdrs):
		return fp

#json解析
def response_dic(json1):
	return json.loads(json1)

class tiantianzhuan(object):
	def __init__(self):
		pass
		
	def login(self,username='',password=''):
		if self.is_login()=='login_no':
			while 1:
				ysdm=self.get_verify_code()
				url='https://www.ttz.com/member/login'
				param={'hidSkUrl':'',\
					   'hidGoUrl':'',\
					   'url':'',\
					   'Username':'*******',\
					   'Password':'*******',\
					   'verify':ysdm['Result'],\
					   'REFERER':'        https://www.ttz.com/'}
				postdata = urllib.parse.urlencode(param).encode()
				request = urllib.request.Request(url,postdata)
				response =urllib.request.urlopen(request).read().decode('utf-8')
				if 'VerifyError' in response:
					Submit_Error(ysdm['Id'])
					continue
				elif '"ok"' in response:
					return 'login_ok'
				else:
					return response
		else:
			return 'login_ok'
				
	def is_login(self):
		url='https://www.ttz.com/Member/userInfo'
		request = urllib.request.Request(url)
		response =urllib.request.urlopen(request).read().decode('utf-8')
		if 'no-login' in response:
			return 'login_no'
		else:
			return response_dic(response)
			
	def get_userinfo(self):
		return int(self.is_login()['Luck28Account']['BalanceTotal'])
		
	def get_verify_code(self):
		url='https://www.ttz.com/member/numVerify'
		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request).read()
		return get_VerifyCode(response,{})
	
	def get_odds(self,id):
		try:
			url='https://www.ttz.com/Luck28/ajaxBuy?do=odds&g28=bj&Luck28Id=%s'%id
			request = urllib.request.Request(url)
			response =re.findall(r'"(.+)"',urllib.request.urlopen(request).read().decode('utf-8'))[0]
			return {'status':'ok','odds':list(map(float, response.split(',')))}
		except:
			return {'status':'no'}
		
	def get_now(self):
		url='https://www.ttz.com/Luck28/lotteryInfo?g28=bj'
		request = urllib.request.Request(url)
		response = response_dic(urllib.request.urlopen(request).read().decode('utf-8'))
		return response
		
	def get_time(self):
		temp=self.get_now()['countDown']-59 
		return temp if temp>=0 else 0
		
	def bet(self,id,money):
		url='https://www.ttz.com/Luck28/buy?g28=bj'
		param={'open_prize_time':'1455766230',\
			   'depend_parent':'0',\
			   'str_mdp_coin':','.join(list(map(str, money))),\
			   'lastgain':'',\
			   '_issue':id,\
			   'now_total':sum(money),\
			   'formhash':'',\
			   'check_key':'',\
			   'check_address':'',\
			   'mdp_coin':money[0],\
			   'mdp_coin':money[1],\
			   'mdp_coin':money[2],\
			   'mdp_coin':money[3],\
			   'mdp_coin':money[4],\
			   'mdp_coin':money[5],\
			   'mdp_coin':money[6],\
			   'mdp_coin':money[7],\
			   'mdp_coin':money[8],\
			   'mdp_coin':money[9],\
			   'mdp_coin':money[10],\
			   'mdp_coin':money[11],\
			   'mdp_coin':money[12],\
			   'mdp_coin':money[13],\
			   'mdp_coin':money[14],\
			   'mdp_coin':money[15],\
			   'mdp_coin':money[16],\
			   'mdp_coin':money[17],\
			   'mdp_coin':money[18],\
			   'mdp_coin':money[19],\
			   'mdp_coin':money[20],\
			   'mdp_coin':money[21],\
			   'mdp_coin':money[22],\
			   'mdp_coin':money[23],\
			   'mdp_coin':money[24],\
			   'mdp_coin':money[25],\
			   'mdp_coin':money[26],\
			   'mdp_coin':money[27]}
		header={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',\
				'Accept-Language':'zh-CN,zh;q=0.8',\
				'Cache-Control':'max-age=0',\
				'Connection':'keep-alive',\
				'Content-Type':'application/x-www-form-urlencoded',\
				'Host':'www.ttz.com',\
				'Origin':'https://www.ttz.com',\
				'Referer':'https://www.ttz.com/Luck28/buy?g28=bj&Luck28Id=%s'%id,\
				'Upgrade-Insecure-Requests':'1',\
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
		postdata = urllib.parse.urlencode(param).encode()
		request = urllib.request.Request(url,postdata)
		
		cookie_filename = 'cookie.txt'
		cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
		cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
		handler = urllib.request.HTTPCookieProcessor(cookie)
		opener = urllib.request.build_opener(handler,RedirectHandler)
		response = opener.open(request)
		#print(response.info().as_string())
		#print(response.getcode())
		'''
		response = urllib.request.urlopen(request)
		'''
		print(response.read().decode())
		return response.read().decode()
		
	def ensure_bet(self,id):
		count=0
		while 1:
			count+=1
			if count>=3:
				return False
			try:
				url='https://www.ttz.com/Luck28/myList?g28=bj'
				response=urllib.request.urlopen(url).read().decode()
				categories=re.findall(r'<li class="luck_01 border_left">(\d{6})</li>',response)
				return id in categories
			except:
				pass
		
	def sigin(self):
		url='https://www.ttz.com/Signin/signin'
		header={'Accept':'application/json, text/javascript, */*; q=0.01',\
				'Accept-Language':'zh-CN,zh;q=0.8',\
				'Connection':'keep-alive',\
				'Host':'www.ttz.com',\
				'Referer':'https://www.ttz.com/Signin/index',\
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',\
				'X-Requested-With':'XMLHttpRequest'}
		request = urllib.request.Request(url,headers=header)
		response=urllib.request.urlopen(request).read().decode()
		return response
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		