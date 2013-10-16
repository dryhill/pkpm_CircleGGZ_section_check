from material import *
class pkpmGGZ:
    ''' 定义pkpm结果钢管柱的结果类'''
    def __init__(self,nc, b, h, cx, cy, lc, nfc, rcc, rsc, fy, fyv, type, m, n):
        self.nc=nc
        self.b=b
        self.h=h
        self.cx=cx
        self.cy=cy
        self.lc=lc
        self.nfc=nfc
        self.rcc=rcc
        self.rsc=rsc
        self.fy=fy
        self.fyv=fyv
        self.type=type
        self.m=m
        self.n=n
        #定材料
        self.c=conc(int(self.rcc))
        self.s=steel(self.rsc, (int(self.b)-int(self.h))/2)
    
    def check(self):
        self.aa=3.1416/4*(self.b*self.b-self.h*self.h)
        self.ac=3.1416/4*self.h*self.h
        self.theta=self.s.fa*self.aa/self.c.fc/self.ac
        if int(self.rcc)<=50: bound_theta=1.0
        if int(self.rcc)>50:  bound_theta=1.56
        
        #计算N0
        if 0.5<self.theta<=bound_theta:
            self.n0=0.9*self.ac*self.c.fc*(1+self.c.a*self.theta)
        if bound_theta<self.theta<2.5 :
            self.n0=0.9*self.ac*self.c.fc*(1+self.theta**0.5+self.theta)
            
        #算phie，考虑偏心率
        self.e0=abs(self.m/self.n)
        rc=self.h/2.0
        self.e0rc=self.e0/rc*1000
        if self.e0/rc<=1.55:
            self.phi_e=1/(1+1.85*self.e0/rc)
        else:
            self.phi_e=0.4/(self.e0/rc)
        
        #均按轴心受压柱考虑柱身弯矩梯度影响的等效长度系数k，即phi_1《=1
        if self.phi_e>1 : self.phi_e=1.0
            
        #算phi_1
        #有侧移框架柱k
        if self.e0rc<=0.8:
            self.k=1-0.625*self.e0rc
        else:
            self.k=0.5
            
        #算有效长度Le
        self.le=max(self.cx, self.cy)*self.lc*1000*self.k
        
        if self.le/self.b>4:
            self.phi_1=1-0.115*(self.le/self.b-4)**0.5
        else:
            self.phi_1=1.0
            
        self.nu=self.phi_1*self.phi_e*self.n0
        #计算长细比
        self.r=((((3.1416*self.b**4/64-3.1416*self.h**4/64))*self.s.e+3.1416*self.h**4/64*self.c.e)/(self.s.e*self.aa+self.c.e*self.ac))**0.5
        
        #承载力超限或者长细比大于100，则选择新截面
        if abs(self.n)>self.nu/1000 or self.le/self.r>100:
            self.capacity_tag=1
        else:
            self.capacity_tag=0
            
        # nc, b, h, cx, cy, lc, nfc, rcc, rsc, fy, fyv, type, m, n     
    def out(self, f):
        f.write('{0:10} {1:20d}\n'.format('N-c', self.nc))
        f.write('{0:10} {1:20}\n'.format('D*t', str(self.b)+'*'+str(self.b/2-self.h/2)))
        f.write('{0:10} {1:20.2f}\n'.format('Cx', self.cx))  
        f.write('{0:10} {1:20.2f}\n'.format('Cy', self.cy))     
        f.write('{0:10} {1:20.2f}\n'.format('Lc', self.lc))  
        f.write('{0:10} {1:20d}\n'.format('抗震等级Nfc', self.nfc))    
        f.write('{0:10} {1:20d}\n'.format('砼等级Rcc', self.rcc))           
        f.write('{0:10} {1:20d}\n'.format('钢材', self.rsc))    
        f.write('{0:10} {1:20.2f}\n'.format('设计弯矩M', self.m))
        f.write('{0:10} {1:20.2f}\n'.format('设计轴力', self.n))             
        f.write('{0:10} {1:10.2f}\n'.format('套箍指标', self.theta))     
        f.write('{0:10} {1:10.2f}\n'.format('偏心率', abs(self.e0rc)))
        f.write('{0:10} {1:10.2f}\n'.format('柱等效长度系数k', abs(self.k)))        
        f.write('{0:10} {1:10.2f}\n'.format('Phi_1', self.phi_1))
        f.write('{0:10} {1:10.2f}\n'.format('Phi_e', self.phi_e)) 
        f.write('{0:10} {1:10.2f}\n'.format('N0', self.n0/1000))
        f.write('{0:10} {1:10.2f}\n'.format('Nu', self.nu/1000))             
        f.write('{0:10} {1:10.2f}\n'.format('回转半径', self.r))       
        f.write('{0:10} {1:10.2f}\n'.format('长细比', self.le/self.r))  
        if abs(self.n)>self.nu/1000:
            f.write('***承载力不满足***\n')
        else:
            f.write('承载力满足\n')
        if self.le/self.r>100:
            f.write('***长细比大于100***\n')            
        f.write('----------------------------------------------\n')
      
        print(str(self.nc))
        
