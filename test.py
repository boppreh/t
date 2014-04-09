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
        task_list.activate(task)
        self.assertTrue(task.is_active)
        task_list.deactivate(task)
        self.assertFalse(task.is_active)

        self.assertIsNone(task.end)
        task_list.finish(task)
        self.assertTrue(abs(task.end - time()) <= 1)

if __name__ == '__main__':
    unittest.main()
