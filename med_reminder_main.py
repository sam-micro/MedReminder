import lcddriver
import time
import RPi.GPIO as GPIO
import schedule

display = lcddriver.lcd()
redLed = 4
yellowLed = 17

lcd_display_time = 60

GPIO.setmode(GPIO.BCM)
GPIO.setup(redLed, GPIO.OUT)
GPIO.setup(yellowLed, GPIO.OUT)

med1_line1 = "Ibuprofen 200mg"
med1_line2 = "2 tablet  Bin A"

def lightFlash():
    while True:
        GPIO.output(redLed, True)
        time.sleep(1)
        GPIO.output(redLed, False)


try:
    lightFlash()
    display.lcd_backlight(0)
    # Reminder 16 character long sentences!
    GPIO.output(redLed, True)
    display.lcd_backlight(0)
    print("Writing to display")
    display.lcd_display_string(med1_line1, 1)
    display.lcd_display_string(med1_line2, 2)
    time.sleep(lcd_display_time)
        
    GPIO.output(redLed, False)
    display.lcd_clear()
    display.lcd_backlight(0)
                
except KeyboardInterrupt:
    print("Cleaning up!")
    display.lcd_clear()
    display.lcd_backlight(0)
    GPIO.cleanup() 
    
