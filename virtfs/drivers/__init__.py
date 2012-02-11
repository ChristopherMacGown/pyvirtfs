# Copyright 2012 Christopher MacGown. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os

from virtfs import exc


PROC_MOUNTS_PATH = "/proc/mounts"

def resolve(path):
    if not os.path.exists(path):
        return False
    return True 


def resolve_virtfs_path(virtfs_driver):
    virtfs_driver = virtfs_driver.__name__.lower()
    if virtfs_driver == 'procfs':
        virtfs_driver = 'proc'  # flipping non-standard fs name.

    try:
        with open(PROC_MOUNTS_PATH, "r") as mounts:
            mounts = mounts.read()
            mount = [m for m in mounts.split('\n') if virtfs_driver in m]
            mount = mount[0].split(' ')[1] if mount else None
    except IOError:
        mount = None
    return mount


class VirtFSDriver(object):
    def __init__(self, virtfs_path=None, contents=None):
        self._virtfs_path = virtfs_path
        self._contents = contents

    def __dir__(self):
        parent_dir = dir(object)
        if self._contents is None:
            return parent_dir + os.listdir(self._virtfs_path)
        else:
            return parent_dir + ['contents',]

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            obj = type(self)._create(os.path.join(self._virtfs_path, name))
            setattr(self, name, obj)
            return getattr(self, name)

    def __str__(self):
        msg = "<%s %s>" % (self.__class__.__name__, self._virtfs_path)
        if self._contents:
            msg += "\n%s" % self._contents
        return msg

    def __enter__(self):
        return self.contents

    def __exit__(self, *args):
        pass

    @property
    def contents(self):
        if self._contents is not None:
            return self._contents
        else:
            return [d for d in dir(self) if d not in dir(object)]

    @classmethod
    def _create(cls, path):
        if not resolve(path):
            raise exc.NotFound(path)

        contents = None
        if os.path.isfile(path):
            with open(path, 'r') as f:
                contents = f.read()
        return cls(path, contents)
