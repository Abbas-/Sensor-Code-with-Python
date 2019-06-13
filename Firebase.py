import RPi.GPIO as GPIO
import firebase_admin
import time
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
from time import sleep

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection('Ayarlar').document('cYYQMtJxdi4sIGTvZ5u0')

class Light():
    value=""
    oldvalue=""
class Curtain():
    value=""
    oldvalue=""
class Heater():
    value=""
    oldvalue=""

def LightOn():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11,GPIO.OUT)
    GPIO.setup(12,GPIO.OUT)
    GPIO.output(11,GPIO.HIGH)
    GPIO.output(12,GPIO.HIGH)

def LightOff():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11,GPIO.OUT)
    GPIO.setup(12,GPIO.OUT)
    GPIO.output(11,GPIO.LOW)
    GPIO.output(12,GPIO.LOW)

def Curtain(value):    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(8, GPIO.OUT)
    pwm=GPIO.PWM(8, 50)
    pwm.start(0)
    
    def SetAngle(angle):
            duty = angle / 18 + 2
            GPIO.output(8, True)
            pwm.ChangeDutyCycle(duty)
            sleep(1)
            GPIO.output(8, False)
            pwm.ChangeDutyCycle(0)
            
    SetAngle(value)
    pwm.stop()
    GPIO.cleanup()
    
    
def UpdateData():
    doc = doc_ref.get()
    Light.value="{}".format(doc.get("Light"))
    Curtain.value="{}".format(doc.get("Curtain"))
    Heater.value="{}".format(doc.get("Heater"))
    
Light.oldvalue="off"
Curtain.oldvalue="off"
Heater.oldvalue="off"
    
while(True):
    UpdateData()
    time.sleep(5)
    if(Light.value != Light.oldvalue):
        Light.oldvalue=Light.value
        if(Light.value != "on"):
            LightOn()
        if(Light.value == "off"):
            LightOff()
    if(Curtain.value != Curtain.oldvalue):
        Curtain.oldvalue=Curtain.value
        if(Curtain.value == "on"):
            Curtain(0)
        if(Curtain.value == "off"):
            print("off180")
    if(Heater.value != Heater.oldvalue):
        Heater.oldvalue=Heater.value
        if(Heater.value == "on"):
            print("Isıtıcı aç")
        if(Heater.value == "off"):
            print("Isıtıcı kapa")
