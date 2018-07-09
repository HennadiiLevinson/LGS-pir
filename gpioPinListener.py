#!/usr/bin/python
# shutdown/reboot(/power on) Raspberry Pi with pushbutton

import RPi.GPIO as GPIO

from datetime import datetime
import time

def set(value, default):
    return value if value else default

class GpioPinListener():  
    def __init__(self, pin, onButtonDown=None, onButtonUp=None, onLongPress=None, onShortPress=None, onFallingEdge=None, onRisingEdge=123,shutdown=2, debounce=0.01, pull_up_down=GPIO.PUD_UP, use_internal_pull=False):
        self.pin = pin
        noneLambda = lambda : None
        self.onButtonDown = set(onButtonDown, noneLambda)
        self.onButtonUp = set(onButtonUp, noneLambda)
        self.onLongPress = set(onLongPress, noneLambda)
        self.onShortPress = set(onShortPress, noneLambda)
        self.onFallingEdge = set(onFallingEdge, noneLambda)
        self.onRisingEdge = set(onRisingEdge, noneLambda)
        self.shutdown = shutdown
        self.debounce = debounce
        self.pull_up_down = pull_up_down
        self.buttonPressedTime = None
        self.elapsed = 0
        if use_internal_pull:
            GPIO.setup(pin, GPIO.IN, pull_up_down=pull_up_down)
        else:
            GPIO.setup(pin, GPIO.IN)
        
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=self._buttonStateChanged)                
        return
    
    
    def update(self):
        if self.buttonPressedTime is not None:
            self.elapsed = (datetime.now() - self.buttonPressedTime).total_seconds()
            if self.elapsed >= self.shutdown:
                self.elapsed = 0
                self.buttonPressedTime = None
                self.onLongPress()
            
    def _buttonStateChanged(self, pin):
        
        if not (GPIO.input(pin)):
            self._onFallingEdgeWrapper()
        else:
            self._onRisingEdgeWrapper()

    def _onFallingEdgeWrapper(self):
        if self.pull_up_down == GPIO.PUD_UP:
            self._onButtonDownWrapper()
        else:
            self._onButtonUpWrapper()
    
    def _onRisingEdgeWrapper(self):
        if self.pull_up_down == GPIO.PUD_UP:
            self._onButtonUpWrapper()
        else:
            self._onButtonDownWrapper()
    
    def _onButtonDownWrapper(self):
        self.onButtonDown()
        if self.buttonPressedTime is None:
            self.buttonPressedTime = datetime.now()
    
    def _onButtonUpWrapper(self):
        self.onButtonUp()
        if self.buttonPressedTime is not None:
            self.buttonPressedTime = None
            if self.elapsed >= self.shutdown:
                a = 10;
            elif self.elapsed >= self.debounce:
                # button pressed for a shorter time, reboot
                self.buttonPressedTime = None
                self.onShortPress()        
                
