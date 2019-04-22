# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 11:21:52 2019

@author: Michael K
"""

#1
com = ["AT", "AT+IMME1", "AT+NOTI1", "AT+ROLE1"]

#2
for x in com:
    print(x)

#3
wut = ["CONNECTION FAILURE", "BANANAS", "CONNECTION SUCCESS", "APPLES"]

#4
text = "SUCCESS"

#5
if "SUCCESS" in "SUCCESS":
    print(1)

if "SUCCESS" in "ijoisafjoijiojSUCESS":
    print(2)
    
if "SUCCESS" == "ijoisafjoijiojSUCESS":
    print(3)
    
if "SUCCESS" == text:
    print(4)

if "SUCC" == text: #will  not print 5, so == compares whole thing
    print(5)


#6
n = len(wut)
i = 0
while (i < n):
    if text in wut[i]:
        print("This worked!")
    else:
        print(wut[i])
    i = i + 1