#Charmi

import unittest
from datetime import date
from milestone2 import Student, Course, LinkedQueue, EnrollmentRecord

class TestLinkedQueue(unittest.TestCase):
    """Tests for the LinkedQueues"""
    def test_enqueue_dequeue_fifo(self):
        """Tests that queue following FIFO order"""
        q = LinkedQueue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)

    def test_dequeue_empty(self):
        """Tests that dequeue raises error when the queue is empty """
        q = LinkedQueue()
        with self.assertRaises(ValueError):
            q.dequeue()

    def test_size_tracking(self):
        """Queue size is tracking correctly"""
        q = LinkedQueue()
        q.enqueue(10)
        q.enqueue(20)
        self.assertEqual(len(q), 2)
        q.dequeue()
        self.assertEqual(len(q), 1)


class TestEnrollment(unittest.TestCase):
    def setUp(self):
        """setting up courses and sample students"""
        self.course = Course("CSE2050", 3, capacity=2)
        self.s1 = Student("STU00001", "Charmi")
        self.s2 = Student("STU00002", "Sneha")
        self.s3 = Student("STU00003", "Lina")

    def test_enroll_until_capacity(self):
        """ensuring that students enrolled until capacity reached"""
        self.course.request_enroll(self.s1, "2026-03-04")
        self.course.request_enroll(self.s2, "2026-06-07")

        self.assertEqual(len(self.course.enrolled), 2)

    def test_waitlist_when_full(self):
        """additional students added to waitlist when the course is full"""
        self.course.request_enroll(self.s1, "2026-01-01")
        self.course.request_enroll(self.s2, "2026-01-02")
        self.course.request_enroll(self.s3, "2026-01-03")

        self.assertEqual(len(self.course.waitlist), 1)

    def test_drop_promotes_waitlist(self):
        """ensure dropping a student promotes next waitlisted student."""
        self.course.request_enroll(self.s1, "2026-01-01")
        self.course.request_enroll(self.s2, "2026-01-02")
        self.course.request_enroll(self.s3, "2026-01-03") 

        self.course.sort_enrolled("id", "insertion")
        self.course.drop("STU00001")

        self.assertEqual(len(self.course.enrolled), 2)
        self.assertEqual(len(self.course.waitlist), 0)



class TestSorting(unittest.TestCase):

    def setUp(self):
        """Set up course with unsorted enrollment data."""
        self.course = Course("CSE2050", 3, capacity=5)
        self.s1 = Student("STU00003", "Charmi")
        self.s2 = Student("STU00001", "Sneha")
        self.s3 = Student("STU00002", "Lina")

        self.course.request_enroll(self.s1, "2026-01-03")
        self.course.request_enroll(self.s2, "2026-01-01")
        self.course.request_enroll(self.s3, "2026-01-02")

    def test_sort_by_id(self):
        """sorting by student ID"""
        self.course.sort_enrolled("id", "insertion")
        ids = [r.student.student_id for r in self.course.enrolled]
        self.assertEqual(ids, ["STU00001", "STU00002", "STU00003"])

    def test_sort_by_name(self):
        """sorting by student name"""
        self.course.sort_enrolled("name", "selection")
        names = [r.student.name for r in self.course.enrolled]
        self.assertEqual(names, ["Charmi", "Lina", "Sneha"])

    def test_sort_by_date(self):
        """sorting by enrollment date"""
        self.course.sort_enrolled("date", "insertion")
        dates = [r.enroll_date for r in self.course.enrolled]
        self.assertEqual(dates, ["2026-01-01", "2026-01-02", "2026-01-03"])


class TestBinarySearchDrop(unittest.TestCase):
    def setUp(self):
        """sorted course for binary search testing"""
        self.course = Course("CSE2050", 3, capacity=5)

        self.s1 = Student("STU00001", "Charmi")
        self.s2 = Student("STU00002", "Sneha")
        self.s3 = Student("STU00003", "Lina")

        self.course.request_enroll(self.s1, "2026-01-01")
        self.course.request_enroll(self.s2, "2026-01-02")
        self.course.request_enroll(self.s3, "2026-01-03")

        self.course.sort_enrolled("id", "insertion")

    def test_binary_search_found(self):
        """ensure binary search returns correct index when found"""
        index = self.course.recursive_binary_search("STU00002", 0, 2)
        self.assertEqual(index, 1)

    def test_binary_search_not_found(self):
        """ensure binary search returns -1 when student not found. """
        index = self.course.recursive_binary_search("STU0021", 0, 2)
        self.assertEqual(index, -1)

    def test_drop_removes_student(self):
        """emsure drop removes the correct student from the enrolled list."""
        self.course.drop("STU00002")
        ids = [r.student.student_id for r in self.course.enrolled]
        self.assertNotIn("STU00002", ids)


if __name__ == "__main__":
    unittest.main()