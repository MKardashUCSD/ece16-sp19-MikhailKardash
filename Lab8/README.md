Mikhail Kardash

A12183302

# Lab 8

## Introduction

*This lab requires students to integrate step count into the pipeline, have the LED display step count and heart rate, and integrate the vibration module.*

## Objective 1

1. *The purpose of objective 1 is to implement live tracking of step count.*

a: *See the following output video. The step count isn't perfectly accurate, but it works. The step count is the updating number. Disregard the other console messages.*

*video link: https://www.youtube.com/watch?v=Xi56CB_9r9s*

## Objective 2

1. *The purpose of objective 2 is to send HR and step count to the LED display on the arduino.*

2. *I was successful in implementing additional functionality, see the following video. Disregard the HR, my IR sensors are not set up properly here. It overcounted by a few steps, but we expected it to.*

*video link: https://www.youtube.com/watch?v=w0nWXXfVOAc*


## Objective 3

1. *The purpose of this objective is to integrate the vibration module with the arduino.*

2. *I completed this objective, but we did a different implementation. We have it check for the modulo 5 on the python side, then lead the message with a '^'. The arduino checks if the first character is '^' and vibrates. Here's a video. We also swapped the active/inactive modes so we could test it while it's stationary.*

*video link:  https://www.youtube.com/watch?v=0XOJCCKI-XA*


## Objective 4

1. *This objective requires students to outline a plan to improve the pedometer and HR sensors.*

a. *For the HR, I would have it ignore any point that spikes the heart rate above 180 as that would be impossible given our filtering. Otherwise, the current algorithm is sufficient.*

b. *For the pedometer, the feature extraction needs to be redone. Instead of the current method, I want to use welch and have it extract the top 3 frequency values. One frequency value is not enough.*

## Objective SOLDER

1. *This objective requires students to solder the vibration module to the protoboard.*

2. *See the following image of the soldered vibration module.*

[!vibrate](Images/vibrate.jpg)

## Conclusion

*I successfully completed this lab. The step counter overcounts by a little bit, but this is to be expected since we have very naive feature extraction. The HR sensor still needs to be fixed in place for accurate readings.*