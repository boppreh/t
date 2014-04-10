import time
import re

class Task(object):
    """
    Class representing a single task. Its just a value store and is usually
    paired with a TaskList that manages it.
    """
    TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

    def __init__(self, name, start=None, end=None, is_active=False):
        self.name = name
        self.start = start
        self.end = end
        self.is_active = is_active

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False

        return (self.name == other.name and
                self.start == other.start and
                self.end == other.end and
                self.is_active == other.is_active)

    def _format_date(self, t):
        return time.strftime(Task.TIME_FORMAT, time.localtime(t))

    def __repr__(self):
        if self.is_active:
            template = '[{}] {} ({} - {})'
        else:
            template = ' {}  {} ({} - {})'
        return template.format('x' if self.end else ' ',
                               self.name,
                               self._format_date(self.start),
                               self._format_date(self.end) if self.end else '?')

class TaskList(object):
    """
    List of tasks. Capable of loading and writing to files or strings.
    """
    def __init__(self, tasks=None, active=None):
        self.tasks = tasks or []
        self.active = active or None

    def create(self, task_name):
        """
        Creates and returns a new incomplete and inactive task with the given
        name.
        """
        task = Task(task_name,
                    start=int(time.time()),
                    end=None,
                    is_active=False)
        self.tasks.insert(0, task)
        return task

    def destroy(self, task):
        """
        Removes the given task, deactivating it first if necessary.
        """
        if task == self.active:
            self.deactivate()
        self.tasks.remove(task)

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
        task.end = int(time.time())

    def __len__(self):
        """
        Returns the total number of tasks.
        """
        return len(self.tasks)

    def __repr__(self):
        return ''.join(str(task) + '\n' for task in self.tasks)

    def save(self, path):
        """
        Writes this task list to a file.
        """
        with open(path, 'w') as f:
            f.write(str(self))

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
        tasks = []

        # Format examples:
        # [ ] Task name (2014/04/09 23:23:23 - ?)
        # [x] Task name (2014/04/09 23:23:23 - 2014/04/09 23:23:23)
        #  x  Task name (2014/04/09 23:23:23 - 2014/04/09 23:23:23)
        #     Task name (2014/04/09 23:23:23 - ?)
        task_pattern = '''
        ^
        (\[|\s)    # Optional open bracket for active tasks.
        (x|\s)     # Optional 'x' for closed tasks.
        (?:\]|\s)  # No need to capture, this will be the same as the first.
        \s

        (.+?)      # Task name.

        \s?
        \(
        (.+?)      # Start date.
        \s?-\s?
        (.+|\?)    # Optional end date, it's an ? if not present.
        \)
        $
        '''
        for parts in re.findall(task_pattern, string, re.VERBOSE | re.MULTILINE):
            is_active = parts[0] == '['
            name = parts[2]
            start = time.mktime(time.strptime(parts[3], Task.TIME_FORMAT))
            if parts[4] == '?':
                end = None
            else:
                end = time.mktime(time.strptime(parts[4], Task.TIME_FORMAT))

            # There are two signals for it to be complete: the "x" and the end
            # date. Those two should not be contradictory.
            assert (parts[4] != '?') == (parts[1] == 'x')

            task = Task(name=name,
                        start=start,
                        end=end,
                        is_active=is_active)
            tasks.append(task)

            if is_active:
                # Should have only one active task.
                assert active is None
                active = task

        return TaskList(tasks=tasks, active=active)


class FileTaskList(TaskList):
    """
    Task list that is persisted in a file. 
    """
    def __init__(self, path):
        """
        Creates a new FileTaskList from the task list in the given path. If
        path does not exist, an empty file is created.

        The path is remembered for future operations.
        """
        # Make sure the file exists.
        open(path, 'a').close()
        self.path = path
        self.reload()

    # Must allow passing of parameters to not violate the superclass behavior.
    def save(self, path=None):
        """
        Saves the task list to the given path, or its own if none is given.
        """
        super(FileTaskList, self).save(path or self.path)

    def reload(self):
        """
        Discards the changes made and reloads the tasks from its own path.
        """
        base_task_list = TaskList.load(self.path)
        self.tasks = base_task_list.tasks
        self.active = base_task_list.active


if __name__ == '__main__':
    task_list = FileTaskList('tasks.txt')

    print(task_list)
    new_task = input('New task: ')
    if new_task:
        task_list.create(new_task)
        task_list.save()
        print('Task created.')
    else:
        print('No task created.')
