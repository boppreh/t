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

    def test_list_itself(self):
        task_list = T()
        self.assertEqual(len(task_list), 0)

        task = task_list.create('Task')
        self.assertEqual(len(task_list), 1)
        self.assertEqual(task_list[task.id], task)

        task_list.destroy(task)
        self.assertEqual(len(task_list), 0)

    def test_serialize(self):
        task_list = T()
        task1 = task_list.create('Task 1')
        task2 = task_list.create('Task 2')
        task_list.finish(task2)
        task_list.activate(task1)

        string = str(task_list)

        new_task_list = T.parse(string)
        self.assertEqual(len(new_task_list), 2)
        self.assertEqual(new_task_list[task1.id], task1)
        self.assertEqual(new_task_list[task2.id], task2)
        self.assertIsNotNone(new_task_list[task2.id].end)
        self.assertTrue(new_task_list[task1.id].is_active)

if __name__ == '__main__':
    unittest.main()
