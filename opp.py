class student:
    def setdetails(self,name,rollno,marks):
        self.name=name
        self.rollno=rollno
        self.marks=marks
    def showdetails(self):
        print(f"NAME is {self.name} and ROLLNO is {self.rollno} and MARKS is {self.marks}")

student_1=student()
student_1.setdetails('John Doe', 101, 95)

student_2=student()
student_2.setdetails('sparsh',111,19)

student_1.showdetails()
student_2.showdetails()

