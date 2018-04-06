
import serial
import time

# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = '/dev/tty.usbserial-A907CAHB'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 115200


def main():
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
    time.sleep(5)
    ser.write('1')
    ser.write('\r\n')
    ser.write('60')
    ser.write('\r\n')
    start = time.time()

    while True:
        # using ser.readline() assumes each line contains a single reading
        # sent using Serial.println() on the Arduino
        reading = ser.readline().decode('utf-8')
        # reading is a string...do whatever you want from here
        print(reading)
        end = time.time()
        ser.flush()
        elapsed = int(end)-int(start)
        print(elapsed)
        if(elapsed == 14):
            ser.write('0')
            ser.write('\r\n')
            ser.close()
            break


if __name__ == "__main__":
    main()