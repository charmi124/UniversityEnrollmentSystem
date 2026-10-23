import csv
from datetime import date

#Task 1: Charmi
class HashMap:
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for i in range(capacity)]

    def _hash(self, key):
        return hash(key) % self.capacity

    def put(self, key, value):
        """Insert or update key-value pair."""
        bucket = self.buckets[self._hash(key)]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

        if self.size / self.capacity >= 0.8:
            self._rehash()

    def get(self, key):
        """Return value or None if not found."""
        bucket = self.buckets[self._hash(key)]

        for k, v in bucket:
            if k == key:
                return v
        return None

    def keys(self):
        """Return all keys in hashmap."""
        result = []
        for bucket in self.buckets:
            for k, v in bucket:
                result.append(k)
        return result

    def _rehash(self):
        """Double size and reinsert all items."""
        old = self.buckets
        self.capacity *= 2
        self.buckets = [[] for i in range(self.capacity)]
        self.size = 0

        for bucket in old:
            for k, v in bucket:
                self.put(k, v)

#Task 2: Sneha 
class Student:
    """Represents a student and completed courses."""

    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.completed_courses = HashMap()  

    def add_completed(self, course_id):
        """Mark course as completed."""
        self.completed_courses.put(course_id, True)

    def has_taken(self, course_id):
        """Check if course was completed."""
        return self.completed_courses.get(course_id) is not None


class Course:
    """Course with capacity, waitlist, and prerequisites."""

    def __init__(self, course_id, name, capacity):
        self.course_id = course_id
        self.name = name
        self.capacity = capacity

        self.enrolled = []
        self.waitlist = []
        self.prerequisites = HashMap()   

    def add_prerequisite(self, prereq_id):
        """Add prerequisite course."""
        self.prerequisites.put(prereq_id, True)

    def request_enroll(self, student):
        """Enroll only if prerequisites are satisfied."""

        for prereq in self.prerequisites.keys():
            if not student.has_taken(prereq):
                raise Exception(f"Missing prerequisite: {prereq}")

        if len(self.enrolled) < self.capacity:
            self.enrolled.append(student)
            return "Enrolled"
        else:
            self.waitlist.append(student)
            return "Waitlisted"


def load_prerequisites(filename, courses_dict):
    """Load prerequisites from CSV."""
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            course_id, prereq_id = row

            if course_id in courses_dict:
                courses_dict[course_id].add_prerequisite(prereq_id)


def merge_sort(arr, key=lambda x: x):
    """O(n log n) stable sort."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)

    return merge(left, right, key)


def merge(left, right, key):
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
    """O(n log n) average, O(n^2) worst case."""
    if len(arr) <= 1:
        return arr

    pivot = arr[0]
    left = [x for x in arr[1:] if key(x) <= key(pivot)]
    right = [x for x in arr[1:] if key(x) > key(pivot)]

    return quick_sort(left, key) + [pivot] + quick_sort(right, key)