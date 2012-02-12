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
from virtfs.drivers import procfs

from tests import utils


class TestProcFS(utils.TestHelper):
    def setUp(self):
        drivers.PROC_MOUNTS_PATH = utils.testdata("proc_mounts")
        self.procfs = procfs.ProcFS()

    def test_trying_to_find_an_entry_that_doesnt_exist(self):
        self.assertRaises(exc.NotFound, getattr, self.procfs, 'foo')

    def test_trying_to_find_an_entry_that_exists(self):
        self.assertTrue(self.procfs.driver)
        self.assertEqual(['nvram', 'rtc',], self.procfs.driver.contents)
        self.assertEqual('<ProcFS mounted at tests/data/fakeprocfs/driver>',
                         str(self.procfs.driver))

    def test_walk_to_a_file_not_just_a_directory_entry(self):
        self.assertTrue(self.procfs.driver.nvram)
        self.assertTrue("Gfx adapter" in self.procfs.driver.nvram.contents)

        self.assertEqual(['contents'], [d for d 
                                          in dir(self.procfs.driver.nvram)
                                          if not d.startswith('_')])

    def test_resolve_virtfs_path(self):
        self.assertEqual('tests/data/fakeprocfs',
                          drivers.resolve_virtfs_path(procfs.ProcFS))
