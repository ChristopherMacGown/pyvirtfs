class NotFound(IOError):
    def __init__(self, path):
        super(NotFound, self).__init__("%s: No such file or directory" % path)
