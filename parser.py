class Employee :

    empCount = 0


    def __init__(self, name, salary):

        self.name = name
        self.salary = salary

        Employee.empCount += 1
    
    def displayCount(self):
        print("Employee Count = ", Employee.empCount)

    def displayEmployee(self):
        print("Employee: ", self.name, ", Salary: ", self.salary )


emp1 = Employee("Sarah", 2000)
emp2 = Employee("John", 3000)


emp3 = Employee("Zara", 2000)
emp4 = Employee("Manni", 5000)

print("Employee Name: "emp1.name)
print(emp1.name, "Salary : ", emp1.salary)



print ("Employee.__doc__:", Employee.__doc__)
print ("Employee.__name__:", Employee.__name__)
print ("Employee.__module__:", Employee.__module__)
print ("Employee.__bases__:", Employee.__bases__)
print ("Employee.__dict__:", Employee.__dict__ )