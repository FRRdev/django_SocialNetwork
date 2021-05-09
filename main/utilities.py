from datetime import datetime
from os.path import splitext

def get_timestamp_path(instance, filename): # generates the names of the uploaded files stored in the module
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])