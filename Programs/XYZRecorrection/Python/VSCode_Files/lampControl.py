from kasa import SmartPlug

lamp = SmartPlug("") #IP of b1172 wifi enabled plug
lamp.update()
def lampEnable():
    lamp.turn_on()
def lampDisable():
    lamp.turn_off()
