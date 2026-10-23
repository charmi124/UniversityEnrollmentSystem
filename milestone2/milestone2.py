import csv 
from datetime import date
from statistics import mean, median, mode

GRADE_POINTS = {
    'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D': 1.0, 'F': 0.0
}

class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.courses = {}

    def enroll(self, course, grade):
        """Enrolls the student in a course with the given grade and updates the course roster"""
        if grade not in GRADE_POINTS:
            raise ValueError("No grade")
        
        self.courses[course] = grade
        course.add_student(self)

    def update_grade(self, course, grade):
        """Modify the student grade for a particular course"""
        if grade not in GRADE_POINTS:
            raise ValueError("Invalid grade")
        if course in self.courses:
            self.courses[course] = grade   

    def calculate_gpa(self):
        """Computes and returns the GPA using all graded courses and their credits."""
        total_points = 0 
        total_credits = 0 

        for course in self.courses:
            grade = self.courses[course]
            points = GRADE_POINTS[grade]
            total_points += points * course.credits
            total_credits += course.credits

        if total_credits == 0:
            return 0.0
        
        gpa = round(total_points / total_credits, 2) 
        return gpa      
    
    def get_courses(self):
        """returns a list of course objects taken by the student""" 
        course_list = []
        for course in self.courses:
            course_list.append(course)
        return course_list 
    
    def get_course_info(self):
        """returns a structursed summary of all enrollments, including course code, grade, and credits."""
        info_list = [] 

        for course in self.courses:
            grade = self.courses[course] 
            course_info = {} 

            course_info["course_code"] = course.course_code
            course_info["grade"] = grade
            course_info["credits"] = course.credits
            info_list.append(course_info) 

        return info_list 
    
    def __repr__(self):
        """Returns the name and student id in a clear statement"""
        return f"{self.name}, {self.student_id}" 
    

# Milestone 2- Task 1: Enrollment Record 
#Charmi
class EnrollmentRecord:
    """Represents student's enrollment in couse with date."""
    def __init__(self, student, enroll_date):
        self.student = student 
        self.enroll_date = enroll_date

#Task 2: LinkedQueue ADT
# Charmi
class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class LinkedQueue:
    def __init__(self):
        self.front = None
        self.back = None
        self._size = 0 
    
    def enqueue(self, item):
        """Add item to the back of the queue"""
        new_node = Node(item)
        if self.is_empty():
            self.front = self.back = new_node 
        else:
            self.back.next = new_node
            self.back = new_node 
        self._size += 1
    
    def dequeue(self):
        """Remove and return item from front of queue"""
        if self.is_empty():
            raise ValueError("The queue is empty")
        item = self.front.data
        self.front = self.front.next
        self._size -= 1
        if self.front is None:
            self.back = None
        return item 
    
    def is_empty(self):
        """Return True if the queue is empty"""
        return self._size == 0 
    
    def __len__(self):
        """Return number of elements in queue"""
        return self._size
    
#Task 3 - Sneha
class Course:
    def __init__(self,course_code,credits, capacity):
        self.course_code = course_code
        self.credits = credits 
        self.capacity = int(capacity)

        self.enrolled = []              
        self.waitlist = LinkedQueue()  
        self.enrolled_sorted_by = None
        self.students = []
    
    def add_student(self, student):
        """Adds a Student object to the course roster if not already present"""
        if student not in self.students:
            self.students.append(student)

    def is_student_enrolled(self, student_id):
        """Add an enrolled roster (list of EnrollmentRecord)."""
        return any(r.student.student_id == student_id for r in self.enrolled)

    
    def is_student_waitlisted(self, student_id):
        """Add a waitlist attribute of type LinkedQueue."""
        current = self.waitlist.front
        while current:
            if current.data.student_id == student_id:
                return True 
            current = current.next
        return False

    def request_enroll(self, student, enroll_date):
        """Enroll student or add to waitlist."""
        if self.is_student_enrolled(student.student_id):
            return "Already enrolled"

        if self.is_student_waitlisted(student.student_id):
            return "Already waitlisted"

        if len(self.enrolled) < self.capacity:
            self.enrolled.append(EnrollmentRecord(student, enroll_date))
            self.enrolled_sorted_by = None
            return "Enrolled"
        else:
            self.waitlist.enqueue(student)
            return "Waitlisted"
        

#Task 4 - Sneha 

    def get_key(self, record, by):
        """Return key for sorting based on id, name, or date"""
        if by == "id":
            return record.student.student_id
        elif by == "name":
            return record.student.name
        elif by == "date":
            return record.enroll_date

    def insertion_sort(self, by):
        """Sort enrolled records using insertion sort. """
        for i in range(1, len(self.enrolled)):
            key = self.enrolled[i]
            j = i - 1
            while j >= 0 and self.get_key(self.enrolled[j], by) > self.get_key(key, by):
                self.enrolled[j + 1] = self.enrolled[j]
                j -= 1
            self.enrolled[j + 1] = key
        self.enrolled_sorted_by = by

    def selection_sort(self, by):
        """Sort enrolled records using selection sort."""
        n = len(self.enrolled)
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                if self.get_key(self.enrolled[j], by) < self.get_key(self.enrolled[min_index], by):
                    min_index = j
            self.enrolled[i], self.enrolled[min_index] = self.enrolled[min_index], self.enrolled[i]
        self.enrolled_sorted_by = by

    def sort_enrolled(self, by, algorithm):
        """Sorting enrolled list using chosen algorithm"""
        if algorithm == "insertion":
            self.insertion_sort(by)
        elif algorithm == "selection":
            self.selection_sort(by)
        else:
            raise ValueError("This is an invalid algorithm")
        
    #Task 5: Sneha and Charmi
    def recursive_binary_search(self, target_id, low, high):
        """Implement recursive binary search and use it to support dropping students by ID."""
        if low > high:
            return -1
        
        mid = (low + high) // 2
        mid_id = self.enrolled[mid].student.student_id
        
        if mid_id == target_id:
            return mid
        elif target_id < mid_id:
            return self.recursive_binary_search(target_id, low, mid - 1)
        else:
            return self.recursive_binary_search(target_id, mid + 1, high)

    #Task 3 : Sneha
    def drop(self, student_id, enroll_date_for_replecement = None):
        """re-sort by ID automatically or raise an exception with a clear error message"""
        if len(self.enrolled) == 0:
            return "No students enrolled."
        
        if self.enrolled_sorted_by != "id":
            self.sort_enrolled("id", "insertion")

        index = self.recursive_binary_search(student_id, 0, len(self.enrolled) - 1)

        if index == -1:
            return f"{student_id} not found."
        
        removed_record = self.enrolled.pop(index) 
        if removed_record.student in self.students:
            self.students.remove(removed_record.student)

        if not self.waitlist.is_empty():
            next_student = self.waitlist.dequeue()

            new_date = str(enroll_date_for_replecement)

            self.enrolled.append(EnrollmentRecord(next_student, new_date))
            self.add_student(next_student)  
            self.sort_enrolled("id", "insertion")

            return f"{removed_record.student.student_id} is dropped; {next_student.student_id} is moved from waitlist."
        
        return f"{removed_record.student.student_id} is dropped."
    
class University:
    def __init__(self):
        self.students = {}  
        self.courses = {}   

    def add_course(self, course_code, credits, capacity = 20):
        """Add or return course. """
        if course_code not in self.courses:
            self.courses[course_code] = Course(course_code, credits, capacity)
        return self.courses[course_code]

    def add_student(self, student_id, name):
        """Add or return student"""
        if student_id not in self.students:
            self.students[student_id] = Student(student_id, name)
        return self.students[student_id]

    def get_student(self, student_id):
        """Getting student id"""
        return self.students.get(student_id)

    def get_course(self, course_code):
        """getting course by the course code"""
        return self.courses.get(course_code)

#csv files
def load_data(university, student_file, course_file):
    """load courses and the student data from the CSV files"""
    with open(course_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            course_code = row.get("course_code") or row.get("CourseCode")
            credits = int(row.get("credits") or row.get("Credits"))
            capacity = int(row.get("capacity") or row.get("Capacity", 30))
            university.add_course(course_code, credits, capacity)

    with open(student_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            student_id = row.get("student_id") or row.get("StudentID")
            name = row.get("name") or row.get("Name")
            student = university.add_student(student_id, name)
            courses_string = row.get("courses") or row.get("Courses")

#demo
if __name__ == "__main__":
    uni = University()
    load_data(
        uni,
        student_file="university_data.csv",
        course_file="course_catalog_CSE10_with_capacity.csv"
    )

    for course_code, course in uni.courses.items():
        print(f"Course: {course_code} (Capacity: {course.capacity})")
        if course.enrolled:
            print("  Enrolled:")
            for record in course.enrolled:
                print(f"{record.student.name} ({record.student.student_id}) - {record.enroll_date}")
        else:
            print("No enrolled students")
        if len(course.waitlist) > 0:
            print("Waitlist:")
            for node in course.waitlist:
                print(f"{node.student_id}")
        print("\n")

    for student_id, student in uni.students.items():
        print(f"{student.name} ({student_id}) - GPA: {student.calculate_gpa()}")
        for info in student.get_course_info():
            print(f"{info['course_code']}: Grade {info['grade']}, Credits {info['credits']}")
        print("\n")