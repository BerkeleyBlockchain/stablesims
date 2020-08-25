""" Environment Module

Loads in environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()

COIN_API_KEY = os.getenv("COIN_API_KEY")
