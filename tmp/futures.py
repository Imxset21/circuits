# Module:   future
# Date:     6th February 2010
# Author:   James Mills, prologic at shortcircuit dot net dot au

"""Futures

Future Value object and decorator wrapping a Thread (by default).
"""

from uuid import uuid4 as uuid
from functools import update_wrapper

from pools import NewTask, Task, Worker

def future():
    def decorate(f):
        def wrapper(self, event, *args, **kwargs):
            event.future = True
            pool = getattr(self, "pool", None)
            if pool:
                return self.push(NewTask(f, self, *args, **kwargs),
                        target=self._pool)
            else:
                return Worker(str(uuid())).push(
                        Task(f, self, *args, **kwargs))
        wrapper.event = True
        return update_wrapper(wrapper, f)
    return decorate
