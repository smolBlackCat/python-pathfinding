"""languages.py module.

This module handles all the language translation issues."""


# TODO: Implement message translation system
# Ad hoc procedure of how it works.
# 1. Get the current system locale
# 2. Based on the current locale, get the translation file in data
# 3. Load the messages into memory

import json
import locale
import os

from . import data_base_dir

message_map = json.load(open(os.path.join(data_base_dir, f"{locale.getlocale()[0]}.json")))
