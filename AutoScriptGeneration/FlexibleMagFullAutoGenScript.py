 # -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 10:04:10 2022

@author: Will
"""

import re
import numpy as np


topPosName = 'LongTest1'
midPosName = 'LongTest2'
botPosName= 'LongTest3'
fieldStr = 'kG'
temp = '30'

topPositionButton='1566, 696'
midPositionButton='1711, 696'
botPositionButton='1853, 696'
topticaTopBarPosition='313, 11'




fieldSetWindowPos='1173, 1031'
fieldSetButtonPos='1341, 1031'
fieldSetBlankPos='1255,1031'



zeroToTenRamp=0.01
#zeroToTenRamp=0.016
tenToSevenRamp=0.016
#tenToSevenRamp=0.023

#tempWaitTime=12
scanIndexArray=np.arange(25)+1
scanTime=14.2
scanTime=47
motorWaittime=6.4

scanWaitTime=scanTime+2


fieldList=['0','65','50','40','30','20','10','0','-10','-20','-30','-40','-50','-65','-0']
#fieldList=['30','20','10','0','-10','-20','-30','-40','-50','-65','-0']

fieldList=['0','0']

path='../../LCCO/Mag121222LCCO13New13Old/'






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

#fieldList=['0','0.001','0.002','0.001','0','-0.001','-0.002','-0.001','-0']


with open('sampleAutoMationCodeHeader.ahk', 'r', encoding='utf-8-sig') as file:
    header = file.read()
    file.close()

header=str(header)

with open('sampleAutoMationCodeFooter.ahk', 'r', encoding='utf-8-sig') as file:
    footer = file.read()
    file.close()

footer=str(footer)

finalString=''


for i in range (len(fieldList)-1):
    
    currentFieldStr=fieldList[i]
    targetFieldStr=fieldList[i+1]
    
    currentField=float(currentFieldStr)
    targetField=float(targetFieldStr)
    
    
    if abs(currentField)<10 or abs (targetField)<10:
        if max (abs(currentField), abs (targetField))<10:
            timeAfter10=0
            timeBefore10=(max (abs(currentField), abs (targetField))-(min (abs(currentField), abs (targetField))))/zeroToTenRamp
        else:
            timeAfter10=(max (abs(currentField), abs (targetField))-10)/tenToSevenRamp
            timeBefore10=(10-(min (abs(currentField), abs (targetField))))/zeroToTenRamp
    else:
        timeBefore10=0
        timeAfter10=(max (abs(currentField), abs (targetField))-(min (abs(currentField), abs (targetField))))/tenToSevenRamp
    
                                                                 
    timeTakes=timeBefore10+timeAfter10
    
    breakTime=(timeTakes*1.01+50)*1000
    
    if currentField==targetField:
        breakTime=0
    
    print (breakTime)
    print ('time in Min',breakTime/60000)
    totalBreakTime=totalBreakTime+breakTime
    
    
    
    with open('AddFieldAndWait.ahk', 'r', encoding='utf-8-sig') as file:
        AddFieldAndWait = file.read()
        file.close()
        
    AddFieldAndWait=str(AddFieldAndWait)
    AddFieldAndWait=AddFieldAndWait.replace('%fieldNum%', targetFieldStr)
    AddFieldAndWait=AddFieldAndWait.replace('BREAKTIMETODO', str(breakTime))
    
    AddFieldAndWait=AddFieldAndWait.replace('%tempSetWindowPos%', fieldSetWindowPos)
    AddFieldAndWait=AddFieldAndWait.replace('%tempSetButtonPos%', fieldSetButtonPos)
    AddFieldAndWait=AddFieldAndWait.replace('%tempSetBlankPos%', fieldSetBlankPos)
    
    
    if  breakTime>0:
    
        finalString=finalString+AddFieldAndWait
    
    
    if targetField>67:
        finalString='ERROR Target field set higher than 6.7T'
        print (finalString)
        break 
    
    
    
    
    
    with open('OnePairScan.ahk', 'r', encoding='utf-8-sig') as file:
        OnePairScanTemplate = file.read()
        file.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    for scanIndex in scanIndexArray:
        
        
        
        
        
        if topPositionButton!='' and topPosName!='':
            
            OnePairScan=OnePairScanTemplate
            OnePairScan=str(OnePairScan)
            
            OnePairScan=OnePairScan.replace("%motorWaittime%", str(motorWaittime*2*1000))
            OnePairScan=OnePairScan.replace("%topticaTopBarPosition%", topticaTopBarPosition)
            OnePairScan=OnePairScan.replace("%motorPosition%", topPositionButton)

            OnePairScan=OnePairScan.replace("%sampleName%", topPosName)

            OnePairScan=OnePairScan.replace('%field%', targetFieldStr+fieldStr)
            OnePairScan=OnePairScan.replace('%temp%', temp)
            OnePairScan=OnePairScan.replace('%scanIndex%', str(scanIndex))
            OnePairScan=OnePairScan.replace('%scanWaitTime%', str(scanWaitTime*1000))
            #OnePairScan=OnePairScan.replace('%tempWaitTime%', str(tempWaitTime*1000))
        
            finalString=finalString+OnePairScan


        if midPositionButton!='' and midPosName!='':
            
            OnePairScan=OnePairScanTemplate
            OnePairScan=str(OnePairScan)
            
            OnePairScan=OnePairScan.replace("%motorWaittime%",  str(motorWaittime*1000))
            OnePairScan=OnePairScan.replace("%topticaTopBarPosition%", topticaTopBarPosition)

            OnePairScan=OnePairScan.replace("%motorPosition%", midPositionButton)


            OnePairScan=OnePairScan.replace('%sampleName%', midPosName)

            OnePairScan=OnePairScan.replace('%field%', targetFieldStr+fieldStr)
            OnePairScan=OnePairScan.replace('%temp%', temp)
            OnePairScan=OnePairScan.replace('%scanIndex%', str(scanIndex))
            OnePairScan=OnePairScan.replace('%scanWaitTime%', str(scanWaitTime*1000))
            #OnePairScan=OnePairScan.replace('%tempWaitTime%', str(tempWaitTime*1000))
        
            finalString=finalString+OnePairScan
            
        if botPositionButton!='' and botPosName!='':
            
            OnePairScan=OnePairScanTemplate
            OnePairScan=str(OnePairScan)
            
            OnePairScan=OnePairScan.replace("%motorWaittime%",  str(motorWaittime*1000))
            OnePairScan=OnePairScan.replace("%topticaTopBarPosition%", topticaTopBarPosition)

            OnePairScan=OnePairScan.replace("%motorPosition%", botPositionButton)

            OnePairScan=OnePairScan.replace('%sampleName%', botPosName)
            OnePairScan=OnePairScan.replace('%field%', targetFieldStr+fieldStr)
            OnePairScan=OnePairScan.replace('%temp%', temp)
            OnePairScan=OnePairScan.replace('%scanIndex%', str(scanIndex))
            OnePairScan=OnePairScan.replace('%scanWaitTime%', str(scanWaitTime*1000))
            #OnePairScan=OnePairScan.replace('%tempWaitTime%', str(tempWaitTime*1000))
        
            finalString=finalString+OnePairScan
  
    
  
    
  
    
  
    
  
    
  
filePath=path+topPosName+midPosName+botPosName+' '+temp+' WholeLoop'+'.ahk'  
    
f = open(filePath,'w',encoding='utf-8-sig')
f.write(header+finalString+footer)
f.close()




print ('Total time in Min',(totalBreakTime+(scanWaitTime+motorWaittime+4)*3*1000*len(scanIndexArray)*(len(fieldList)-1) ) /60000)


print ('Total time in Hours',(totalBreakTime+(scanWaitTime+motorWaittime+4)*3*1000*len(scanIndexArray)*(len(fieldList)-1) ) /60000/60)




