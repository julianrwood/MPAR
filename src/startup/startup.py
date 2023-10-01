import logging
import sys 
import importlib

logging.info('MPAR.src.startup.py: initialising startup procedures')

# Set icons for undo and redo buttons
selfLocation = __file__
iconLocation = selfLocation.replace('\src\startup\startup.py','')

sys.path.append(iconLocation)

import src.ui.ui as ui
# Launch our ui
ui.main()