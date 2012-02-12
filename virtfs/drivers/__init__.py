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
VIRTFS_LEAFS = {}


def register_leaf(name):
    def register_class(cls):
        VIRTFS_LEAFS[name] = cls
    return register_class


def resolve_to_leafclass(virtfs_driver):
    '''Given a Driver, return the appropriate leaf class'''
    return VIRTFS_LEAFS[virtfs_driver.__name__.lower()]


def resolve_virtfs_path(virtfs_driver):
    '''Given a virtfs driver, determine where that filesystem is mounted'''

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
    '''The base VirtFSDriver provides access to Linux virtual filesystems.'''

    def __init__(self, virtfs_path=None):
        self._virtfs_path = virtfs_path

    def __dir__(self):
        '''If this node is a directory, add the list of contained files to its
        parent dir(). If this node is a file or is filelike, add ['contents']
        to the parent dir().
        '''

        # TODO(chris): Fix the docstring

        return dir(object) + os.listdir(self._virtfs_path)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            obj = type(self)._create(os.path.join(self._virtfs_path, name))
            setattr(self, name, obj)
            return getattr(self, name)

    def __repr__(self):
        return "<%s mounted at %s>" % (self.__class__.__name__,
                                       self._virtfs_path)

    def __setattr__(self, name, value):
        try:
            child = super(VirtFSDriver, self).__getattribute__(name)
        except AttributeError:
            child = None

        if not child and name.startswith('_'):
            object.__setattr__(self, name, value)
        elif not child and self.is_child(name):
            super(VirtFSDriver, self).__setattr__(name, value)
        elif child:
            child.set(value)

    def is_child(self, name):
        return os.path.exists(os.path.join(self._virtfs_path, name))

    @property
    def contents(self):
        '''If this is a directory node, return the list of contained files. If
        this is a file or filelike object, return the contents of the file.
        '''

        return [d for d in dir(self) if d not in dir(object)]

    @classmethod
    def _create(cls, path):
        '''Build a child node and store it in __dict__'''
        if not os.path.exists(path):
            raise exc.NotFound(path)

        if os.path.isfile(path):
            cls = resolve_to_leafclass(cls)
        return cls(path)


class VirtFSItem(object):
    def __init__(self, path, lazy_load=True):
        self._virtfs_item_path = path
        self._contents = None
        if not lazy_load:
            self._load()

    def _load(self):
        with open(self._virtfs_item_path, 'r') as contents:
            self._contents = contents.read()
        return self._contents

    def __repr__(self):
        return '<%s at %s>' % (self.__class__.__name__, self._virtfs_item_path)

    def __enter__(self):
        return self.contents

    def __exit__(self, *args):
        pass

    def set(self, value, auto_save=True):
        raise NotImplementedError("%s is not writeable." 
                                  % self.__class__.__name__)

    @property
    def contents(self):
        if self._contents:
            return self._contents
        return self._load()


class WriteableVirtFSItem(VirtFSItem):
    '''A VirtFSItem that can be written back to the virtual filesystem.'''
    def __init__(self, path, lazy_load=True):
        super(WriteableVirtFSItem, self).__init__(path, lazy_load)
        self._tmp_virtfs_item_path = os.path.join('/tmp/',
                                                  self._virtfs_item_path)
    def set(self, value, auto_save=True):
        self._contents = value
        if auto_save:
            self.save()

    def _guarantee_tempdir(self):
        tempdir = os.path.dirname(self._tmp_virtfs_item_path)
        if not os.path.exists(tempdir):
            os.makedirs(tempdir, 0700)

    def save(self):
        self._guarantee_tempdir()
        with open(self._tmp_virtfs_item_path, 'w') as contents:
            contents.write(self._contents if self._contents else '')

        try:
            os.rename(self._tmp_virtfs_item_path, self._virtfs_item_path)
            os.removedirs(os.path.dirname(self._tmp_virtfs_item_path))
        except IOError, e:
            raise exc.CouldNotSetValueError(e)

        return self
