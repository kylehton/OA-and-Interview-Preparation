
from collections import defaultdict
import json
from typing import List

class Employee():
    def __init__(self, name="", employee_id="", department="", salary=0):
        self.name = name
        self.employee_id = employee_id
        self.dept = department
        self.salary = salary

    def to_dict(self):
        return {
            "name": self.name,
            "employee_id": self.employee_id,
            "department": self.dept,
            "salary": self.salary
        }

class EmployeeDirectory():
    def __init__(self):
        self.employees = {} # dict of employees

    def loadEmployees(self, path) -> None:
        with open(path) as file:
            obj = json.load(file)
            for item in obj:
                emp = Employee(
                    item['name'], 
                    item['employee_id'], 
                    item.get('department', 'Unknown'), 
                    item.get('salary', None))
                if not emp.name or not emp.employee_id:
                    raise ValueError(f"Missing required field in {item}")
                self.employees[emp.employee_id] = emp
    
    def average_salary(self, dept: str) -> float:
        salarySum = 0
        empCount = 0
        for employee in self.employees.values():
            if employee.dept == dept:
                if employee.salary is not None:
                    salarySum += employee.salary
                    empCount += 1
        if empCount == 0:
            return 0.0
        return (salarySum/empCount)
    
    def get_by_department(self, dep: str) -> List[Employee]:
        res = []
        for employee_id in self.employees:
            employee = self.employees[employee_id]
            if employee.dept == dep:
                res.append(employee)
        return res
    
    def give_raise(self, employee_id, percent) -> None:
        if employee_id in self.employees:
            self.employees[employee_id].salary *= (1+percent)
        else:
            raise ValueError(f"Employee ID: {employee_id} does not exist.")
    
    def save_to_file(self, path):
        data = []
        for employee in self.employees.values():
            data.append(employee.to_dict())
        with open(path, 'w') as file:
            json.dump(data, file, indent=2)
        