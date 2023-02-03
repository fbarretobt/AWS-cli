class Employee :

    empCount = 0


    def _init_(self, name, salary){

        self.name = name
        self.salary = salary

        Employee.emCount += 1
    
    }

    def displayCount(self):
        print("Employee Count = ", Employee.empCount)

    def displayEmployee(self):
        print("Employee: ", self.name, ", Salary: ", self.salary )


emp1 = Employee("Sarah", "2000")
emp2 = Employee("John", "3000")


emp1.displayEmployee()
emp2.displayEmployee()

print("Total Employees = ", Employee.empCount)
