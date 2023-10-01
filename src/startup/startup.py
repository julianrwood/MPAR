import logging
import sys 
import importlib

logging.info('mediaplayer.src.startup.py: begining startup procedures')

# This loads our project into the path variable
sys.path.append('C:/Users/Julian/projects/python/mediaPlayer')

import src.ui.ui as ui
# Launch our ui
ui.main()