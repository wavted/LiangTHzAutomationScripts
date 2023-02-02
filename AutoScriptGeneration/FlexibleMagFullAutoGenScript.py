 # -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 10:04:10 2022

@author: Will
"""

import re
import numpy as np


topPosName = 'SAM'
midPosName = 'SUB'
botPosName= ''
fieldStr = 'kG'
temp = '30'
# =============================================================================
# for room temp stick 
# topPositionButton='1566, 696'
# midPositionButton='1711, 696'
# botPositionButton='1853, 696'
# =============================================================================

#for low temp stick
#the cordinates of top/mid/bot stick change button of labview program
topPositionButton='1682, 687'
midPositionButton='1821, 687'
botPositionButton=''
topticaTopBarPosition='313, 11'



#the rightmost part of the field entry text box (needs to be towards the right end so that the previous number gets deleted)
fieldSetWindowPos='1117, 1021'
# the field ramp button 
fieldSetButtonPos='1271, 1021'
# somewhere blank in the field settings labview window. Used to reset the textbox
fieldSetBlankPos='1183,1021'



zeroToTenRamp=0.01
#zeroToTenRamp=0.016
tenToSevenRamp=0.016
#tenToSevenRamp=0.023

#tempWaitTime=12
scanIndexArray=np.arange(5)+1
scanTime=14.2
#scanTime=47
motorWaittime=6.4

scanWaitTime=scanTime+2


#the first element of field list array should be the field you are currently on, 
#the second element is the first field you want to go to, and continue from there.
#in the example here, the program will not measure at '0' field
#if the first and second element is the same, the program will not set field and will immedietly start measuring at this field, after it is done, it will ramp to the third number
fieldList=['0','65','50','40','30','20','10','0','-10','-20','-30','-40','-50','-65','-0']

#floating point fields also works, the files will be automatically saved as 0p01 for 0.01 since toptica does not take decimals
#only use floating point numbers or integers in the fieldList array
#fieldList=['0','0.01','0.02']



path='../'






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

    
    currentFieldStr=fieldList[i].replace('.', 'p')
    targetFieldStr=fieldList[i+1].replace('.', 'p')
    
    currentField=float(fieldList[i])
    targetField=float(fieldList[i+1])
    
    
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




print ('Total time in Min',(totalBreakTime+(scanWaitTime+motorWaittime+4.3)*3*1000*len(scanIndexArray)*(len(fieldList)-1) ) /60000)


print ('Total time in Hours',(totalBreakTime+(scanWaitTime+motorWaittime+4.3)*3*1000*len(scanIndexArray)*(len(fieldList)-1) ) /60000/60)




