from dotenv import load_dotenv

import os
from pathlib import Path

load_dotenv()
email = os.getenv('EMAIL_ID')
password = os.getenv('PASSWORD')


print(email , password)