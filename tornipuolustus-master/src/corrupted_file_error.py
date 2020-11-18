
class CorruptedFileError(Exception):
    
    def __init__(self, message):
        super(CorruptedFileError, self).__init__(message)