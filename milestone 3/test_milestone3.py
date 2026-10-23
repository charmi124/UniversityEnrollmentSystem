#Charmi
import unittest
from milestone3 import HashMap, Student, Course, merge_sort, quick_sort


class TestHashMap(unittest.TestCase):
    def test_put_get(self):
        """test put and get functionality"""
        hm = HashMap()
        hm.put("a", 1)
        hm.put("b", 2)

        self.assertEqual(hm.get("a"), 1)
        self.assertEqual(hm.get("b"), 2)

    def test_collision_handling(self):
        """testing HashMap collisions with chaining"""
        hm = HashMap(1)  
        hm.put("a", 1)
        hm.put("b", 2)
        hm.put("c", 3)

        self.assertEqual(hm.get("a"), 1)
        self.assertEqual(hm.get("b"), 2)
        self.assertEqual(hm.get("c"), 3)

    def test_rehashing(self):
        """Testing that rehasing preserves key-value pairs"""
        hm = HashMap(2)

        for i in range(10): 
            hm.put(i, i * 10)

        for i in range(10):
            self.assertEqual(hm.get(i), i * 10)


class TestPrerequisites(unittest.TestCase):

    def test_prereq_success(self):
        """testing that enrollment succeeds when prerequisites are met"""
        course = Course("C1", "Test", 10)
        student = Student("1", "Charmi")

        student.add_completed("CSE2050")
        course.add_prerequisite("CSE2050")

        result = course.request_enroll(student)
        self.assertEqual(result, "Enrolled")

    def test_prereq_failure(self):
        """"tests that enrollment fails when prerequisites are missing"""
        course = Course("C1", "Test", 10)
        student = Student("1", "Sneha")

        course.add_prerequisite("CSE2050")

        with self.assertRaises(Exception):
            course.request_enroll(student)


class TestSorting(unittest.TestCase):

    def test_merge_sort(self):
        """test merge sort returns correctly sorted list"""
        arr = [5, 2, 9, 1, 3]
        sorted_arr = merge_sort(arr)
        self.assertEqual(sorted_arr, [1, 2, 3, 5, 9])

    def test_quick_sort(self):
        """test quicksort returns correctly sorted list"""
        arr = [5, 2, 9, 1, 3]
        sorted_arr = quick_sort(arr)
        self.assertEqual(sorted_arr, [1, 2, 3, 5, 9])


if __name__ == "__main__":
    unittest.main()