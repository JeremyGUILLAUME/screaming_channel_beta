import numpy as np

from ctypes import cdll, CDLL, c_long, c_int, c_float, c_double, c_char_p, create_string_buffer, byref, c_uint
import time
import datetime
import os
import sys

bb_api = CDLL('libbb_api.so.5.0.5')

def connect_device(target_freq=2.464e9): 

    deviceHandle = c_int()
    print( "Openning device.." )
    openStatus = bb_api.bbOpenDevice( byref( deviceHandle )  )
    print( "openStatus = %s; handle = %s" % ( openStatus, deviceHandle )  )

    serialNumber	= c_uint()
    openStatus = bb_api.bbGetSerialNumber(deviceHandle, byref( serialNumber) )
    print serialNumber

    print( "\nConfiguring device.." )

    freq_center = c_double(target_freq)
    span_ = c_double(20000000)
    bandwidth_ = c_double(3750000)

    openStatus = bb_api.bbConfigureCenterSpan( deviceHandle, freq_center, span_)
    print( "openStatus = %s; handle = %s" % ( openStatus, deviceHandle )  )

    openStatus = bb_api.bbConfigureLevel( deviceHandle, -20, -1) #BB_AUTO_ATTEN
    print( "openStatus = %s; handle = %s" % ( openStatus, deviceHandle )  )

    openStatus = bb_api.bbConfigureGain( deviceHandle, 3) #BB_AUTO_GAIN
    print( "openStatus = %s; handle = %s" % ( openStatus, deviceHandle )  )

    openStatus = bb_api.bbConfigureIQ( deviceHandle, 8, bandwidth_) #8
    print( "openStatus = %s; handle = %s" % ( openStatus, deviceHandle )  )

    openStatus = bb_api.bbConfigureIO(deviceHandle, 0, 0)
    print( "openStatus = %s; handle = %s" % ( openStatus, deviceHandle )  )

    openStatus = bb_api.bbInitiate(deviceHandle, 4, 0)
    print( "openStatus = %s; handle = %s" % ( openStatus, deviceHandle )  )

    return deviceHandle

def change_freq(deviceHandle, target_freq):
    freq_center = c_double(target_freq)
    span_ = c_double(20000000)
    bandwidth_ = c_double(3750000)

    openStatus = bb_api.bbConfigureCenterSpan( deviceHandle, freq_center, span_)
    openStatus = bb_api.bbConfigureLevel( deviceHandle, -20, -1) #BB_AUTO_ATTEN
    openStatus = bb_api.bbConfigureIQ( deviceHandle, 8, bandwidth_) #8
    openStatus = bb_api.bbConfigureIO(deviceHandle, 0, 0)
    openStatus = bb_api.bbInitiate(deviceHandle, 4, 0)

def get_data(deviceHandle, size):
    iqCount 	= c_int(size)
    iqData	 = (c_float * (size*2))(0)
    triggers	 = (c_int * (size*2))(0)
    triggerCount = c_int(0)
    purge	 = c_int(1)
    dataRemaining = c_int()
    sampleLoss	  = c_int()
    sec		  = c_int()
    nano	  = c_int()

    openStatus = bb_api.bbGetIQUnpacked( deviceHandle, 
					 byref(iqData), 
					 iqCount, 
				 	 byref( triggers ), 
                        		 triggerCount, 
					 purge, 
					 byref( dataRemaining ), 
                        		 byref( sampleLoss ), 
					 byref( sec ), 
					 byref( nano ) )
    Data = []
    for i in range(size):
        Data.append( np.absolute(iqData[i*2] + iqData[i*2 + 1]*1j) )
    return Data

def disconnect_device(deviceHandle):
    print( "Disconnecting!")
    openStatus = bb_api.bbCloseDevice( deviceHandle )
    print( "openStatus = %s; handle = %s" % ( openStatus, deviceHandle )  )








