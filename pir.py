#!/usr/bin/env python
 
import sys
import time
import RPi.GPIO as GPIO
from devices import Device, Display
from gpioPinListener import GpioPinListener
from threading import Timer

class Main():
    SHUTOFF_TIME = 30  # seconds
    PIR_LOCK_TIME = 120
    LONG_PRESS_TIME = 2
    pirPin = 17        # Pin 11 on the 
    buttonPin = 3
    lastUserRequestedDisplayOff = 0
    lastMovementDetected = 0
    display = Display()
    device = Device()
    pirLocked = False
    turnOffTimer = None
    pirUnlockTimer = None

    def shortPress(self):
        print("Button was pressed")
        self.display.toggle()
        if self.display.isOn:
            self.pirLocked = False        
            self.restartTurnOffTimer()
        else:
            #display shut down by user
            self.pirLocked = True
            self.restartPirLockTimer()
            
    
    def restartPirLockTimer(self):
        if self.pirUnlockTimer:
            self.pirUnlockTimer.cancel()
        self.pirUnlockTimer = Timer(self.PIR_LOCK_TIME, lambda:self.setPirLocked(False))
        self.pirUnlockTimer.start()
        
    def restartTurnOffTimer(self):
        if self.turnOffTimer:
            self.turnOffTimer.cancel()
        self.turnOffTimer = Timer(self.SHUTOFF_TIME, self.display.turn_off)
        self.turnOffTimer.start()
            
    def setPirLocked(self, value):
        self.pirLocked = value
    
    def onMovementDetected(self):
        if not self.pirLocked:
            self.display.turn_on()
            self.restartTurnOffTimer()

    def main(self):
        GPIO.setmode(GPIO.BCM)
        
        buttonListener = GpioPinListener(
            self.buttonPin,
            onLongPress=self.device.shutdown,
            onShortPress=self.shortPress,
            onFallingEdge=None,
            onRisingEdge=None,
            shutdown=self.LONG_PRESS_TIME,
            debounce=0.01,
            pull_up_down=GPIO.PUD_UP,
            use_internal_pull=True
        )

        pirListener = GpioPinListener(
            self.pirPin,
            onLongPress=None,
            onShortPress=None,
            onFallingEdge=None,
            onButtonDown=self.onMovementDetected,
            shutdown=self.SHUTOFF_TIME,
            debounce=0.01,
            pull_up_down=GPIO.PUD_DOWN,
            use_internal_pull=False
        )
        self.display.turn_off()    
        while True:
            buttonListener.update()
            pirListener.update()
            time.sleep(.1)
        
if __name__ == '__main__':
    try:
        Main().main()
    except KeyboardInterrupt:
        GPIO.cleanup()
