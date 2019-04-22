# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 11:33:06 2019

@author: Michael K
"""
#1
name = "Mikhail"

#2
byte_name = name.encode('utf-8')

#3
byte_name_bad = byte_name + b'\xef'

#4
byte_name.decode('utf-8')

#5
def decoder(a):
    try:
        a.decode('utf-8')
        return a.decode('utf-8')
    except UnicodeDecodeError:
        return ""

#6
print(decoder(byte_name_bad))
print(decoder(byte_name))
