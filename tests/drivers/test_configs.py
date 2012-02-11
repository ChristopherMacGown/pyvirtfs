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
from virtfs.drivers import configfs

from tests import utils


class TestConfigFS(utils.TestHelper):
    def setUp(self):
        drivers.PROC_MOUNTS_PATH = utils.testdata("proc_mounts_with_configfs")
        self.configfs = configfs.ConfigFS()

    def test_trying_to_find_an_entry_that_doesnt_exist(self):
        try:
            self.configfs.foo
        except exc.NotFound:
            self.assertTrue(True, )
        except:
            self.assertFalse(True,
                             "expected configfs.foo to raise exc.NotFound")

    def test_trying_to_find_an_entry_that_exists(self):
        self.assertTrue(self.configfs.fakenbd)
        self.assertEqual(['nbd1',], self.configfs.fakenbd.contents)
        self.assertEqual('<ConfigFS tests/data/fakeconfigfs/fakenbd>',
                         str(self.configfs.fakenbd))

    def test_walk_to_a_file_not_just_a_directory_entry(self):
        self.assertTrue(self.configfs.fakenbd.nbd1.target)
        self.assertEqual('fakeip\n', self.configfs.fakenbd.nbd1.target.contents)
        self.assertEqual('', self.configfs.fakenbd.nbd1.rw.contents)
        self.assertEqual('<ConfigFS '
                         'tests/data/fakeconfigfs/fakenbd/nbd1/target>\n'
                         'fakeip\n',
                         str(self.configfs.fakenbd.nbd1.target))

    def test_resolve_virtfs_path(self):
        self.assertEqual('tests/data/fakeconfigfs',
                          drivers.resolve_virtfs_path(configfs.ConfigFS))
