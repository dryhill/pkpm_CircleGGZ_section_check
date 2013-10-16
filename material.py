class conc:
    ''' 定义砼材料类'''
    def __init__(self, name):
        self.name=name
        
        if name==30:
            self.fc=14.3
            self.e=3e4
            self.a=2
        
        if name==35:
            self.fc=16.7
            self.e=3.15e4
            self.a=2            
            
        if name==40:
            self.fc=19.1
            self.e=3.25e4
            self.a=2            
            
        if name==45:
            self.fc=21.1
            self.e=3.35e4
            self.a=2            
            
        if name==50:
            self.fc=23.1
            self.e=3.45e4   
            self.a=2         

        if name==55:
            self.fc=25.3
            self.e=3.55e4
            self.a=1.8            
            
        if name==60:
            self.fc=27.5
            self.e=3.6e4
            self.a=1.8                 

        if name==70:
            self.fc=31.8
            self.e=3.7e4
            self.a=1.8                 
            
        if name==80:
            self.fc=35.9
            self.e=3.8e4   
            self.a=1.8                 


class steel:
    ''' 定义钢材料类'''
    def __init__(self, name, thickness):
        self.name=name
        self.thickness=thickness
        self.e=2.06e5
        if thickness<=16: self.fa=310
        if 16<thickness<=40: self.fa=300         


    
        
