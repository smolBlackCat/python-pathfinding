"""languages.py module.

This module handles all the language translation issues."""

import json
import locale
import os

from . import data_base_dir

fd = None

try:
    fd = open(os.path.join(data_base_dir, f"{locale.getdefaultlocale()[0]}.json"))
except FileNotFoundError:
    # Defaults to British English
    fd = open(os.path.join(data_base_dir, "en_GB.json"))

message_map = json.load(fd)

fd.close()
