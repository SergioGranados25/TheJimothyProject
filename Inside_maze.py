'''
PiCar-X Driving Lab 7
This module contains functions that move the robot in square pattern.
'''
from picar.utils import reset_mcu
from picar import picarx
import time

reset_mcu()
herbie = picarx.Picarx()

STARTING_SPEED = 50
line_value = herbie.get_line_sensor_values()
speed = 75
angle = 2
movement = (speed,angle)
last_angle = movement[1]
last_speed = movement[0]
new_line_value = [0,0,0]

active = False
all_white = False
all_black =False
object_detected = False
object_detected_1= False

def get_line_sensor_values(cut_off):
    '''
    Read the line sensor values and use the cut_off value to return a list
    where each element is either 0 for black or 1 for white.
    '''
    global new_line_value
    global line_value
    line_value = herbie.get_line_sensor_values()
    for value in range(len(line_value)):
        if line_value[value] <= cut_off:
            new_line_value[value] = 0
        else:
            new_line_value[value] = 1
    print(new_line_value)
def get_line_controls():
    '''
    Read line sensor and return a two tuple with the first element the speed
    and the second element the turn angle ie (speed, angle).
    '''
    get_line_sensor_values(800)
    global last_angle
    global last_speed
    if new_line_value[0] == 1 and new_line_value[1] == 0 and new_line_value[2] == 0:
        speed = 1
        angle = -5
    if new_line_value[0] == 0 and new_line_value[1] == 0 and new_line_value[2] == 1:
        speed = 1
        angle = -25
    if new_line_value[0] == 1 and new_line_value[1] == 1 and new_line_value[2] == 0:
        speed = 1
        angle = 12
    if new_line_value[0] == 0 and new_line_value[1] == 0 and new_line_value[2] == 0:
        speed = 1
        angle = -25
    if new_line_value[0] == 0 and new_line_value[1] == 1 and new_line_value[2] == 1:
        speed = 1
        angle = -25
    if new_line_value[0] == 1 and new_line_value[1] == 1 and new_line_value[2] == 1:
        speed = last_speed
        angle = last_angle
    if new_line_value[0] == 1 and new_line_value[1] == 0 and new_line_value[2] == 1:
        speed = 1
        angle = 0
    if new_line_value[0] == 0 and new_line_value[1] == 1 and new_line_value[2] == 0:
        speed = 1
        angle = 0
    global movement
    
    movement = (speed,angle)
    last_angle = movement[1]
    last_speed = movement[0]
    


def follow_line():
    '''
    Continuosly steers the PiCar-X until no line is detected, where by
    the function exits.
    '''
    get_line_sensor_values(800)
    
    
    
    if (new_line_value[0] == 0 and new_line_value[1] == 1 and new_line_value[2] == 1)or(new_line_value[0] == 1 and new_line_value[1] == 1 and new_line_value[2] == 1)or(new_line_value[0] == 0 and new_line_value[1] == 0 and new_line_value[2] == 0)or(new_line_value[0] ==1 and new_line_value[1] == 0 and new_line_value[2] == 0) or (new_line_value[0] == 0 and new_line_value[1] == 0 and new_line_value[2] == 1) or (new_line_value[0] == 1 and new_line_value[1] == 1 and new_line_value[2] == 0):
        global active
        active = True
        
    while active:
        print('active')
        get_line_controls()
        herbie.turn_wheels(movement[1])
        herbie.forward(movement[0])
        #detects object
        distance = herbie.get_distance()  
        if distance > 0 and distance < 300:
            if distance < 18.5:
                print('object detected')
                global object_detected
                object_detected = True
                if object_detected:
                    print('Object detected')
                    herbie.turn_wheels(-30)
                    herbie.forward(1)
                    time.sleep(0.75)
                    herbie.turn_wheels(30)
                    time.sleep(0.75)
                    global object_detected_1
                    object_detected_1 =True
                    object_detected = False
                while object_detected_1:
                        get_line_controls()
                        herbie.forward(1)
                        herbie.turn_wheels(5)
                        
                        if(new_line_value[0] == 0 and new_line_value[1] == 1 and new_line_value[2] == 1)or(new_line_value[0] == 0 and new_line_value[1] == 0 and new_line_value[2] == 0)or(new_line_value[0] ==1 and new_line_value[1] == 0 and new_line_value[2] == 0) or (new_line_value[0] == 0 and new_line_value[1] == 0 and new_line_value[2] == 1) or (new_line_value[0] == 1 and new_line_value[1] == 1 and new_line_value[2] == 0):
                            object_detected_1 = False
                        
            #object_detected = True
            
        #if Jim goes off line
        if new_line_value[0] == 1 and new_line_value[1] == 1 and new_line_value[2] == 1:
            global all_white
            all_white = True
            startTime = time.time()
            while all_white:
                get_line_controls()
                if(new_line_value[0] == 0 and new_line_value[1] == 0 and new_line_value[2] == 0)or(new_line_value[0] ==1 and new_line_value[1] == 0 and new_line_value[2] == 0) or (new_line_value[0] == 0 and new_line_value[1] == 0 and new_line_value[2] == 1) or (new_line_value[0] == 1 and new_line_value[1] == 1 and new_line_value[2] == 0):
                    all_white = False
                endTime = time.time()
                if(endTime - startTime > 2):
                    herbie.stop()
                    herbie.turn_wheels(0)
                    all_white = False
                    active = False
        
         # if Jim reaches right angle           
        if new_line_value[0] == 0 and new_line_value[1] == 0 and new_line_value[2] == 0:
            global all_black
            all_black = True
            herbie.stop()
            time.sleep(0.5)
            while all_black:
                get_line_sensor_values(800)
                herbie.turn_wheels(0)
                herbie.forward(1)
                time.sleep(0.5)
                if new_line_value[0] == 1 and new_line_value[1] == 1 and new_line_value[2] == 1:
                    herbie.stop()
                    time.sleep(0.1)
                    herbie.backward(1)
                    time.sleep(0.5)
                    left_turn()
                    all_black = False
                    
                
def avoid_object():
    global object_detected
    object_detected = True
    active = True
    herbie.turn_wheels(-15)


def left_turn():
    herbie.turn_wheels(-30)
    herbie.forward(1)
    time.sleep(1)
    herbie.turn_wheels(30)
    herbie.backward(1)
    time.sleep(1)
    herbie.stop()
    herbie.turn_wheels(0)
        
def test_1():
    global active
    active = True
    herbie.turn_wheels(-30)
    herbie.forward(1)
    time.sleep(0.75)
    herbie.turn_wheels(30)
    time.sleep(0.75)
    global object_detected_1
    object_detected_1 =True
    while object_detected_1:
        get_line_sensor_values(800)
        herbie.forward(1)
        herbie.turn_wheels(25)
        time.sleep(0.5)
        herbie.turn_wheels(0)
        time.sleep(1)
        if(new_line_value[0] == 0 and new_line_value[1] == 1 and new_line_value[2] == 1)or(new_line_value[0] == 0 and new_line_value[1] == 0 and new_line_value[2] == 0)or(new_line_value[0] ==1 and new_line_value[1] == 0 and new_line_value[2] == 0) or (new_line_value[0] == 0 and new_line_value[1] == 0 and new_line_value[2] == 1) or (new_line_value[0] == 1 and new_line_value[1] == 1 and new_line_value[2] == 0):
            break
            
    
    active = True
    follow_line()
        
        
        
        
        
        
        
#*******************************************
#  DO NOT MODIFY ANYTHING BELOW THIS POINT *
#******************************************
def test_line_sensor():
    try:
        while True:
            print('Line Sensor values:',herbie.get_line_sensor_values())
    except:
        pass


def go_bot():
    try:
        follow_line()
    except Exception as e:
        print(e)
    finally:
        herbie.stop()
        herbie.turn_wheels(0)