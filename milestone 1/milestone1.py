import csv
from statistics import mean, median, mode

#Milestone 2 - Task 1: Charmi
class EnrollmentRecord:
    """Creates an EnrollmentRecord structure to represent enrollment in a course."""
    def __init__(self, student, enroll_date):
        self.student = student
        self.enroll_date = enroll_date

    def __repr__(self):
        return f"{self.student.name} ({self.student.student_id}) - {self.enroll_date}"   


#Milestone 2 - Task 2: Charmi

class Node:
    def __init__(self, data):
        """Implement Node class with fields data and next"""
        self.data = data 
        self.next = None 

class LinkedQueue:
    def __init__(self):
        """..."""
        self.front = None
        self.rear = None
        self._size = 0 
    
    def is_empty(self):
        """..."""
    
    def __len__(self):
        return self._size

    def enqueue(self, item):
        """..."""
        new_node = Node(item)
        if self.rear:
            self.rear.next = new_node
        self.rear = new_node
        if self.front is None:
            self.front = new_node
        self.size += 1
    
    def dequeue(self):
        """..."""
        if self.is_empty():
            raise ValueError("The queue is empty")
        item = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return item



# Task 4 Milestone 2: Sneha 
    def _get_sort_key(self, record, by):
        """
        Returns the value used for comparison based on sorting key.
        """
        if by == "name":
            return record.student.name.lower()
        elif by == "id":
            return record.student.student_id
        elif by == "date":
            return record.enroll_date
        else:
            raise ValueError("Invalid sort key. Use 'name', 'id', or 'date'.")

    def _selection_sort(self, by):
        """
        Selection Sort algorithm
        """
        n = len(self.enrolled)

        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                if self._get_sort_key(self.enrolled[j], by) < self._get_sort_key(self.enrolled[min_index], by):
                    min_index = j
            self.enrolled[i], self.enrolled[min_index] = self.enrolled[min_index], self.enrolled[i]

    def _insertion_sort(self, by):
        """
        Insertion Sort algorithm
        """
        for i in range(1, len(self.enrolled)):
            current_record = self.enrolled[i]
            current_key = self._get_sort_key(current_record, by)

            j = i - 1
            while j >= 0 and self._get_sort_key(self.enrolled[j], by) > current_key:
                self.enrolled[j + 1] = self.enrolled[j]
                j -= 1

            self.enrolled[j + 1] = current_record

    def sort_enrolled(self, by, algorithm):
        """
        Sorts the enrolled roster.

        by:
            'name' 1. sort by student name
            'id'   2. sort by student ID
            'date' 3. sort by enrollment date

        algorithm:
            'selection'  1. selection sort
            'insertion' 2.  insertion sort
        """

        if by not in ["name", "id", "date"]:
            raise ValueError("Sort key must be 'name', 'id', or 'date'.")

        if algorithm == "selection":
            self._selection_sort(by)
        elif algorithm == "insertion":
            self._insertion_sort(by)
        else:
            raise ValueError("Algorithm must be 'selection' or 'insertion'.")

        # track how it's sorted
        self.enrolled_sorted_by = by

#Milestone 2 Task 5
def recursive_binary_search(records, target_id, low, high):
    """Implement recursive binary search and use it to support dropping students by ID."""
    if low > high:
        return -1

    mid = (low + high) // 2
    mid_id = records[mid].student.student_id

    if mid_id == target_id:
        return mid
    elif target_id < mid_id:
        return recursive_binary_search(records, target_id, low, mid - 1)
    else:
        return recursive_binary_search(records, target_id, mid + 1, high)




#task 1- Sneha
class Course: 
    def __init__(self, course_code, credits):
        """Initializes a course with code and credits, starting with empty student roster"""
        self.course_code = course_code
        self.credits = credits  
        self.students = []  


# Milestone 2 structures: Sneha : Task 3 
        self.enrolled = []              # list of EnrollmentRecord
        self.waitlist = LinkedQueue()   # queue from Task 2
        self.enrolled_sorted_by = None

    def is_student_enrolled(self, student_id):
        for record in self.enrolled:
            if record.student.student_id == student_id:
                return True
        return False

    def is_student_waitlisted(self, student_id):
        current = self.waitlist.front
        while current:
            if current.data.student_id == student_id:
                return True
            current = current.next
        return False

    def request_enroll(self, student, enroll_date):
        enroll_date = str(enroll_date)

        if self.is_student_enrolled(student.student_id):
            return f"{student.student_id} already enrolled."

        if self.is_student_waitlisted(student.student_id):
            return f"{student.student_id} already waitlisted."

        if len(self.enrolled) < self.capacity:
            record = EnrollmentRecord(student, enroll_date)
            self.enrolled.append(record)
            self.enrolled_sorted_by = None
            return f"{student.student_id} enrolled successfully."
        else:
            self.waitlist.enqueue(student)
            return f"{student.student_id} added to waitlist."

    def recursive_binary_search(self, student_id, low, high):
        if low > high:
            return -1

        mid = (low + high) // 2
        mid_id = self.enrolled[mid].student.student_id

        if mid_id == student_id:
            return mid
        elif student_id < mid_id:
            return self.recursive_binary_search(student_id, low, mid - 1)
        else:
            return self.recursive_binary_search(student_id, mid + 1, high)

    def drop(self, student_id, enroll_date_for_replacement=None):
        if len(self.enrolled) == 0:
            return "No students enrolled."

        # must be sorted by ID for binary search
        if self.enrolled_sorted_by != "id":
            self.sort_enrolled("id", "insertion")

        index = self.recursive_binary_search(student_id, 0, len(self.enrolled) - 1)

        if index == -1:
            return f"{student_id} not found."

        removed = self.enrolled.pop(index)

        if not self.waitlist.is_empty():
            next_student = self.waitlist.dequeue()

            if enroll_date_for_replacement is None:
                new_date = date.today().isoformat()
            else:
                new_date = str(enroll_date_for_replacement)

            self.enrolled.append(EnrollmentRecord(next_student, new_date))

            # keep sorted after adding
            self.sort_enrolled("id", "insertion")

            return f"{removed.student.student_id} dropped, {next_student.student_id} moved from waitlist."

        return f"{removed.student.student_id} dropped."



    def add_student(self, student):
        """Adds a Student object to the course roster if not already present"""
        if student not in self.students:
            self.students.append(student)
    
    def get_student_count(self):
        """Returns the number of students currently enrolled"""
        return len(self.students)
    
    def __repr__(self):
        """Returns the course code and credits in a clear statement"""
        return f"Course({self.course_code}, {self.credits})"

# Task 2 - Charmi
GRADE_POINTS = {
    'A' : 4.0, 'A-' : 3.7,
    'B+': 3.3, 'B' : 3.0, 'B-' : 2.7,
    'C+': 2.3, 'C' : 2.0, 'C-' : 1.7,
    'D' : 1.0,
    'F' : 0.0
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

#Task 3 - Charmi + Sneha
class University:
    def __init__(self):
        self.students = {} #maps student_id --> Student object
        self.courses = {}  #maps course_id --> Course object

    def add_course(self, course_code, credits): #Sneha
        """ if the course does not exist, create and store it; return the course object."""
        if course_code not in self.courses:
            self.courses[course_code] = Course(course_code, credits)
        return self.courses[course_code]

    def add_student(self, student_id, name): #Sneha
        """if the student does not exist, create and store them; return the student object"""
        if len(student_id) != 8: #Validate ID
            return None
        if student_id[0:3] != "STU":
            return None
        if name == "": #validate name 
            raise ValueError("Name cannot be empty")
        
        if student_id not in self.students: #preventing duplicates
            self.students[student_id] = Student(student_id, name)
        return self.students[student_id]

    def get_student(self, student_id):  #Charmi
        """returns the student object for that ID (or None if not found)."""
        return self.students.get(student_id)

    def get_course(self, course_code): #Charmi
        """returns the course object for that code (or None if not found)"""
        return self.courses.get(course_code)

    def get_course_enrollment(self, course_code): #Charmi
        """returns the number of students enrolled in the given course"""
        course = self.get_course(course_code)
        if course is None:
            return 0
        return len(course.students)

    def get_students_in_course(self, course_code): #Charmi
        """returns a list of student objects enrolled in the given course"""
        course = self.get_course(course_code)
        if course:
            return course.students
        return []

    #stats: Charmi
    def course_stats(self, course_code):
        """Calculate mean, mode and median for a course"""
        if course_code not in self.courses:
            return None
        
        course = self.courses[course_code]
        if not course.students:
            return None
        
        grades = []
        for students in course.students:
            grade_letter = students.courses[course]
            grade_pt = GRADE_POINTS[grade_letter]
            grades.append(grade_pt)

            avg = round(mean(grades),2)
            med = round(median(grades),2)
            mode = round(mode(grades),2)

            return f'"mean:" {avg}, "median:{med}, "mode:"{mode}'

    def uni_gpa_stats(self):
        """Calculate mean and median for the GPA of all students in the university"""
        gpas = []

        for student in self.students.values():
            gpa = student.calculate_gpa()
            gpas.append(gpa)

        if len(gpas) == 0:
            return None
        
        mean_gpa = round(mean(gpas), 2)
        median_gpa = round(median(gpas),2)

        return f'"mean:" {mean_gpa}, "median:" {median_gpa}'

    def common_students(self, course_code1, course_code2):
        """Print common students in two different courses (Intersection)"""
        course1 = self.get_course(course_code1)
        course2 = self.get_course(course_code2)

        if not course1 or not course2:
            return []
        
        common = []
        for student in course1.students:
            if student in course2.students:
                common.append(student)

        return common

#csv files - Sneha 
def load_data(university, student_file, course_file):
    with open(course_file, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            course_code = row["course_code"]      
            credits = int(row["credits"])          
            university.add_course(course_code, credits)

    with open(student_file, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            student_id = row["student_id"]        
            name = row["name"]                   
            student = university.add_student(student_id, name)
            courses_string = row["courses"]
            if courses_string:
                entries = courses_string.split(";")
                for entry in entries:
                    if ":" in entry:
                        course_code, grade = entry.split(":")
                        course = university.get_course(course_code)
                        if course:
                            student.enroll(course, grade)

#csv files: Task 1 Charmi
def load_enrollment_records(uni, enrollment_file, course_code):

    records = []

    with open(enrollment_file, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            student = uni.get_student(row["student_id"])
            if student and row["course_code"] == course_code:
                records.append(EnrollmentRecord(student, row["enroll_date"]))
    return records

#Demonstration - Charmi
if __name__ == "__main__":
    uni = University()
    load_data(uni, "university_data.csv", "course_catalog.csv")
    
    # printing students in a course 
    course_code = "CSE1010"
    students_in_course = uni.get_students_in_course(course_code)
    print(f"Students enrolled in {course_code}:")
    for student in students_in_course:
        print(f"{student.name} ({student.student_id})")
    
    print("\n")  
     
    #GPA of a student
    student_id = "STU00001"
    student = uni.get_student(student_id)
    if student:
        print(f"GPA of {student.name} ({student.student_id}): {student.calculate_gpa()}")
    else:
        print(f"Student {student_id} not found.")
    

    print("\n")
          
    #print all courses and course info (grades and credits) for a student
    if student:
        print(f"Courses for {student.name} ({student.student_id}):")
        for info in student.get_course_info():
            print(f"{info['course_code']} :- Grade: {info['grade']}, Credits: {info['credits']}")

    print("\n")
    
    #getting common students in diff courses (intersection)
    course1 = "CSE2050"
    course2 = "BIO1010"
    common_students = uni.common_students(course1,course2)

    print(f"Common students in {course1} and {course2}:")
    for student in common_students:
        print(f"{student.name} {(student.student_id)}")
    
    print("\n")

    # printing stats for GPA:
    print(f"University GPA Statistics:")
    print(uni.uni_gpa_stats())

    #M2 Task 1: Charmi

    course_code = "CSE1010"
    records = load_enrollment_records(uni, "enrollments_CSE10.csv", course_code)

    print(f"\nEnrollmentRecords for {course_code}:")
    for record in records:
        print(record)

    #M2 Task 2: Charmi 
    waitlist = LinkedQueue()

    student1 = uni.get_student("STU00001")
    student2 = uni.get_student("STU00002")
    
    if student1:
        waitlist.enqueue(student1)
    if student2:
        waitlist.enqueue(student2)
    
    print(f"Waitlist size: {len(waitlist)}") 

    next_student = waitlist.dequeue()
    print(f"Next student from waitlist: {next_student.name} ({next_student.student_id})")
    print(f"Waitlist size after dequeue: {len(waitlist)}")  