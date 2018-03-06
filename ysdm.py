#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import *
import urllib.request
import hashlib
import json
import os
import sys

class APIClient(object):
	def __init__(self,imagepath='',username='******',password='*******',typeid='3040',timeout='90',softid='62553',softkey='97b50d74cb754728b609decf7550c8ac'):
		self.__param={}
		self.__param['username']=username
		self.__param['password']=password
		self.__param['typeid']=typeid
		self.__param['timeout']=timeout
		self.__param['softid']=softid
		self.__param['softkey']=softkey
		self.__param['id']=''
		self.__imagepath=imagepath
	
	def imagetobytes(self):
		return self.__imagepath
	
	def upload_image(self):
		url='http://api.ysdm.net/create.json'
		timestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		boundary = '------------' + hashlib.md5(timestr.encode()).hexdigest().lower()
		boundarystr = '\r\n--%s\r\n'%(boundary)

		bs = b''
		for key,value in self.__param.items():
			if key !='result_id':
				bs = bs + boundarystr.encode('ascii')
				param = "Content-Disposition: form-data; name=\"%s\"\r\n\r\n%s"%(key, value)
				#print param
				bs = bs + param.encode('utf8')
		bs = bs + boundarystr.encode('ascii')

		header = 'Content-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/gif\r\n\r\n'%('sample')
		bs = bs + header.encode('utf8')

		bs = bs + self.imagetobytes()
		tailer = '\r\n--%s--\r\n'%(boundary)
		bs = bs + tailer.encode('ascii')

		headers = {'Content-Type':'multipart/form-data; boundary=%s'%boundary,
					'Connection':'Keep-Alive',
					'Expect':'100-continue',
					}
		request = urllib.request.Request(url, bs, headers)
		try:
			response=self.reurlopen(request)
		except Exception as e:
			print(e)
		result_dic=json.loads(response.read().decode('utf-8'))
		if 'Result' in result_dic:
			self.__param['id']=result_dic['Id']
			return result_dic
		else:
			return 'Error'


	def error_submit(self,itemkey=''):
		url='http://api.ysdm.net/reporterror.json'
		bs = []
		if itemkey!='':
			self.__param['id']=itemkey
		for key,value in self.__param.items():
			if key=='username' or key=='password' or key=='softid' or key=='softkey' or key=='id':
				bs.append('%s=%s'%(key,value))
		bs='&'.join(bs)
		bs=bs.encode()
		request = urllib.request.Request(url, data=bs)
		try:
			response=self.reurlopen(request)
		except Exception as e:
			print(e)
		m=response.read().decode('utf-8')
		return m

	def chaxun(self):
		url='http://api.ysdm.net/info.json'
		bs = []
		for key,value in self.__param.items():
			if key=='username' or key=='password':
				bs.append('%s=%s'%(key,value))
		bs='&'.join(bs)
		bs=bs.encode()
		request = urllib.request.Request(url, data=bs)
		try:
			response=self.reurlopen(request)
		except Exception as e:
			print(e)
		Score= json.loads(response.read().decode('utf-8'))['Score']	
		return Score		
	
	def reurlopen(self,request):
		count=0
		while 1:
			count+=1
			if count>=4:
				raise loginError('Error')
			try:
				return urllib.request.urlopen(request)
			except Exception as e:
				print(e)

	def getpath(self):
		return self.__imagepath

def get_VerifyCode(imagebytes,d):
	try:
		v=APIClient(imagebytes)
		for i,j in v.upload_image().items():
			d[i]=j
		return d
	except Exception as e:
		print(e)
		d['Result']='0000'
		return d
		
def Submit_Error(id):
	try:
		v=APIClient('')
		v.error_submit(id)
	except Exception as e:
		print(e)
		
if __name__ == '__main__':
	pass
	
	
	
	
	
	
	
	
	
	
	
	