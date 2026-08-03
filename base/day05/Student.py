from Person import Person





class Student(Person):

    def study(self):
        print("Student", self.name, " is studying")


student = Student("sumeng",23,175,75)

student.study()