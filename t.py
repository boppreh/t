from time import time

class Task(object):
    def __init__(self, id, name, start=None, end=None, is_active=False):
        self.id = id
        self.name = name
        self.start = start
        self.end = end
        self.is_active = is_active

    def __repr__(self):
        return '[{} {}{} {}-{}]'.format(self.id,
                                        '!' if self.is_active else '',
                                        repr(self.name),
                                        self.start,
                                        self.end if self.end else '')

class T(object):
    def __init__(self):
        self.tasks_by_id = {}
        self.last_id = 0
        self.active = None

    def create(self, task_name):
        self.last_id += 1
        task = Task(self.last_id,
                    task_name,
                    start=int(time()),
                    end=None,
                    is_active=False)
        self.tasks_by_id[self.last_id] = task
        return task

    def activate(self, task):
        if self.active is not None:
            self.deactivate()

        self.active = task
        task.is_active = True

    def deactivate(self):
        if self.active is not None:
            self.active.is_active = False
            self.active = None

    def finish(self, task):
        task.end = int(time())

if __name__ == '__main__':
    print(T().create('a'))
