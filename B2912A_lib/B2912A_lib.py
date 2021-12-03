import os
import time
import pyvisa as visa
import numpy as np

class B2912A:

    #variables initialization
    def __init__(self,addr): 
        self.addr = addr
        self.B2912A = B2912A

    #Visa initialization
    def visaInit (self,timeout_secs):
        rm = visa.ResourceManager('@py')
        self.B2912A = rm.open_resource(self.addr)
        self.B2912A.timeout = timeout_secs * 1000
    
    #Function to know if source is ther
    def areYouThere(self):
        id = self.B2912A.write('*IDN?')
        if(id == '' or id == None):
            print('Device not detected')
        else:
            print('Device %s is here' %id)
    
    #Reset Function
    def reset(self):
        self.B2912A.write('*RST')

    #Close device interface function
    def closeDevice(self):
        self.B2912A.close()        

    #Outputs control 
    def outputOn(self, ch):
        if(ch == 1):
            self.B2912A.write('OUTP1 ON')
            print('ch1 Output ON')
        elif(ch == 2):
            self.B2912A.write('OUTP2 ON')
            print('ch2 Output ON')
        elif(ch == ''):
            print('ERROR: No channel selected')
        else:
            print('ERROR: Invalid channel selected')

    def outputOff(self,ch):
        if(ch == 1):
            self.B2912A.write('OUTP1 OFF')
            print('ch1 Output OFF')
        elif(ch == 2):
            self.B2912A.write('OUTP2 OFF')
            print('ch2 Output OFF')
        elif(ch == ''):
            print('ERROR: No channel selected')
        else:
            print('ERROR: Invalid channel selected')

    

    def sourceConfig(self,value,ch=1,mode='VOLT'):
        self.B2912A.write(':SOUR%s:FUNC:MODE %s'%(ch,mode))
        self.B2912A.write(':SOUR%s:%s %s'%(ch,mode,value))
    
    def senseConfig(self,limit,ch=1,mode='CURR'):
        self.B2912A.write(':SENS%s:FUNC "%s"'%(ch,mode))
        self.B2912A.write(':SENS%s:%s:PROT %s'%(ch,mode,limit))

    def senseFixedRange(self, value, ch=1, fixed=True):
        fix = not(int(fixed))
        self.B2912A.write(':SENS%s:CURR:RANG:AUTO %s'%(ch,fix))
        self.B2912A.write(':SENS%s:CURR:RANG %s'%(ch,value))
    
    def dataFormat(self,elements='CURR',dataType='ASC'):
        self.B2912A.write(':FORM:ELEM:SENS %s'%elements) #Diem quins elements volem al buffer
        self.B2912A.write(':FORM:DATA %s'%dataType) #Diem que volem les dades en format ascii
        print(self.B2912A.query(':FORM:ELEM:SENS?'))

    def triggerConfig(self,period,numPoints,delay,source='TIM'):
        self.B2912A.write(':TRIG:ACQ:SOUR %s'%source)
        self.B2912A.write(':TRIG:%s %s'%(source,period))
        self.B2912A.write(':TRIG:COUN %s'%numPoints)
        self.B2912A.write(':TRIG:DEL %s'%delay)

    def startgetMeasuring(self,ch=1):
        self.B2912A.write(':INIT:ACQ (@%s)'%ch)
        data = self.B2912A.query(':FETC:ARR? (@%s)'%ch)
        datalist = data.split(',')
       
        return datalist

    def startMeasuring(self,ch=1):
        print('Starting measure...')
        self.B2912A.write(':INIT:ACQ (@%s)'%ch)

    def getData(self,ch=1):
        print('Getting data...')
        data = self.B2912A.query(':FETC:ARR? (@%s)'%ch)
        datalist = data.split(',')

        return datalist

    def startMean(self):
        self.B2912A.write(':TRAC:FEED:CONT NEXT')  
        self.B2912A.write(':TRAC:STAT:FORM MEAN')
        self.B2912A.write(':INIT:ACQ (@1)')

    def getMean(self):
        print('Getting mean...')
        data = self.B2912A.query(':TRAC:STAT:DATA?')
        datalist = data.split(',')
        return datalist

    def errorHandling(self):
        print(self.B2912A.query(':SYST:ERR:ALL?'))
        
    #Configuration of source for BLE measurements
    def BLEconfig(self,voltage1,ilimit1,voltage2,ilimit2,buffSize,timePeriod,elem='TIME,CURR'):
        #Configuring CH1 source and measurment params
        self.sourceConfig(value=voltage1,ch=1,mode='VOLT')    
        self.senseConfig(limit=ilimit1,ch=1,mode='CURR') 
        ##Trigger CH1 setup
        self.triggerConfig(timePeriod,buffSize,0,source='TIM')  
        #Configuring CH2 source and measurement params
        self.sourceConfig(value=voltage2,ch=2,mode='VOLT')
        #Data formating
        self.dataFormat(dataType='ASC',elements=elem)

        print("MODE1: " + self.B2912A.query(':SENS1:FUNC:ON?') 
        + 'MODE2: ' + self.B2912A.query(':SENS2:FUNC:ON?'))

    


