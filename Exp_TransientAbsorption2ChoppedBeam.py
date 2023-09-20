import ControlLaser as las
import ControlChopper as chop
import ControlLockInAmplifier as lock
import ControlConex as Rtransla

import numpy as np

import FileControl 
import time
import matplotlib.pyplot as plt

#############################
# Global parameter
#############################
time_exp=1 # time of experiment in second
nb_loop=2
PhaseChopperProbe=295
PhaseChopperPump=400
MotorId=1 # It can take the value of one or two depanding of which motor we are calibrating

# We define the map dimension in mm
res_xy=0.1;
dx=0.05
dy=0.1

StartingPositionx=5
StartingPositiony=7



FileNameData='DataTransientAbsTwoBeam_'

LockInParaFile='ParameterLockInTA.txt'

GeneralPara={'Experiment name':' PL no move','Exposition duration':time_exp,
             'Number of loop':nb_loop}


InstrumentsPara={}



#############################
# Initialisation of laser
#############################

Laser= las.LaserControl('COM6',2)

InstrumentsPara['Laser']=Laser.parameterDict

#############################
# Initialisation of the Pulse Picker
#############################

#############################
# Initialisation of lock-in amplifier
#############################

LockInDevice=lock.LockInAmplifier(LockInParaFile)

# Set output 1 and two
LockInDevice.SetOutputTA()

print('Set up lock-in output 1 and 2')

InstrumentsPara['Lock-in-amplifier']=LockInDevice.parameterDict

#############################
# Initialisation of Choppers
#############################

Chopper1= chop.OpticalChopper('COM14')
Chopper1.SetInternalFrequency(0)
Chopper1.SetMotorStatus('ON')
Chopper1.WaitForLock(10)
Chopper1.SetPhase(PhaseChopperProbe)
Chopper1.parameterDict['Phase']=PhaseChopperProbe

InstrumentsPara['ChopperProbe']=Chopper1.parameterDict


Chopper1= chop.OpticalChopper('COM14')
Chopper1.SetInternalFrequency(0)
Chopper1.SetMotorStatus('ON')
Chopper1.WaitForLock(10)
Chopper1.SetPhase(PhaseChopperPump)
Chopper1.parameterDict['Phase']=PhaseChopperPump

InstrumentsPara['ChopperPump']=Chopper1.parameterDict


#############################
# Conex Controller initialisation
#############################

# We then initalize the axis
#print('Initialisation of z the axis')
#z_axis=ControlConex.ConexController('COM5')
print('Initialisation of x the axis')
x_axis=Rtransla.ConexController('COM3')
print('Initialisation of y the axis')
y_axis=Rtransla.ConexController('COM4')

#For the moment I just place myself at the middle
x_axis.MoveTo(StartingPositionx)
y_axis.MoveTo(StartingPositiony)

# We define the position list
x=np.arange(x_axis.Pos,x_axis.Pos+dx,res_xy)
y=np.arange(y_axis.Pos,y_axis.Pos+dy,res_xy)

#############################
# Preparation of the directory
#############################

DirectoryPath=FileControl.PrepareDirectory(GeneralPara,InstrumentsPara)

#############################
# Acquisition loop
#############################
print('Begin acquisition')

StartingPosition=np.linspace(1,11,50)
Speedx=np.linspace(1,11,50)
lengthLine=3

temp_iterator=np.nditer(StartingPosition, flags=['f_index'])

print("Everything is ready")

Laser.StatusShutterTunable(1)
for k in  temp_iterator:
    Laser.StatusShutterTunable(1)
    time.sleep(2)
    Rtransla.MoveLine1D(x_axis,k,k+lengthLine,Speedx[temp_iterator.index])
    y.Move(k)
    Laser.StatusShutterTunable(0)




      
