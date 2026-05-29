class bird():
    def sound(self):
        print("bird sound like ")
class crow(bird):
    def sound(self):
        print("crow sound like caw caw")
class parrot(bird):
    def sound(self):
        print("parrot sound like squawk")


bird1=crow()
bird2=parrot()

bird1.sound()
bird2.sound()
