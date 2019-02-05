import serial

port = '/dev/ttyACM0'

ser = serial.Serial(port, 115200, timeout=2)

mode = 1
m1 = 300
m2 = 300

motor_control = str(mode) + ' ' + str(m1) + ' ' + str(m2) + ' '

print(motor_control)

print("- - - - - - - -")

while True:
    ser.write(motor_control.encode())
    print(ser.readline().decode('utf-8'))
