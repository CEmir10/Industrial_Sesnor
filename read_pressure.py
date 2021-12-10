import serial
import time

ESC = '\x1b'

#s = open('test','wb+')

s = serial.Serial(port='/dev/ttyUSB0', baudrate=2400)

# Set unit of measuremnt
def set_unit_of_measurement(unit_value):
    if(unit_value<=2):
        cmd=bytearray(ESC +'c' + str(unit_value), 'utf-8')# bytearray func writes data to serial, utf-8 is used for encoding every character as 8 bits
    print(cmd)
    s.write(cmd)

# Set type of input
def set_type_of_input(input_type):
    if(input_type<=4):
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

# Displays the preset pressure value, in this function for example if we have ESCp05600, we want to display after p
def read_preset_pressure():
    cmd  = bytearray(ESC + 'p', 'utf-8')
    s.write(cmd)
    time.sleep(1)
    rsp = s.read(7)
    pressure_str = rsp[2:]      #reading from tird byte 5 digits                
    pressure = int(pressure_str)
    return pressure

def read_configuration():
    cmd =  bytearray(ESC + 'i', 'utf-8')
    s.write(cmd)
    time.sleep(1)
    rsp_temp = s.read(45)    #we have to read 38 bytes
    rsp = rsp_temp[6:]
    pressure = int(rsp[0:4])
    dead_band = int(rsp[6:9])
    unit = int(rsp[12])
    ctrl_type = int(rsp[14])
    full_scale  = int(rsp[10:14])

    return (pressure, dead_band, full_scale)

def main():
    set_unit_of_measurement(0)
    #set_type_of_input()
    set_dead_band(50)
    set_full_scale(10000)
    min_pressure_set(1000)                  #minimum pressure is 1000
    set_type_of_input(2) 
    digital_out_conf(5000,2000)
    #set_pressure(1001)
    pressure, _, full_scale  =read_configuration()
    print(read_preset_pressure())



if __name__ == '__main__':
    main()