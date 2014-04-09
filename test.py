import unittest
from time import time
from t import T

class TestT(unittest.TestCase):
    def test_basic(self):
        task_list = T()

        task = task_list.create('Task name')
        self.assertEqual(task.name, 'Task name')
        self.assertTrue(abs(task.start - time()) <= 1)

        self.assertFalse(task.is_active)
        self.assertIsNone(task_list.active)
        task_list.activate(task)
        self.assertEqual(task_list.active, task)
        self.assertTrue(task.is_active)
        task_list.deactivate()
        self.assertIsNone(task_list.active)
        self.assertFalse(task.is_active)

        self.assertIsNone(task.end)
        task_list.finish(task)
        self.assertTrue(abs(task.end - time()) <= 1)

    def test_two_tasks(self):
        task_list = T()
        task1 = task_list.create('Task 1')
        task2 = task_list.create('Task 2')

        task_list.activate(task1)
        task_list.activate(task2)
        self.assertFalse(task1.is_active)
        self.assertTrue(task2.is_active)
        self.assertEqual(task_list.active, task2)

if __name__ == '__main__':
    unittest.main()
