import serial
import time
import matplotlib.pyplot as plt


ESC = '\x1b'

#s = open('test','wb+')

s = serial.Serial(port='/dev/ttyUSB0', baudrate=2400)

# Set unit of measuremnt
def set_unit_of_measurement(unit_value):
    #if(unit_value<=2):
    cmd=bytearray(ESC +'c' + str(unit_value), 'utf-8')# bytearray func writes data to serial, utf-8 is used for encoding every character as 8 bits
    print(cmd)
    s.write(cmd)

# Set type of input
def set_type_of_input(input_type):
    
    cmd=bytearray(ESC +'d' + str(input_type), 'utf-8')
    print(cmd)
    s.write(cmd)

# Set deadband(indicates the pressure range in proximity to set pressure), value expressed in mbar
def set_dead_band(dead_band_val_mbar):
    cmd = bytearray(ESC +'b' + str(dead_band_val_mbar).zfill(3), 'utf-8')
    print (cmd)
    s.write(cmd)

# Set full scale, value expressed in mbar
def  set_full_scale(full_scale_mbar):
    cmd = bytearray(ESC + 'E' + str(full_scale_mbar).zfill(5), 'utf-8' )
    print(cmd)
    s.write(cmd)

# Minimum pressure set, the minimum pressure set is 1000mbar
def min_pressure_set(min_press_mbar):
    cmd=bytearray(ESC + 'e' + str(min_press_mbar).zfill(5),'utf-8')
    print(cmd)
    s.write(cmd)

# Sets the type of digital output
def digital_out_conf(activation_value, deactivation_value):
    cmd=bytearray(ESC + 'O'+ '1' +str(activation_value).zfill(5)+str(deactivation_value).zfill(5),'utf-8')
    print(cmd)
    s.write(cmd)

# Set pressure
def  set_pressure(pressure_value):
    cmd = bytearray(ESC + 'P' + str(pressure_value).zfill(5), 'utf-8' )
    print(cmd)
    s.write(cmd)

# Displays the preset pressure value, read what we set with set_pressure function
def read_preset_pressure():
    cmd  = bytearray(ESC + 'p', 'utf-8')
    s.write(cmd)
    time.sleep(1)
    rsp_temp = s.read_all().decode('utf-8')
    rsp = rsp_temp.lstrip('\x11')
    pressure_str = rsp[2:]      #reading from tird byte 5 digits                
    pressure = int(pressure_str)
    return pressure

def read_configuration():
    cmd =  bytearray(ESC + 'i', 'utf-8')
    s.write(cmd)
    time.sleep(1)
    rsp_temp = s.read_all().decode('utf-8')    #we have to read 46 bytes
    rsp = rsp_temp.lstrip('\x11')
    pressure = int(rsp[2:7])
    dead_band = int(rsp[8:11])
    unit = int(rsp[12:13])
    ctrl_type = int(rsp[14:15])
    full_scale  = int(rsp[16:21])
    type_ofoutput=int(rsp[22:23])
    out_act_tresshold=int(rsp[24:28])
    out_deact_tersshold=int(rsp[29:33])
    min_pressure=int(rsp[35:39])
    return (pressure, dead_band, unit, ctrl_type, full_scale)

"""def measure():
        n=5
        while(n>0):
            print(read_preset_pressure())
            time.sleep(2) """   


def main():
    set_unit_of_measurement(0)
    set_type_of_input(4)
    set_dead_band(100)
    set_full_scale(10000)
    min_pressure_set(500)                  #minimum pressure is 1000
    pressure_set, _, _, _, _ = read_configuration()

    i = 0
    while(True):

        
        set_pressure(i*500)
        time.sleep(2)
         #measure()
        data=read_preset_pressure()
        print(read_preset_pressure())

        i += 0.5
        if(i > 14):
            plt.plot(data)
            plt.show()
            i = 0
        time.sleep(2)           


if __name__ == '__main__':
    main()