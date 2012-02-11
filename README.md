# pyvirtfs

A python package that provides access to the Linux virtual filesystems proc,
sys, and configfs.


## Examples

    from virtfs import sysfs
    block = sysfs.block
    block.contents
    print block.sda.queue.rotational.contents



    from virtfs import procfs
    mounts = procfs.contents
    print mounts.contents


    from virtfs import configfs
    fakenbd = configfs.fakenbd
    print fakenbd.contents
