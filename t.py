from time import time
import re

class Task(object):
    """
    Class representing a single task. Its just a value store and is usually
    paired with a TaskList that manages it.
    """
    def __init__(self, id, name, start=None, end=None, is_active=False):
        self.id = id
        self.name = name
        self.start = start
        self.end = end
        self.is_active = is_active

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False

        return (self.id == other.id and
                self.name == other.name and
                self.start == other.start and
                self.end == other.end and
                self.is_active == other.is_active)

    def __repr__(self):
        return '[{}{} {}-{} "{}"]'.format(self.id,
                                          '!' if self.is_active else '',
                                          self.start,
                                          self.end if self.end else '',
                                          self.name)

class TaskList(object):
    """
    List of tasks. Capable of loading and writing to files or strings.

    Each task list creates tasks with locally unique ids and may have one task
    set as "active".
    """
    def __init__(self, tasks_by_id=None, active=None):
        self.tasks_by_id = tasks_by_id or {}
        self.active = active or None
        self.last_id = max(self.tasks_by_id) if len(self.tasks_by_id) else 0

    def create(self, task_name):
        """
        Creates and returns a new incomplete and inactive task with the given
        name.
        """
        self.last_id += 1
        task = Task(self.last_id,
                    task_name,
                    start=int(time()),
                    end=None,
                    is_active=False)
        self.tasks_by_id[self.last_id] = task
        return task

    def destroy(self, task):
        """
        Removes the given task, deactivating it first if necessary.
        """
        if task == self.active:
            self.deactivate()
        del self.tasks_by_id[task.id]

    def activate(self, task):
        """
        Replaces the previously active task with the given one.
        """
        if self.active is not None:
            self.deactivate()

        self.active = task
        task.is_active = True

    def deactivate(self):
        """
        Deactivates the currently active task, leaving a None value. If there
        is no active task, it does nothing.
        """
        if self.active is not None:
            self.active.is_active = False
            self.active = None

    def finish(self, task):
        """
        Marks a task as finished.
        """
        task.end = int(time())

    def __len__(self):
        """
        Returns the total number of tasks.
        """
        return len(self.tasks_by_id)

    def __getitem__(self, id):
        """
        Returns a task by its id.
        """
        return self.tasks_by_id[id]

    def __repr__(self):
        result = []
        for task in self.tasks_by_id.values():
            result.append(str(task) + '\n')
        return ''.join(result)

    def save(self, path):
        """
        Writes this task list to a file.
        """
        with open(path, 'w') as f:
            f.write(str(self).encode('utf-8'))

    @staticmethod
    def load(path):
        """
        Loads a task list from a file.
        """
        with open(path, 'r') as f:
            text = f.read()
        return TaskList.parse(text)

    @staticmethod
    def parse(string):
        """
        Creates a task list from the given serialized string.
        """
        active = None
        tasks_by_id = {}

        task_pattern = '\[(\d+)(!?) (\d+)-(\d*) "(.+)"\]\n'
        for parts in re.findall(task_pattern, string):
            id = int(parts[0])
            is_active = parts[1] == '!'
            start = int(parts[2])
            end = int(parts[3]) if parts[3] else None
            name = parts[4]
            task = Task(id=id,
                        name=name,
                        start=start,
                        end=end,
                        is_active=is_active)

            assert id not in tasks_by_id
            tasks_by_id[id] = task
            if is_active:
                assert active is None
                active = task

        return TaskList(tasks_by_id=tasks_by_id, active=active)


if __name__ == '__main__':
    t = TaskList()
    print(t.create('a'))
    print(t)
