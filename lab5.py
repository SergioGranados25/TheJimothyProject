#!/usr/bin/env python3
'''
This module contains a function that continuously calls a function
isObjectDeteced, which return a True if a sensor detects an object
otherwise it returns False.  If isObjectDetected returns a True, then
the avoidObject function is invoked to take action.
'''
DISTANCE_THRESHOLD=30  # distance in cm in which an object is acknowledged to exist

from picar.utils import reset_mcu
from picar import picarx
import time

reset_mcu()
jim = picarx.Picarx()


#****************************************************
#  Modify only the below two functions by replacing *
#  the pass statement.                              *
#****************************************************
def is_object_detected(within_a_distance):
    if jim.get_distance() <= within_a_distance:
         global object_detected
         object_detected = True
         return True

def avoid_object():
     # replace this line with your code
    global object_detected
    while object_detected:
        print(jim.get_distance())
        current_distance = jim.get_distance()
        jim.turn_wheels(-25)
        jim.forward(1)
        if current_distance > 40:
            object_detected = False
            time.sleep(0.8)
            jim.turn_wheels(0)
            jim.forward(1)
            time.sleep(1)
            jim.turn_wheels(20)
            time.sleep(1)
            jim.turn_wheels(0)
            jim.stop()
            
        
        

#*******************************************
#  DO NOT MODIFY ANYTHING BELOW THIS POINT *
#*******************************************
def test_obstacle_sensor():
    
    '''
    Tests the obstacle sensor by continuously printing out
    the object distance detected.
    '''
    try:
        while True:
            print('Object distance:',jim.get_distance())
    except:
        print('Test Ended!')
        

    def main():
    

def go_jim():
    try:
        herbie = Picarx()
        herbie.forward(30)
        while True:
            distance = herbie.get_distance()
            print("distance: ",distance)
            if distance > 0 and distance < 300:
                if distance < 25:
                    herbie.turn_wheels(-35)
                else:
                    herbie.turn_wheels(0)
    finally:
        herbie.forward(0)

