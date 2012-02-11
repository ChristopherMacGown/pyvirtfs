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
from virtfs.drivers import configfs
from virtfs.drivers import procfs
from virtfs.drivers import sysfs


sysfs = sysfs.SysFS()
procfs = procfs.ProcFS()

if drivers.resolve_virtfs_path(configfs.ConfigFS):
    # ConfigFS may not be enabled, so we don't want to enable it if it isn't.
    configfs = configfs.ConfigFS()
else:
    del configfs
