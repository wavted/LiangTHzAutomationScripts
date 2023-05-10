# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 10:04:10 2022

@author: Will
"""

import re
import numpy as np







topPositionButton='65, 1034'
#topPositionButton='51, 843'
midPositionButton='207, 1034'
botPositionButton='354, 1034'

topticaTopBarPosition='255, 14'

tempSetWindowPos='1818, 903'
tempSetButtonPos='1803,1013'
tempSetBlankPos='1860, 806'

cryotempSetWindowPos='1389, 945'
cryotempSetButtonPos='1272, 1030'
cryotempSetBlankPos='1510, 804'


topPosName = '15BNoMirror'
midPosName = 'LSATNoMirror'
botPosName= '10NoMirror'
TempStr = ''

scanIndexArray=np.arange(200)+1
scanTime=127.5
TempChangeAdditionalWaitTime=45

#default:
tempWaitTimePerKelvin=90
tempWaitTimePerKelvin=50

motorWaittime=2.9

scanWaitTime=scanTime+2

tempList=['5','5','10','15','17','19','20','21','23','25','27','30','35','40','45','50','55','60','65','70','75','80','85','90','95','100','110','120','130','150','170','200','250','295']
tempList=['300','300']
#tempList=['95','95']
#tempList=['50','55','60','65','70','75','80','85','90','95','100','110','120']


path='../../BLCTesting/BLC Modification Add Ref/ChangeTohalfInchMirror/PergedWithVSWithoutMirror/'






def importTxt(dir):
    file = open(dir, encoding="utf8")
    a= file.read()
    arrayOfWords=a.lower().split()
    
    for x in range(len(arrayOfWords)):
        arrayOfWords[x]=re.sub("[^a-zA-Z]+", "",arrayOfWords[x])
        #x = ''.join(filter(str.isalnum, x))
        if  arrayOfWords[x].isalpha()!=True and arrayOfWords[x]!='':
            print('error, still contains symbols')
            return
    
    file.close()
    return arrayOfWords





totalBreakTime=0

#tempList=['0','0.001','0.002','0.001','0','-0.001','-0.002','-0.001','-0']


with open('sampleAutoMationCodeHeader.ahk', 'r', encoding='utf-8-sig') as file:
    header = file.read()
    file.close()

header=str(header)

with open('sampleAutoMationCodeFooter.ahk', 'r', encoding='utf-8-sig') as file:
    footer = file.read()
    file.close()

footer=str(footer)

finalString=''


for i in range (len(tempList)-1):
    currentTempStr=tempList[i].replace('.', 'p')
    targetTempStr=tempList[i+1].replace('.', 'p')
    
    currentTemp=float(tempList[i])
    targetTemp=float(tempList[i+1])
    
    temp=targetTempStr
    if tempList[i]!=tempList[i+1] :

        
        if targetTemp<=20:
            tempWaitTimePerKelvinAdjusted=tempWaitTimePerKelvin*0.17
        elif targetTemp<=30:
            tempWaitTimePerKelvinAdjusted=tempWaitTimePerKelvin*0.2
        elif targetTemp<=40:
            tempWaitTimePerKelvinAdjusted=tempWaitTimePerKelvin*0.25
        elif targetTemp<=60:
            tempWaitTimePerKelvinAdjusted=tempWaitTimePerKelvin*0.26
        elif targetTemp<=85:
            tempWaitTimePerKelvinAdjusted=tempWaitTimePerKelvin*0.26
        elif targetTemp<=100:
            tempWaitTimePerKelvinAdjusted=tempWaitTimePerKelvin*0.26
        elif targetTemp<150:
            tempWaitTimePerKelvinAdjusted=tempWaitTimePerKelvin*0.30
        elif targetTemp<=180:
            tempWaitTimePerKelvinAdjusted=tempWaitTimePerKelvin*2.2
        elif targetTemp<310:
            tempWaitTimePerKelvinAdjusted=tempWaitTimePerKelvin*2.6
            
            
            
# =============================================================================
#         if targetTemp<=100:
#             tempWaitTimePerKelvinAdjusted=tempWaitTimePerKelvin*1.4
#         elif targetTemp<=200:
#             tempWaitTimePerKelvinAdjusted=tempWaitTimePerKelvin*1.9
#         elif targetTemp<=300:
#             tempWaitTimePerKelvinAdjusted=tempWaitTimePerKelvin*2.1
# =============================================================================

    
        
        breakTime=(TempChangeAdditionalWaitTime+(targetTemp-currentTemp)*tempWaitTimePerKelvinAdjusted)*1000
        print ('time in Min',breakTime/60000)
        totalBreakTime=totalBreakTime+breakTime
        
        
        
        
        
        
        
        #set cryostat temp
            
        with open('AddTempAndWait.ahk', 'r', encoding='utf-8-sig') as file:
            AddTempAndWait = file.read()
            file.close()
            
        AddTempAndWait=str(AddTempAndWait)
        
        
    
        AddTempAndWait=AddTempAndWait.replace('%tempSetWindowPos%', cryotempSetWindowPos)
        AddTempAndWait=AddTempAndWait.replace('%tempSetButtonPos%', cryotempSetButtonPos)
        AddTempAndWait=AddTempAndWait.replace('%tempSetBlankPos%', cryotempSetBlankPos)
        
        if targetTemp<=5:
            cryotargetTemp=targetTemp-0.2
            #cryotargetTemp=targetTemp-2
        elif targetTemp<=12:
            cryotargetTemp=targetTemp-0.9
        elif targetTemp<=18:
            cryotargetTemp=targetTemp-1
        elif targetTemp<=25:
            cryotargetTemp=targetTemp-1.5
        #elif targetTemp<=35:
            #cryotargetTemp=targetTemp-1.5
        #elif targetTemp<=45:
            #cryotargetTemp=targetTemp-2
        elif targetTemp<=320:
            #cryotargetTemp=targetTemp-30
            cryotargetTemp=targetTemp-1
        elif targetTemp<=220:
            cryotargetTemp=targetTemp-1
        elif targetTemp<=320:
            cryotargetTemp=targetTemp-1
# =============================================================================
#         elif targetTemp<=65:
#             cryotargetTemp=targetTemp-2
#         elif targetTemp<=300:
#             cryotargetTemp=targetTemp-2
#         elif targetTemp<=100:
#             cryotargetTemp=targetTemp-20
#         else:
#             cryotargetTemp=targetTemp-35
# =============================================================================
        
        AddTempAndWait=AddTempAndWait.replace('%TempNum%', str(cryotargetTemp))
        AddTempAndWait=AddTempAndWait.replace('BREAKTIMETODO', '0')
        finalString=finalString+AddTempAndWait
        
        
        
        #set sample temp
        with open('AddTempAndWait.ahk', 'r', encoding='utf-8-sig') as file:
            AddTempAndWait = file.read()
            file.close()
            
        AddTempAndWait=str(AddTempAndWait)
        
        
    
        AddTempAndWait=AddTempAndWait.replace('%tempSetWindowPos%', tempSetWindowPos)
        AddTempAndWait=AddTempAndWait.replace('%tempSetButtonPos%', tempSetButtonPos)
        AddTempAndWait=AddTempAndWait.replace('%tempSetBlankPos%', tempSetBlankPos)
        
        
        AddTempAndWait=AddTempAndWait.replace('%TempNum%', str(targetTemp))
        AddTempAndWait=AddTempAndWait.replace('BREAKTIMETODO', str(breakTime))
        finalString=finalString+AddTempAndWait
    
        
        if targetTemp>325:
            finalString='ERROR Target temp set higher than 325K'
            print (finalString)
            break 
    
    

    
    
    
    
    
    
    
    
    
    with open('OnePairScan.ahk', 'r', encoding='utf-8-sig') as file:
        OnePairScanTemplate = file.read()
        file.close()
    
    
    for scanIndex in scanIndexArray:
        
        
        
        
        
        if topPositionButton!='' and topPosName!='':
            
            OnePairScan=OnePairScanTemplate
            OnePairScan=str(OnePairScan)
            OnePairScan=OnePairScan.replace("%sampleName%_%temp%_%field%_%scanIndex%",'%sampleName%_%temp%_%scanIndex%')
            OnePairScan=OnePairScan.replace('%temp%', temp)
            
            if botPositionButton!='' and botPosName!='':
                
                OnePairScan=OnePairScan.replace("%motorWaittime%", str(motorWaittime*2*1000))
            else:
                OnePairScan=OnePairScan.replace("%motorWaittime%", str(motorWaittime*1000))
            OnePairScan=OnePairScan.replace("%topticaTopBarPosition%", topticaTopBarPosition)
            OnePairScan=OnePairScan.replace("%motorPosition%", topPositionButton)

            OnePairScan=OnePairScan.replace("%sampleName%", topPosName)

            
            OnePairScan=OnePairScan.replace('%scanIndex%', str(scanIndex))
            OnePairScan=OnePairScan.replace('%scanWaitTime%', str(scanWaitTime*1000))
            #OnePairScan=OnePairScan.replace('%tempWaitTime%', str(tempWaitTime*1000))
        
            finalString=finalString+OnePairScan


        if midPositionButton!='' and midPosName!='':
            
            OnePairScan=OnePairScanTemplate
            OnePairScan=str(OnePairScan)
            OnePairScan=OnePairScan.replace("%sampleName%_%temp%_%field%_%scanIndex%",'%sampleName%_%temp%_%scanIndex%')
            OnePairScan=OnePairScan.replace('%temp%', temp)
            
            
            OnePairScan=OnePairScan.replace("%motorWaittime%",  str(motorWaittime*1000))
            OnePairScan=OnePairScan.replace("%topticaTopBarPosition%", topticaTopBarPosition)

            OnePairScan=OnePairScan.replace("%motorPosition%", midPositionButton)


            OnePairScan=OnePairScan.replace('%sampleName%', midPosName)


            OnePairScan=OnePairScan.replace('%scanIndex%', str(scanIndex))
            OnePairScan=OnePairScan.replace('%scanWaitTime%', str(scanWaitTime*1000))
            #OnePairScan=OnePairScan.replace('%tempWaitTime%', str(tempWaitTime*1000))
        
            finalString=finalString+OnePairScan
            
        if botPositionButton!='' and botPosName!='':
            
            OnePairScan=OnePairScanTemplate
            OnePairScan=str(OnePairScan)
            OnePairScan=OnePairScan.replace("%sampleName%_%temp%_%field%_%scanIndex%",'%sampleName%_%temp%_%scanIndex%')
            OnePairScan=OnePairScan.replace('%temp%', temp)
            
            
            OnePairScan=OnePairScan.replace("%motorWaittime%",  str(motorWaittime*1000))
            OnePairScan=OnePairScan.replace("%topticaTopBarPosition%", topticaTopBarPosition)

            OnePairScan=OnePairScan.replace("%motorPosition%", botPositionButton)

            OnePairScan=OnePairScan.replace('%sampleName%', botPosName)

            OnePairScan=OnePairScan.replace('%scanIndex%', str(scanIndex))
            OnePairScan=OnePairScan.replace('%scanWaitTime%', str(scanWaitTime*1000))
            #OnePairScan=OnePairScan.replace('%tempWaitTime%', str(tempWaitTime*1000))
        
            finalString=finalString+OnePairScan
  
    
  
    
  
    
  
    
  
    
  
filePath=path+topPosName+midPosName+botPosName+' '+str(tempList[0]).replace('.', 'p')+' to '+str(tempList[-1]).replace('.', 'p')+'.ahk'  
    
f = open(filePath,'w',encoding='utf-8-sig')
f.write(header+finalString+footer)
f.close()



print ('Total waiting time in Min',(totalBreakTime+(motorWaittime+scanWaitTime+4.3)*3*1000*len(scanIndexArray)*(len(tempList)-1 ) )/60000)



