import sqlite3
from typing import Dict, List, Tuple

import os


connection = sqlite3.connect(os.path.join('db', 'finances.db'))
cursor = connection.cursor()

