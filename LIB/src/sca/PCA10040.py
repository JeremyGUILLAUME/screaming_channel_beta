import serial
import time

def init_PCA10040(device="/dev/ttyACM0", baudrate=115200, timeout=5, time_div=0, channel=0, plot_=False, power=0):

    ser = _open_serial_port(device, baudrate, timeout)
    #ser.write(b'p1')
    ser.write(b'p%d'%power)
    if plot_==True: print( ser.readline() )
    else: ser.readline()
    if plot_==True: print( ser.readline() )
    else: ser.readline()
    time.sleep(1)

    ser.write(b'a')
    if plot_==True: print( ser.readline() )
    else: ser.readline()
    ser.write(b'%02d\n'%channel)
    if plot_==True: print( ser.readline() )
    else: ser.readline()
    ser.write(b'c')     # start continuous wave

    if time_div != 0:
        ser.write(b'N%d\r\n' % int(time_div) )
        print( ser.readline() )

    return ser 


def send_PCA10040_param(ser, cmd, d, plot_=True):
    if cmd == 'P':
        #o = [ord(d[i]) for i in range(len(d))]
        #s = " ".join(str(o[i]) for i in range(len(o)))
        s = " ".join(str(d[i]) for i in range(len(d)))
        ser.write(b'P')
        ser.write(s.encode())
    elif cmd == 'K':
        #o = [ord(d[i]) for i in range(len(d))]
        #s = " ".join(str(o[i]) for i in range(len(o)))
        s = " ".join(str(d[i]) for i in range(len(d)))
        ser.write(b'K')
        ser.write(s.encode())
    elif cmd == 'N':
        ser.write(b'N%d\r\n' % int(d) )
        if plot_== True:
            print( ser.readline() )


def close_PCA10040(ser):
    ser.write(b'e')     # turn off continuous wave
    _close_serial_port(ser)


def _open_serial_port(device, baudrate, timeout):
    #l.debug("Opening serial port")
    return serial.Serial(device, baudrate, timeout)


def _close_serial_port(ser):
    return ser.close()
