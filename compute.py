import numpy,math
from pulp import *

def reorganization(odds1,odds2):
	new_odds=[]
	odds1_flag=[0]*len(odds1)
	odds2_flag=[0]*len(odds2)
	for i in range(28):
		if odds1[i]>odds2[i]:
			new_odds.append(odds1[i])
			odds1_flag[i]=1
		else:
			new_odds.append(odds2[i])
			odds2_flag[i]=1
	return {'odds':new_odds,'odds1_flag':odds1_flag,'odds2_flag':odds2_flag}
	
	
def reward(odds):
	temp=0
	for i in odds:
		temp+=1/i
	return 1/temp
	
def solve(odds,money):
	A=[]
	for i in range(1,len(odds)):
		temp=[0]*len(odds)
		temp[0]=odds[0]
		temp[i]=-odds[i]
		A.append(temp)
	A.append([1]*len(odds))
	B=[0]*len(odds)
	B[-1]=1
	A=numpy.array(A)
	B=numpy.array(B)
	X=numpy.linalg.solve(A,B)
	return list(X)
	
def compute(odds1,odds2,money):
	reo=reorganization(odds1,odds2)
	rew=reward(reo['odds'])
	if rew>1.003:
		answer=solve(reo['odds'],money)
		odds1_bet=[answer[i]*reo['odds1_flag'][i] for i in range(len(odds1))]
		odds1_money=[int(round(1.18*money*i/sum(odds1_bet))) for i in odds1_bet]
		return {'status':'ok','odds_money':odds1_money,'reward':rew}
	else:
		return {'status':'no','reward':rew}
		
def get_money(money1,money2):
	S=money1+money2
	D=abs(money1-money2)
	MIN=(S-D)/2
	MAX=S-MIN
	F=D/S
	if F<0.995:
		R=(-math.atan(6*(F-0.5)))/33+0.04
		money=int(R*S/10000)*10000
		if money<10000:
			return {'status':'no'}
		else:
			return {'status':'ok','money':money}
	else:
		return {'status':'no'}
		
def recompute(odds1,odds2,money1):
	money1=[int(i/112) for i in money1]
	prob=LpProblem('lp_max',LpMaximize)
	money_xy=[]
	for i in range(28):
		money_xy.append(LpVariable('x%d'%i,lowBound =0))
	prob+=odds1[0]*money1[0]+odds2[0]*money_xy[0]-sum(money1)-sum(money_xy)
	for i in range(27):
		prob+=odds1[i]*money1[i]+odds2[i]*money_xy[i]-odds1[i+1]*money1[i+1]-odds2[i+1]*money_xy[i+1]==0
	prob.solve()
	LpStatus[prob.status]
	'''
	for v in prob.variables():
		print(v.name,'=',v.varValue)
	'''
	money=[int(round(i.varValue)) for i in money_xy]
	return {'money':money,'objective=':value(prob.objective)}
	
if __name__ == '__main__':
	a=[818.82, 336.62, 170.16, 102.15, 68.24, 48.48, 35.99, 27.93, 22.25, 18.12, 15.9, 14.35, 13.38, 13.36, 13.3, 13.65, 14.6, 15.94, 18.12, 22.43, 27.51, 35.65, 48.82, 67.95, 101.61, 174.42, 326.5, 805.93]
	b=[1000.971, 333.944, 166.607, 100.061, 66.607, 47.707, 35.686, 27.782, 22.209, 18.19, 15.865, 14.498, 13.693, 13.338, 13.327, 13.699, 14.49, 15.876, 18.182, 22.223, 27.773, 35.712, 47.612, 66.715, 99.982, 166.698, 333.827, 1001.627]
	print(sum(compute(a,b,100)))
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		
		
