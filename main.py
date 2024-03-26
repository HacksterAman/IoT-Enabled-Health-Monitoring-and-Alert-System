import network
import machine, onewire, max30100
from machine import Pin, PWM, I2C
from time import sleep, sleep_us
from writer import Writer
import freesans20
import sh1106
import BlynkLib

# WiFi credentials
ssid = "Aman197"
key = "ushaaman"

# Blynk settings
BLYNK_AUTH = '2Z1G4_RNkweqHINWDcFMBoN_6ZDozadY'

# Global variables for sensor readings
heartrate = "0"
spo2 = "0"
level = "0"

# IV Bag config
capacity = 1000 #1000ml iv bag
alert_level = 10 #alert_level at 10%
alert = False
interrupt = True

# I2C config
sda=Pin(21)
scl=Pin(22)          
i2c = I2C(scl=scl,sda=sda)

# Display config
oled_width = 128
oled_height = 64
oled = sh1106.SH1106_I2C(oled_width, oled_height, i2c)
font = Writer(oled, freesans20)

# Heartrate and SpO2 Sensor config
sensor = max30100.MAX30100(i2c=i2c)
sensor.enable_spo2()

# Load Cell config
hx711_dt = Pin(19, Pin.IN) 
hx711_sck = Pin(18, Pin.OUT)

# Initialize the led
led = Pin(2, Pin.OUT)

# Initialize the buzzer
buzzer = Pin(23, Pin.OUT)

# Initialize the button
button = Pin(5, Pin.IN, Pin.PULL_UP)

# Function to read button press
def read_button():
    if button.value():
        while button.value():
            pass
        print("Button Pressed")
        return True
    else:
        return False
    
# Function to connect to network
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, key)
        while not sta_if.isconnected():
            pass
    led.on()
    print('Connected to network')

# Function to print lines on the display
def printlines(lines):
    font.printstring(lines)
    oled.show()
    Writer.set_textpos(0, 0)

# Function to clear the display
def clear():
    oled.fill(0)
    oled.show()

# Function to read Heart Rate and SpO2 Sensor
def read_max30100():
    sensor.read_sensor()
    rawspo2 = sensor.ir
    rawheartrate = sensor.red
    spo2 = rawspo2/100
    if spo2 >100:
        spo2 = 100
    heartrate = rawheartrate/200

    return str(round(spo2)), str(round(heartrate))    
 
# Function to read Load Cell Sensor
def read_hx711():
    hx711_sck.value(0)  # Start by setting the SCK pin to low
    count = 0
    # Wait for the DT to go low to indicate that the HX711 is ready to send data
    while hx711_dt.value() == 1:
        pass

    # Read 24-bit data from HX711
    for i in range(24):
        hx711_sck.value(1)
        count = count << 1
        hx711_sck.value(0)
        if hx711_dt.value() == 0:
            count += 1

    # Set the channel and gain factor for next reading
    hx711_sck.value(1)
    sleep_us(1)
    hx711_sck.value(0)
    
    # Adjust the 24-bit two's complement
    if count & 0x800000:  # if the 24th bit is set, this is a negative number
        count -= 0x1000000

    return count

# Function to monitor IV Bag
def ivbag():
    global capacity, alert_level, alert, interrupt
    weight = round((read_hx711() + 148000)/350)
    
    if weight>=capacity:
        level = 100
    elif weight<0:
        level = 0
    else:
        level = round(weight/capacity*100)
    if level>alert_level:
        interrupt=False
        alert = False
        buzzer.off()
        
    elif level<=alert_level and not interrupt:
        buzzer.on()
    
    if read_button():
        buzzer.value(interrupt)
        interrupt = not interrupt
        
    return str(weight), str(level)

# Function to send data to Blynk
def send_to_blynk():
    blynk.virtual_write(0, level)
    blynk.virtual_write(1, heartrate)
    blynk.virtual_write(2, spo2)

# Network and Server Connection Initialization
clear()
printlines("   Connecting\n         WIFI\n            ...")
do_connect()
led.on()
clear()
printlines("         WIFI\n   Connected\n            ...")
sleep(1)
clear()
printlines("   Connecting\n       Server\n            ...")
blynk = BlynkLib.Blynk(BLYNK_AUTH)
clear()
printlines("       Server\n   Connected\n            ...")
clear()

# Main Loop
while True:
    led.off()
    spo2, heartrate = read_max30100()
    weight, level = ivbag()
    print(f"SpO2: {spo2}%\tHeartrate: {heartrate}bpm\t\tIV Bag: {weight}gm/{level}%")
    printlines(f"Heartrate: {heartrate}{" "*(4-len(heartrate))}\nSpO2: {spo2}{" "*(5-len(spo2))}\nIV Bag: {level}%{" "*(4-len(level))}")
    try:
        blynk.run()
        send_to_blynk()
    except:
        pass
    led.on()

