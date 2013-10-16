from material import *
from class_pkpm_ggz_result import *

class Ggz:
    def __init__(self,d, t):
        self.b=d
        self.t=t
        self.h=d-2*t
        


#首先读入wpj?.out文件，识别钢管柱，分别调用程序判定

filelist=[]
f=open('wpj.txt', 'r')
while True:
    line=f.readline()
    if not line:
        break
    filelist.append(line)
    
f.close()

#读入钢管柱截面列表，如果当前截面不满足，则自动搜索满足的截面
section_list=[]
f=open('ggzlist.txt', 'r')
while True:
    line=f.readline()
    if not line: break
    sec=line.split()
    atom_ggz=Ggz(int(sec[0]), int(sec[1]))
    section_list.append(atom_ggz)
  
#对每个wpj文件进行读取
for i in range(len(filelist)):
    f=open(filelist[i], 'r')
    w=open('check.txt', 'w')
    
    #找到柱配筋段落
    while True:
        line=f.readline()
        if line.find('柱配筋和验算输出')>0: break
        
    endtag=0
    blanktag=0
    totalline=0
    while True:
        if totalline>4000: break
        #对每一根柱子读入，把数字组成一个列表，然后查找关键字找数据
        colresult=[]
    
        while True:
            line=(f.readline()).replace('*', '') #将星号删掉
            line=line.replace('m', '') #将m删掉
            line=line.replace('=', '') #将=删掉            
            line=line.replace('(', ' ')
            line=line.replace(')', ' ')   #去掉括号          
            #放入数据池
            print(line)

            if line.strip(): 
                blanktag=0          #如果不是空行，则空行标记重置
            else:
                blanktag=blanktag+1         #如果空行，则空行累计

            if not line or blanktag>4: endtag=1 #如果是文件结尾，或连续5行是空行，则结束
                
            colresult+=line.split()
            if line.find('----------')>0: break #---------是构件的分割线
            if endtag>0: break
          
    
        #如果有关键字钢管混凝土，则读取数据
        # nc, b, h, cx, cy, lc, nfc, rcc, rsc, fy, fyv, type, m, n 
        if '钢管混凝土' in colresult:
            nc=int(colresult[colresult.index('N-C')+1]) 
            b=float(colresult[colresult.index('BHUTDF')+1])   
            h=float(colresult[colresult.index('BHUTDF')+2])  
            cx=float(colresult[colresult.index('Cx')+1])   
            cy=float(colresult[colresult.index('Cy')+1])    
            lc=float(colresult[colresult.index('Lc')+1])   
            nfc=int(colresult[colresult.index('Nfc')+1])  
            rcc=int(float(colresult[colresult.index('Rcc')+1]) )
            rsc=int(colresult[colresult.index('Rsc')+1])    
            fy=float(colresult[colresult.index('Fy')+1])    
            fyv=float(colresult[colresult.index('Fyv')+1])  
            type='GGZ'
            m=float(colresult[colresult.index('M')+1])            
            n=float(colresult[colresult.index('N')+1])
        
            #创建钢管柱类
            col=pkpmGGZ(nc, b, h, cx, cy, lc, nfc, rcc, rsc, fy, fyv, type, m, n)
            col.check()
            col.out(w)
            j=0
            while col.capacity_tag:  #如果超过了承载力
                if j>= len(section_list):
                    w.write('找不到适合的截面============================\n')                    
                    break
                col=pkpmGGZ(nc, section_list[j].b, section_list[j].h, cx, cy, lc, nfc, rcc, rsc, fy, fyv, type, m, n)
                col.check()
                j=j+1
            if j>0 and j<len(section_list) :col.out(w)
            
        print(str(blanktag))    
        if endtag>0 : break          
    f.close()        
    w.close()
print('finish')    

