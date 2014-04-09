from time import time

class Task(object):
    def __init__(self, name, start=None, end=None, is_active=False):
        self.name = name
        self.start = start
        self.end = end
        self.is_active = is_active

    def __repr__(self):
        return '[{}{} {}-{}]'.format('!' if self.is_active else '',
                                       repr(self.name),
                                       self.start,
                                       self.end if self.end else '')

class T(object):
    def __init__(self):
        pass

    def create(self, task_name):
        return Task(task_name, start=int(time()), end=None, is_active=False)

    def activate(self, task):
        task.is_active = True
        return task

    def finish(self, task):
        task.end = int(time())
        return task

if __name__ == '__main__':
    print(T().create('a'))
