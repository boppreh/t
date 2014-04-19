import unittest
from time import time
from t import TaskList

class TestTaskList(unittest.TestCase):
    def test_basic(self):
        task_list = TaskList()

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
        task_list.close(task)
        self.assertTrue(abs(task.end - time()) <= 1)
        task_list.reopen(task)
        self.assertIsNone(task.end)

    def test_two_tasks(self):
        task_list = TaskList()
        task1 = task_list.create('Task 1')
        task2 = task_list.create('Task 2')

        task_list.activate(task1)
        task_list.activate(task2)
        self.assertFalse(task1.is_active)
        self.assertTrue(task2.is_active)
        self.assertEqual(task_list.active, task2)

    def test_list_itself(self):
        task_list = TaskList()
        self.assertEqual(len(task_list), 0)

        task = task_list.create('Task')
        self.assertEqual(len(task_list), 1)

        task_list.destroy(task)
        self.assertEqual(len(task_list), 0)

    def test_serialize(self):
        task_list = TaskList()
        task1 = task_list.create('Task 1')
        task2 = task_list.create('Task 2')
        task_list.close(task2)
        task_list.activate(task1)

        string = str(task_list)

        new_task_list = TaskList.parse(string)
        self.assertEqual(len(new_task_list), 2)
        self.assertEqual(new_task_list.tasks, task_list.tasks)

if __name__ == '__main__':
    unittest.main()
