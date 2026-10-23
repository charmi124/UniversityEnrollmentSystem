import csv
from datetime import date

#Task 1: Charmi
class HashMap:
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for i in range(capacity)]

    def _hash(self, key):
        """Return bucket index for key"""
        return hash(key) % self.capacity

    def put(self, key, value):
        """Insert or update key-value pair."""
        bucket = self.buckets[self._hash(key)]

        for i in range(len(bucket)):
            x = bucket[i]

            if x[0] == key:
                bucket[i] = (key, value)
                return 

        bucket.append((key, value))
        self.size += 1

        if self.size / self.capacity >= 0.8:
            self._rehash()

    def get(self, key):
        """Reutrn value associated with key. If not found return None"""
        bucket = self.buckets[self._hash(key)]

        for k, v in bucket:
            if k == key:
                return v
        return None

    def keys(self):
        """Return list of all keys in hashmap"""
        result = []
        for bucket in self.buckets:
            for k, v in bucket:
                result.append(k)
        return result

    def _rehash(self):
        """Double capacity and reinsert all elements"""
        old = self.buckets
        self.capacity *= 2
        self.buckets = [[] for i in range(self.capacity)]
        self.size = 0

        for bucket in old:
            for k, v in bucket:
                self.put(k, v)

#Task 2: Sneha 
class Student:
    
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.completed_courses = HashMap()  

    def add_completed(self, course_id):
        """Mark course as completed"""
        self.completed_courses.put(course_id, True)

    def has_taken(self, course_id):
        """Return True if student has completed course"""
        return self.completed_courses.get(course_id) is not None


class Course:
    
    def __init__(self, course_id, name, capacity):
        self.course_id = course_id
        self.name = name
        self.capacity = capacity

        self.enrolled = []
        self.waitlist = []
        self.prerequisites = HashMap()   

    def add_prerequisite(self, prereq_id):
        """Add prerequisite course"""
        self.prerequisites.put(prereq_id, True)

    def request_enroll(self, student):
        """Enroll student if prerequisites are met. Else, raise Exception"""
        for prereq in self.prerequisites.keys():
            if not student.has_taken(prereq):
                raise Exception(f"Missing prerequisite: {prereq}")

        if len(self.enrolled) < self.capacity:
            self.enrolled.append(student)
            return "Enrolled"
        else:
            self.waitlist.append(student)
            return "Waitlisted"


def merge_sort(arr, key=lambda x: x):
    """Sort list using merge sort O(nlogn)"""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)

    return merge(left, right, key)


def merge(left, right, key):
    """Merge 2 sorted lists into 1 sorted list"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    return result + left[i:] + right[j:]


def quick_sort(arr, key=lambda x: x):
    """Sort list using quick sort O(nlogn)"""
    if len(arr) <= 1:
        return arr

    pivot = arr[0]
    left = [x for x in arr[1:] if key(x) <= key(pivot)]
    right = [x for x in arr[1:] if key(x) > key(pivot)]

    return quick_sort(left, key) + [pivot] + quick_sort(right, key)

class University:
    """stores courses"""
    def __init__(self):
        self.courses = {}

#csv files
def load_prerequisites(filename, courses_dict):
    
    with open(filename, newline='') as file:
        reader = csv.reader(file, delimiter='\t')

        next(reader,None)

        for row in reader:
            if len(row) < 2:
                continue

            course_id = row[0].strip()
            prereq_id = row[1].strip()

            if prereq_id == "":
                continue

            if course_id in courses_dict:
                courses_dict[course_id].add_prerequisite(prereq_id)

        
if __name__ == "__main__":
    uni = University()

    uni.courses["CSE2050"] = Course("CSE1010", "Intro to Python", 3)
    uni.courses["CSE2102"] = Course("CSE2050", "Data Structures", 3)
    uni.courses["CSE2500"] = Course("CSE2050", "Data Structures", 3)

    load_prerequisites("cse_prerequisites.csv", uni.courses)

    for course_id, course in uni.courses.items():
        print(course_id, course.prerequisites.keys())