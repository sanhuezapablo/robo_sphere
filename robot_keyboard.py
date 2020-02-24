"""
@author: psanhuez
"""

import sim
from time import sleep
from pynput.keyboard import Key, Listener
from threading import Thread


def on_press(event):
    speed = 4
    if event == Key.up:
        sim.simxSetJointTargetVelocity(clientID, left_motor, speed, sim.simx_opmode_streaming)
        sim.simxSetJointTargetVelocity(clientID, right_motor, speed, sim.simx_opmode_streaming)
        print("Up Key")
    elif event == Key.right:
        sim.simxSetJointTargetVelocity(clientID, left_motor, speed, sim.simx_opmode_streaming)
        sim.simxSetJointTargetVelocity(clientID, right_motor, -speed, sim.simx_opmode_streaming)
        print("Right Key")
    elif event == Key.left:
        sim.simxSetJointTargetVelocity(clientID, right_motor, speed, sim.simx_opmode_streaming)
        sim.simxSetJointTargetVelocity(clientID, left_motor, -speed, sim.simx_opmode_streaming)
        print("Left Key")
    elif event == Key.down:
        sim.simxSetJointTargetVelocity(clientID, left_motor, -speed, sim.simx_opmode_streaming)
        sim.simxSetJointTargetVelocity(clientID, right_motor, -speed, sim.simx_opmode_streaming)
        print("Down Key")
        
def on_release(key):
    sim.simxSetJointTargetVelocity(clientID, left_motor, 0, sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(clientID, right_motor, 0, sim.simx_opmode_streaming)
    
def threaded():
    while True:
        err_code, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID, sensor, sim.simx_opmode_streaming)
        sleep(0.5)
    
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # start a connection

if clientID!=-1:
    print ("Connected to remote API server")
    
    err_code, left_motor = sim.simxGetObjectHandle(clientID,"left_motor", sim.simx_opmode_blocking)
    err_code, right_motor = sim.simxGetObjectHandle(clientID,"right_motor", sim.simx_opmode_blocking)
    err_code, sensor = sim.simxGetObjectHandle(clientID,"sensor", sim.simx_opmode_blocking)
    
    thread = Thread(target = threaded)
    thread.start()
    
    with Listener(
            on_press = on_press, 
            on_release = on_release) as listener:
        listener.join()
else:
    print("Not connected to remote API")