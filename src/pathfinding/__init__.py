import os
import sys

data_base_dir = None

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    data_base_dir = "data"
else:
    data_base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 "data")

icon_path = os.path.join(data_base_dir, "icon.png")