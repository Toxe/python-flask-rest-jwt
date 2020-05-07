import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or b"\xb0\xb3\n\xe1\xeep'\xdc\x9a\x1bm\xa4\xce\x81\xd5\x9fW^\xd0h"
