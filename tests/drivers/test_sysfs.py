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


from virtfs import drivers
from virtfs import exc
from virtfs.drivers import sysfs

from tests import utils


class TestSysFS(utils.TestHelper):
    def setUp(self):
        drivers.PROC_MOUNTS_PATH = utils.testdata("proc_mounts")
        self.sysfs = sysfs.SysFS()

    def test_trying_to_find_an_entry_that_doesnt_exist(self):
        try:
            self.sysfs.foo
        except exc.NotFound:
            self.assertTrue(True, )
        except:
            self.assertFalse(True, "expected sysfs.foo to raise exc.NotFound")

    def test_trying_to_find_an_entry_that_exists(self):
        self.assertTrue(self.sysfs.block)
        self.assertEqual(['sda',], self.sysfs.block.contents)
        self.assertEqual('<SysFS tests/data/fakesysfs/block>',
                         str(self.sysfs.block))

    def test_walk_to_a_file_not_just_a_directory_entry(self):
        self.assertTrue(self.sysfs.block.sda.dev)
        with self.sysfs.block.sda.dev as contents:
            self.assertEqual("8:0\n", contents)
        self.assertEqual('<SysFS tests/data/fakesysfs/block/sda/dev>\n8:0\n',
                         str(self.sysfs.block.sda.dev))

        self.assertTrue(self.sysfs.block.sda.capability)
        with self.sysfs.block.sda.capability as contents:
            self.assertEqual("50\n", contents)
        self.assertEqual('<SysFS tests/data/fakesysfs/block/sda/capability>'
                         '\n50\n',  # The continuation of above   
                        str(self.sysfs.block.sda.capability))

    def test_resolve_virtfs_path(self):
        self.assertEqual('tests/data/fakesysfs',
                          drivers.resolve_virtfs_path(sysfs.SysFS))
