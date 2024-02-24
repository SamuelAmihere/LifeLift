#! /usr/bin/env python3

import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('LFTLIFT_MYSQL_USER'))
print(os.getenv('LFTLIFT_MYSQL_PWD'))
print(os.getenv('LFTLIFT_MYSQL_HOST'))
print(os.getenv('LFTLIFT_MYSQL_DB'))