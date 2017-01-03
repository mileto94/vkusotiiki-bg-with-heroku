import os
from socket import gethostname

host_name = gethostname()

settings_path = os.path.abspath(os.path.dirname(__file__))

if 'milka' in host_name:
    current_settings = 'dev_settings'
else:
    current_settings = 'live_settings'

print("Loading setting...", current_settings)

filename = os.path.join(settings_path, "{settings}.py".format(settings=current_settings))

try:
    exec(
        compile(
            open(filename, "rb").read(),
            filename,
            'exec'),
        globals(),
        locals())
except IOError:
    raise Exception("Could not import %s" % current_settings)
