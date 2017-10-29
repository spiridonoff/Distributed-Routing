
# coding: utf-8

# In[633]:

import random
import matplotlib.pyplot as plt
import math
import json


# In[634]:

#defining nodes
'''
n:node id, out:out going neighbors, in:ingoing neighbors, f:feasibility, tp:total packets generated
r: total rate of packet generation, lambda: rate of packet generation for each destination
phi: routing table
'''
node={1:{'n':1,'out':[2,3],'in':[],'f':1,'tp':[0,0,0,0],'r':0,'lambda':[0,0,0.1,0.1],'phi':[[1.,0,0,0],
                                                                                         [0,1.,0,0],
                                                                                         [0,0.7,0.3,0],
                                                                                         [0,0.2,0.8,0]],
        'DT':[[0],[0],[0],[0]]},
      2:{'n':2,'out':[3,4],'in':[1],'f':0,'tp':[0,0,0,0],'r':0,'lambda':[0,0,0,0.1],'phi':[[0,0,0,0],
                                                                                       [0,1.,0,0],
                                                                                       [0,0,0.,1.],
                                                                                       [0,0,0.7,0.3]],
        'DT':[[0],[0],[0],[0]]},
      3:{'n':3,'out':[4],'in':[1,2,4],'f':0,'tp':[0,0,0,0],'r':0,'lambda':[0,0,0,0],'phi':[[0,0,0,0],
                                                                                       [0,0,0,0],
                                                                                       [0,0,1.,0],
                                                                                       [0,0,0,1.]],
        'DT':[[0],[0],[0],[0]]},
      4:{'n':4,'out':[3],'in':[2,3],'f':0,'tp':[0,0,0,0],'r':0,'lambda':[0,0,0,0],'phi':[[0,0,0,0],
                                                                                        [0,0,0,0],
                                                                                        [0,0,1.,0],
                                                                                        [0,0,0,1.]],
        'DT':[[0],[0],[0],[0]]}}


# In[ ]:




# In[635]:

for key in node.keys():
    node[key]['r']=sum(node[key]['lambda'])
    
    if node[key]['r'] > 0:
        node[key]['f'] = 1
    else:
        node[key]['f'] = 0     


# In[636]:

#link
link={ '12':{'od':(1,2), 'q':{}, 'r':0.5,'ql':0,'na':0,'nd':0,'xl':[0], 'tl':[0],'f':0,
            'trk':0,'tdrk':0,'rk':[0,0],'drk':[0,0],'al':[0],'dl':[0],'md':[0]},
       '13':{'od':(1,3), 'q':{}, 'r':0.5,'ql':0,'na':0,'nd':0,'xl':[0], 'tl':[0],'f':0,
            'trk':0,'tdrk':0,'rk':[0,0],'drk':[0,0],'al':[0],'dl':[0],'md':[0]},
       '24':{'od':(2,4), 'q':{}, 'r':0.5,'ql':0,'na':0,'nd':0,'xl':[0], 'tl':[0],'f':0,
            'trk':0,'tdrk':0,'rk':[0,0],'drk':[0,0],'al':[0],'dl':[0],'md':[0]},
       '34':{'od':(3,4), 'q':{}, 'r':0.5,'ql':0,'na':0,'nd':0,'xl':[0], 'tl':[0],'f':0,
            'trk':0,'tdrk':0,'rk':[0,0],'drk':[0,0],'al':[0],'dl':[0],'md':[0]},
       '23':{'od':(2,3), 'q':{}, 'r':0.5,'ql':0,'na':0,'nd':0,'xl':[0], 'tl':[0],'f':0,
            'trk':0,'tdrk':0,'rk':[0,0],'drk':[0,0],'al':[0],'dl':[0],'md':[0]},
       '43':{'od':(4,3), 'q':{}, 'r':0.5,'ql':0,'na':0,'nd':0,'xl':[0], 'tl':[0],'f':0,
            'trk':0,'tdrk':0,'rk':[0,0],'drk':[0,0],'al':[0],'dl':[0],'md':[0]}}


# In[637]:

dtt=0.001 #delta tau/tau
eta1 = 0.05
eta2 = 0.005
eta3 = 0.0001
eta4 = 0.0005
eta=eta3 #step size


# In[638]:

iteration=0
totaldelay=0
receivedpackets=0
meandelay=[]
t = 0
T1 = 10000
T2 = 5000
T3 = 2500
T4 = 1000

T = 5000 #observation period (ms)
totaltime = 500000 #ms
pcount=0
packet={}
EC={}

while t<totaltime:
    iteration = iteration + 1
    ################### Resetting parameters ###################
    #totaldelay=0
    #receivedpackets=0
    
    for key in node.keys():
        node[key]['tp']=[0,0,0,0]
        
    for key in link.keys():
        link[key]['na']=link[key]['na'] - link[key]['nd']
        if link[key]['na'] != link[key]['ql']:
            print 'ERROR, # of arrivals and Queue length not match'
        link[key]['trk']=0
        link[key]['tdrk']=0
        link[key]['rk']=[0,0]
        link[key]['drk']=[0,0]
        link[key]['al']=link[key]['al'][link[key]['nd']:]
        link[key]['nd']=0
        #link[key]['dl']=[0]
        #link[key]['md']=[0]
    ################### end of resetting ###################
    
    while t<iteration*T:
        #updating event calendar
        for key in node.keys():
            if node[key]['f']==1:
                if not EC.has_key(key): #new feasible event
                    EC[key] = random.expovariate(node[key]['r']) #new event life-time
            else:
                if EC.has_key(key): #delete infeasible events
                    del EC[key]


        for key in link.keys():
            if link[key]['f']==1:
                if not EC.has_key(key): #new feasible event
                    EC[key] = random.expovariate(link[key]['r']) #new event life-time
            else:
                if EC.has_key(key): #delete infeasible events
                    del EC[key]

        #finding the next event
        e = min(EC, key=EC.get)
        y = EC[e] 
        t = t + y #updating time

        #updating the residual life-times
        for key in EC.keys():
              EC[key] = EC[key]-y

        #del the current event from event calendar
        del EC[e]

        flag1 = 0
        for key in node.keys():
            if e==key:
                flag1=flag1+1
                #choosing packet destination
                u = random.random()
                p = 0
                for i in range(len(node[key]['lambda'])):
                    p = p + node[key]['lambda'][i]/node[key]['r']
                    if u <= p:
                        j=i+1 #destination is j
                        break

                #choosing the rout of the packet
                u = random.random()
                p = 0
                for i in range(len(node[key]['phi'][j-1])):
                    p = p + node[key]['phi'][j-1][i]
                    if u <= p:
                        k=i+1 #next node is k
                        break

                #producing packet
                pcount=pcount+1
                packet[pcount]={'ID':pcount,'destination':j,'size':0.9,'arrival time':t,'nodes':[key],'generation time':t}
                node[key]['tp'][j-1]=node[key]['tp'][j-1]+1

                #sending packet to next link
                flag2 = 0
                for key_ in link.keys():
                    if link[key_]['od'] == (key,k):
                        flag2 = 1
                        link[key_]['xl'].append(link[key_]['ql'])
                        link[key_]['tl'].append(t)
                        link[key_]['al'].append(t)
                        link[key_]['ql'] = link[key_]['ql'] + 1
                        link[key_]['na'] = link[key_]['na'] + 1
                        if link[key_]['ql']>1:
                            link[key_]['q'][max(link[key_]['q'])+1] = pcount
                        else:
                            link[key_]['q'][1] = pcount
                        
                        link[key_]['f'] = 1
                        #link[key_]['r'] = packet[link[key_]['q'][min(link[key_]['q'])]]['size']

                if flag2 == 0:
                    print 'ERROR, packet got lost.'

        for key_ in link.keys():
            if e==key_:
                flag1=flag1+1
                #link controling part
                link[key_]['xl'].append(link[key_]['ql']) #saving queue length and time
                link[key_]['tl'].append(t)
                link[key_]['dl'].append(t)
                link[key_]['ql'] = link[key_]['ql'] - 1 #decreasing queue length
                link[key_]['nd'] = link[key_]['nd'] + 1 #increasing number of departures
                pid = link[key_]['q'][min(link[key_]['q'])] #finding the ID of leaving packet

                ################################Start of FPA CALCULATIONS################################
                link[key_]['rk'][1] = link[key_]['rk'][0]
                link[key_]['rk'][0] = t - packet[pid]['arrival time']
                rk1 = link[key_]['rk'][1]

                Ak = link[key_]['al'][link[key_]['nd']]-link[key_]['al'][link[key_]['nd']-1]
                dAk = Ak*dtt

                link[key_]['drk'][1] = link[key_]['drk'][0]
                drk1 = link[key_]['drk'][1]

                #calculating drk
                if Ak > rk1:
                    drk = (-1)*dAk + max(drk1 - Ak + rk1, dAk)
                else:
                    drk = (-1)*dAk + max(drk1, dAk + Ak - rk1)

                link[key_]['drk'][0] = drk

                #calculating tRk=Rk*k
                link[key_]['trk'] = link[key_]['trk'] + link[key_]['rk'][0]
                link[key_]['tdrk'] = link[key_]['tdrk'] + link[key_]['drk'][0]
                md = (link[key_]['trk'] - link[key_]['tdrk']/dtt)/link[key_]['nd']
                link[key_]['md'].append(md)
                ################################END OF FPA CALCULATIONS################################
                
                del link[key_]['q'][min(link[key_]['q'])]

                if len(link[key_]['q'])!=link[key_]['ql']:
                    print 'error, queue length not matching',key_

                if link[key_]['ql']==0: #checking feasibility
                    link[key_]['f']=0

                #else: #adjusting next departure time
                    #link[key_]['r'] = packet[link[key_]['q'][min(link[key_]['q'])]]['size']

                #choosing the rout of the packet
                key=link[key_]['od'][1]
                
                if key in packet[pid]['nodes']:
                    print 'Error, packet visited node', key, ' twice!'
                else:
                    packet[pid]['nodes'].append(key)
                    
                j = packet[pid]['destination']
                node[key]['tp'][j-1] = node[key]['tp'][j-1] + 1
                
                if j==key:
                    totaldelay=totaldelay + t - packet[pid]['generation time']
                    receivedpackets = receivedpackets + 1
                    
                    del packet[pid]
                else:
                    u = random.random()
                    p = 0
                    for i in range(len(node[key]['phi'][j-1])):
                        p = p + node[key]['phi'][j-1][i]
                        if u <= p:
                            k=i+1 #goes to node k
                            break
                    #sending this packet to the next link
                    flag2 = 0
                    for key2 in link.keys():
                        if link[key2]['od'] == (key,k):
                            flag2 = 1
                            link[key2]['xl'].append(link[key2]['ql'])
                            link[key2]['tl'].append(t)
                            link[key2]['al'].append(t)                        
                            link[key2]['ql'] = link[key2]['ql'] + 1
                            link[key2]['na'] = link[key2]['na'] + 1
                            if link[key2]['ql']>1:
                                link[key2]['q'][max(link[key2]['q'])+1] = pid
                            else:
                                link[key2]['q'][1] = pid
                            
                            packet[pid]['arrival time']=t
                            link[key2]['f'] = 1
                            #link[key2]['r'] = packet[link[key2]['q'][min(link[key2]['q'])]]['size']

                    if flag2 != 1:
                        print 'ERROR, packet got lost.', key, k , flag2, j       

        if flag1 == 0:
            print 'ERROR, event got lost'
        elif flag1 > 1:
            print 'ERROR, event got used more than once'
    #end of while loop
    
    ################### calculating marginal delays of each node ###################
    DT=[[0 for i in node.keys()] for j in node.keys()]
    
    for i in [4,3,2,1]:
        for j in node.keys():
            DT[i-1][j-1] = 0
            for k in node[i]['out']:
                DT[i-1][j-1] = DT[i-1][j-1] + node[i]['phi'][j-1][k-1]*(DT[k-1][j-1]+link[str(i)+str(k)]['md'][-1])
        
    for i in node.keys():
        for j in node.keys():
            node[i]['DT'][j-1].append(DT[i-1][j-1])
        
    ################### updating the routing table ###################
    A = [[0 for i in node.keys()] for j in node.keys()]
    Kmin = [[0 for i in node.keys()] for j in node.keys()]
    for i in node.keys():
        for j in node.keys():
            if len(node[i]['out'])>0:
                A[i-1][j-1]=min(DT[k-1][j-1]+link[str(i)+str(k)]['md'][-1] for k in node[i]['out'])
            for k in node[i]['out']:
                if A[i-1][j-1]==DT[k-1][j-1]+link[str(i)+str(k)]['md'][-1]:
                    Kmin[i-1][j-1] = k
                    break
                    
    a = [[[0 for i in node.keys()] for j in node.keys()] for k in node.keys()]
    delta = [[[0 for i in node.keys()] for j in node.keys()] for k in node.keys()]
    
    for i in node.keys():
        for j in node.keys():
            for k in node[i]['out']:
                a[i-1][k-1][j-1]=DT[k-1][j-1]+link[str(i)+str(k)]['md'][-1] - A[i-1][j-1]
                if node[i]['tp'][j-1]>0:
                    delta[i-1][k-1][j-1]=min(node[i]['phi'][j-1][k-1],eta*a[i-1][k-1][j-1]*T/node[i]['tp'][j-1])
                if k!=Kmin[i-1][j-1]:
                    node[i]['phi'][j-1][k-1] = node[i]['phi'][j-1][k-1] - delta[i-1][k-1][j-1]
                    node[i]['phi'][j-1][Kmin[i-1][j-1]-1] = node[i]['phi'][j-1][Kmin[i-1][j-1]-1] + delta[i-1][k-1][j-1]
    
    meandelay.append(totaldelay/receivedpackets)

with open('/home/artin/Desktop/DES/ex_3_mean_delay_%s.json'%eta, 'w') as json_file:
    json.dump(meandelay, json_file)


# In[639]:

plt.step([i*T/1000 for i in range(len(meandelay))],meandelay,linewidth=1.2)
plt.ylabel('mean Delay')
plt.xlabel('Time (sec)')
plt.show()


# In[640]:

with open('/home/artin/Desktop/DES/ex_3_mean_delay_%s.json'%eta1, 'r') as json_file:
    meandelay1 = json.load(json_file)

with open('/home/artin/Desktop/DES/ex_3_mean_delay_%s.json'%eta2, 'r') as json_file:
    meandelay2 = json.load(json_file)
    
with open('/home/artin/Desktop/DES/ex_3_mean_delay_%s.json'%eta3, 'r') as json_file:
    meandelay3 = json.load(json_file)
    
with open('/home/artin/Desktop/DES/ex_3_mean_delay_%s.json'%eta4, 'r') as json_file:
    meandelay4 = json.load(json_file)


# In[650]:

plt.step([i*T/1000 for i in range(len(meandelay1))],meandelay1,'b',linewidth=1.2)
plt.step([i*T/1000 for i in range(len(meandelay2))],meandelay2,'r',linewidth=1.2)
plt.step([i*T/1000 for i in range(len(meandelay3))],meandelay3,'y',linewidth=1.2)
plt.step([i*T/1000 for i in range(len(meandelay4))],meandelay4,'g',linewidth=1.2)
#plt.step([0,totaltime/1000],[26.7,26.7],linestyle='--')
plt.ylabel('mean Delay')
plt.xlabel('Time (sec)')
plt.savefig('Example4: mean delay different step sizes.png')
plt.show()


# In[ ]:




# In[642]:

node[1]['phi'][3]


# In[643]:

node[3]['phi'][3]


# In[644]:

key = 2
j = 4 
Y = [0]+node[key]['DT'][j-1]
plt.step(range(len(Y)),Y)
plt.ylabel('Marginal Delay of node '+ str(key) + ' with destination '+str(j))
plt.xlabel('iteration')
plt.show()


# In[645]:

key='12'
plt.step(link[key]['dl'],link[key]['md'])
plt.ylabel('Marginal Delay on link '+ key)
plt.xlabel('time')
plt.show()


# In[646]:

key='13'
plt.step(link[key]['tl'],link[key]['xl'])
plt.ylabel('Length of Queue on link '+ key)
plt.xlabel('time')
plt.show()



