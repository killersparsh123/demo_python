class bike():
    def setdetails(self,brand,model,color):
        self.brand=brand
        self.model=model
        self.color=color
    def showdetail(self):
        print(f"This is a bike brand named {self.brand} and the model is {self.model} and the color is {self.color}")
bike_1=bike()
bike_1.setdetails('Yamaha','MT-15','Blue')

bike_2=bike()
bike_2.setdetails('Honda','CBR650R','Red')

bike_1.showdetail()
bike_2.showdetail()
