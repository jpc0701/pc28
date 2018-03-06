from compute import *
import random

a=[15.7778,14.4058,13.6164,13.2533,13.2533,13.6164,14.4058,15.7778]
c=[15.873,14.4928,13.6986,13.3333,13.3333,13.6986,14.4928,15.873]

b=2

k=(b*0.56-0.44)/b

s=1

r1=[0]*44
r2=[1]*56

r=r1+r2

for i in range(100000):
	bet=0.01
	s-=bet
	result=random.choice(r)
	print(result,end='')
	if result==1:
		s+=(bet*b)
	print('  ',s)
		
print(s)
