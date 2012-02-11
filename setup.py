from distutils.core import setup

description = '''A package providing access to the Linux virtual filesystems    
proc, sysfs, and configfs.'''

setup(name='virtfs',
      description=description,
      version='0.9',
      author='Christopher MacGown',
      author_email='ignoti@gmail.com',
      url='',
      packages=['virtfs', 'virtfs/drivers'],)
