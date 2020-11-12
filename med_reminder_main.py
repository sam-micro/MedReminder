import lcddriver
import time
import RPi.GPIO as GPIO
import schedule

display = lcddriver.lcd()
redLed = 4
yellowLed = 17

lcd_display_time = 60

GPIO.setmode(GPIO.BCM)
GPIO.setup(redLed,GPIO.OUT)
GPIO.setup(yellowLed,GPIO.OUT)
GPIO.setup(buzzerPIN,GPIO.OUT)
GPIO.setup(buttonPIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)

buzzer = GPIO.PWM(buzzerPIN,1000)

med1_line1 = "Ibuprofen 200mg"
med1_line2 = "2 tablet  Bin A"
med2_line1 = "Lisinopril 20mg"
med2_line2 = "1 tablet  Bin B"
med3_line1 = "Famotidine 20mg"
med3_line2 = "1 tablet  Bin C"
med4_line1 = "Aspirin 81mg"
med4_line2 = "1 tablet  Bin D"

msg_line1 = "All done now!"
msg_line2 = "Keep it up!"

def light_buzz():
    print("light on")
    GPIO.output(redLed, True)
    time.sleep(1)
    print("light off")
    GPIO.output(redLed, False)
    time.sleep(1) 
    buzzer.start(10)
    print("buzz")
    time.sleep(buzzer_time)
    buzzer.stop()

def goodjob_msg():
    display.lcd_clear()
    display.lcd_display_string(msg_line1, 1)
    display.lcd_display_string(msg_line2, 2)
    time.sleep(5)  
    print("Cleaning up!")
    display.lcd_clear()
    display.lcd_backlight(0)

def loop_cleanup():
    display.lcd_clear()
    print("Finally cleaning up!")
    display.lcd_backlight(0)

def morning_alert():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(redLed,GPIO.OUT)
    GPIO.setup(yellowLed,GPIO.OUT)
    GPIO.setup(buzzerPIN,GPIO.OUT)
    GPIO.setup(buttonPIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)    
    try:
        while True:
            button_state = GPIO.input(buttonPIN)
            if button_state == True:
                light_buzz()

            else:
                GPIO.cleanup(buzzerPIN)
                GPIO.cleanup(redLed)
                time.sleep(2)

                display.lcd_backlight(0)
                print("Writing to display")
                display.lcd_display_string(med1_line1, 1)
                display.lcd_display_string(med1_line2, 2)
                GPIO.wait_for_edge(buttonPIN,GPIO.FALLING)

                time.sleep(1)
                display.lcd_clear()
                display.lcd_display_string(med2_line1, 1)
                display.lcd_display_string(med2_line2, 2)
                GPIO.wait_for_edge(buttonPIN,GPIO.FALLING)

                time.sleep(1)
                display.lcd_clear()
                display.lcd_display_string(med3_line1, 1)
                display.lcd_display_string(med3_line2, 2)
                GPIO.wait_for_edge(buttonPIN,GPIO.FALLING)

                print("Cleaning up!")
                display.lcd_clear()
                display.lcd_backlight(0)

                goodjob_msg()

                break
    
    finally:
        loop_cleanup()
        
def evening_alert():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(redLed,GPIO.OUT)
    GPIO.setup(yellowLed,GPIO.OUT)
    GPIO.setup(buzzerPIN,GPIO.OUT)
    GPIO.setup(buttonPIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    try:
        while True:
            button_state = GPIO.input(buttonPIN)
            if button_state == True:
                light_buzz()

            else:
                time.sleep(2)
                
                display.lcd_backlight(0)
                print("Writing to display")
                
                time.sleep(1)
                display.lcd_clear()
                display.lcd_display_string(med4_line1, 1)
                display.lcd_display_string(med4_line2, 2)
                GPIO.wait_for_edge(buttonPIN,GPIO.FALLING)

                goodjob_msg()

                break
    finally:
        loop_cleanup()


schedule.every().day.at('09:00').do(morning_alert)
schedule.every().day.at('20:00').do(evening_alert)

while True:
    schedule.run_pending()
    time.sleep(1)
    GPIO.cleanup()
