import unittest
from milestone1 import University, Student, Course, GRADE_POINTS, EnrollmentRecord, LinkedQueue

class TestMilestone1(unittest.TestCase):

    #Task 1 - Sneha
    def test_create_course(self):
        """test object creation for course class"""
        c = Course("CSE1010", 2)
        self.assertEqual(c.course_code, "CSE1010")
        self.assertEqual(c.credits, 2)
        self.assertEqual(len(c.students), 0)

    def test_add_student(self): 
        """test adding student objects to the course roster"""
        c = Course("CSE1010", 2)
        s = Student("STU00001", "Sneha")
        c.add_student(s)
        self.assertIn(s, c.students)

    def test_prevents_duplicates(self):
        """test that code prevents duplicate object entries in student roster"""
        c = Course("CSE1010", 2)
        s= Student("STU00001", "Sneha")
        c.add_student(s)
        c.add_student(s)
        self.assertEqual(len(c.students), 1)

    def test_student_count(self):
        """tests student count"""
        c = Course("CSE1010", 2)
        s1 = Student("STU00001", "Sneha")
        s2 = Student("STU00002","Charmi")
        c.add_student(s1)
        c.add_student(s2)
        self.assertEqual(c.get_student_count(), 2)

    #task 2 - Charmi
    def test_student_creation(self):
        """test object creation for student class"""
        s = Student("STU00001", "Charmi")
        self.assertEqual(s.student_id, "STU00001")
        self.assertEqual(s.name, "Charmi")
        self.assertEqual(s.courses, {})

    def test_enroll_course(self):
        """test enrolling to course"""
        s = Student("STU0001", "Charmi")
        c = Course("CSE1010", 2)
        s.enroll(c, "A-") #calling it from the milestone1.py file
        self.assertIn(c, s.courses)
        self.assertIn(s.courses[c], "A-")
        self.assertIn(s, c.students)
    
    def test_gpa_calculation(self):
        """test GPA calculation"""
        s = Student("STU00001", "Charmi")
        c1 = Course("CSE1010", 2)
        c2 = Course("CSE2050", 3)

        s.enroll(c1, "A-")
        s.enroll(c2, "B+")

        expected = ( GRADE_POINTS["A-"] * 2 + GRADE_POINTS["B+"]*3) / (2+3)

    def test_student_get_courses(self):
        """test getting student courses"""
        s = Student("STU00001", "Charmi")
        c = Course("CSE1010", 2)
        s.enroll(c, "A-")

        courses = s.get_courses()
        self.assertEqual(courses, [c])

        info = s.get_course_info()
        self.assertIn(c, s.courses)
        self.assertEqual(s.courses[c], "A-")
        self.assertEqual(c.credits, 2)


    #Task 3 - Sneha and Charmi
    def test_university_class(self):
        """test object creation for university class"""
        self.assertEqual(University().students, {})
        self.assertEqual(University().courses, {})

    def test_add_course(self):
        """test adding a course to university object"""
        uni = University()
        c = uni.add_course("CSE1010", 3)
        self.assertIn("CSE1010", uni.courses)
        self.assertIs(uni.courses["CSE1010"], c)

    def test_duplicate_course(self):
        """test duplicate course objects"""
        uni = University()
        c1 = uni.add_course("CSE1010", 2)
        c2 = uni.add_course("CSE1010", 2)
        self.assertEqual(c1, c2)
        self.assertEqual(len(uni.courses), 1)
        
    def test_add_student(self):
        """test adding a student"""
        uni = University()
        uni.add_student("STU00001", "Charmi")

    def test_duplicate_student(self):
        """test adding duplicate student"""
        uni = University()
        s1 = uni.add_student("STU00001", "Charmi")
        s2 = uni.add_student("STU00001", "Charmi")
        self.assertEqual(s1, s2)
        self.assertEqual(len(uni.students), 1)
    
    def test_get_student_info(self):
        """test getting student info"""
        uni = University()
        uni.add_student("STU00001", "Charmi")
        s = uni.get_student("STU00001")
        self.assertIsInstance(s, Student)

    def test_nonexistent_student_info(self):
        """test getting non-existent student info"""
        uni = University()
        self.assertIsNone(uni.get_student("STU12345"))

    def test_getting_course(self):
        """test getting course"""
        uni = University()
        uni.add_course("CSE1010", 2)
        c = uni.get_course("CSE1010")
        self.assertIsInstance(c, Course)

    def test_nonexistent_student_couse(self):
        """test getting non-existent student course"""
        uni = University()
        self.assertIsNone(uni.get_course("CSE12345")) 


    def structure(self):
        """test structure for milestone 2"""
        self.uni = University()
        self.course1 = self.uni.add_course("CSE1010", 2)
        self.student1 = self.uni.add_student("STU00001", "Charmi")
        self.student2 = self.uni.add_student("STU00002", "Sneha")

        self.records = [
            EnrollmentRecord(self.student1, "2026-03-29"),
            EnrollmentRecord(self.student2, "2026-03-31"),
        ]

        self.queue = LinkedQueue()

    def test_enrollment_record(self):
        """test enrollment records"""
        record = self.record[0]
        self.assertEqual(record.student.name, "Charmi")
        self.assertEqual(record.enroll_date, "2026-03-29")
        self.assertIn("Charmi", repr(record))


    def test_enqueue_dequeue(self):
        """test queues"""
        self.queue.enqueue(self.student1)
        self.queue.enqueue(self.student2)
        self.assertEqual(len(self.queue), 2)

        s = self.queue.dequeue()
        self.assertEqual(s.name, "Charmi")

        s2 = self.queue.dequeue()
        self.assertEqual(s2.name, "Sneha")
        self.assertTrue(self.queue.is_empty())

    def test_dequeue_empty(self):
        with self.assertRaises(ValueError):
            self.queue.dequeue()


if __name__ == "__main__":
    unittest.main()