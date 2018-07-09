from subprocess import call

class Device():
    def __init__(self):
        return
    
    def shutdown(self):
        print("Shut down mock uncomment!")
        call(['shutdown', '-h', 'now'], shell=False)
    

class Display():
    
    def __init__(self):
        self.isOn = True
    
    def toggle(self):
        if self.isOn:
            self.turn_off()
        else:
            self.turn_on()
    
    def turn_on(self):
        if not self.isOn:
            self.isOn = True
            print("turn on")
            call("sh monitor_on.sh", shell=True)
     
    def turn_off(self):
        if self.isOn:
            self.isOn = False
            print("turn off")
            call("sh monitor_off.sh", shell=True)

