# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 10:48:35 2019

@author: Michael K
"""

#1
list_1 = list(range(1,11))

#2
list_2 = []
for x in list_1:
    list_2.append(float(x) + 10.0)

#3
list_1[0] = "one"
list_1[1] = "two"
list_1[2] = "three"
print(list_1)

#4
temp = ('eleven', 'twelve', 'thirteen')
list_2[0:3] = temp
print(list_2)

#6
joint_1 = list_1.extend(list_2)

#7
joint_2 = list_1 + list_2
print(joint_2)

#8
a = [1,2,3,4]
b = [5,6,7]

def list_shift(base_list, new_data):
    temp = base_list + new_data
    n = len(temp)
    m = len(base_list)
    for i in range(0,m):
        base_list[m-i-1] = temp[n-i-1]
    return base_list


list_shift(a,b)

print(a)