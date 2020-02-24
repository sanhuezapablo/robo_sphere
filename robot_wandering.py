"""
@author: psanhuez
"""

import sim
import time
import numpy as np
import random

def obstacle_detect(distance):
    if distance < 0.35:
        obstacle = True
    else:
        obstacle = False
        
    return obstacle

def move_forward(speed):
    sim.simxSetJointTargetVelocity(clientID,left_motor,speed,sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(clientID,right_motor,speed,sim.simx_opmode_streaming)
    print("Moving Forward")
    
def avoid_obstacle(speed, d):
    
    print("Avoiding Obstacle...")
    rand = random.randint(0,1)
    
    while obstacle_detect(d) == True:
            
        if (rand == 1):
            sim.simxSetJointTargetVelocity(clientID,left_motor,speed,sim.simx_opmode_streaming)
            sim.simxSetJointTargetVelocity(clientID,right_motor,0,sim.simx_opmode_streaming)
            
        else:
            sim.simxSetJointTargetVelocity(clientID,left_motor,0,sim.simx_opmode_streaming)
            sim.simxSetJointTargetVelocity(clientID,right_motor,speed,sim.simx_opmode_streaming)
            
        err_code,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID,sensor,sim.simx_opmode_buffer)
        d = np.linalg.norm(detectedPoint)
        
def robot_move():
    
    while True:
    
        err_code,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=sim.simxReadProximitySensor(clientID,sensor,sim.simx_opmode_streaming)
        d = np.linalg.norm(detectedPoint)
        
        if obstacle_detect(d) == True:
            avoid_obstacle(5, d)
        else:
            move_forward(5)
        
        time.sleep(0.3)
        err_code,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID,sensor,sim.simx_opmode_buffer)

        

sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # start a connection

if clientID!=-1:
    print ("Connected to remote API server")
    
    err_code, left_motor = sim.simxGetObjectHandle(clientID,"left_motor", sim.simx_opmode_blocking)
    err_code, right_motor = sim.simxGetObjectHandle(clientID,"right_motor", sim.simx_opmode_blocking)
    err_code, sensor = sim.simxGetObjectHandle(clientID,"sensor", sim.simx_opmode_blocking)
    
    err_code, sensor = sim.simxGetObjectHandle(clientID,"sensor", sim.simx_opmode_blocking)
    err_code, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector=sim.simxReadProximitySensor(clientID,sensor,sim.simx_opmode_streaming)

    robot_move()

else:
    print("Not connected to remote API")
    