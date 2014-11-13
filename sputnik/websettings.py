import os
dirname = os.path.dirname(__file__)
rootdir = os.path.dirname(dirname) # Up one directory level.

WEB_ROOT = os.path.join(rootdir, 'web')
STATIC_PATH = os.path.join(WEB_ROOT, 'static')
TEMPLATE_PATH = WEB_ROOT
