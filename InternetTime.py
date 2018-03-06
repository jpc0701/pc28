import os 
import time 
import ntplib 

def set():
	utc_time=time.localtime(time.time())
	if (utc_time.tm_min+4)%5==0:
		while 1:
			try:
				c = ntplib.NTPClient() 
				response = c.request('time.nist.gov') 
				ts = response.tx_time 
				print(ts)
				_date = time.strftime('%Y-%m-%d',time.localtime(ts)) 
				_time = time.strftime('%X',time.localtime(ts)) 
				os.system('date {} && time {}'.format(_date,_time))
				print('%s  同步时间成功！'%time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
				break
			except Exception as e:
				print(e)
				pass
		time.sleep(60)
			
def set1():
	c = ntplib.NTPClient() 
	response = c.request('pool.ntp.org') 
	ts = response.tx_time 
	print(time.time()-ts)
	
			
if __name__ == '__main__':
	while 1:
		try:
			set()
		except:
			print('Error!')


