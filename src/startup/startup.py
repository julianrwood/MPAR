import logging
import sys 
import importlib

"""
This is the main entry point to the program. 
We probably do some dodgy shit here but i'm not smart enough to know why this is a shitty idea

I've wrapped it into it's own function so that forks can just call this function from wherever and 
im-bed it into whatever custom DCC and anything else they'd like.

You'd really just need to take the returned "software" variable and use that. It's just a QMainWindow
"""

def startMyBoiUp():
    """
    This is the entry point for the progam
    """

    logging.info('MPAR.src.startup.py: initialising startup procedures')
    # Set the icon location and append it to the path directory
    selfLocation = __file__
    iconLocation = selfLocation.replace('\src\startup\startup.py','')
    sys.path.append(iconLocation)

    #Import and launch our ui
    import src.ui.ui as ui
    # Launch our ui
    software = ui.main()
    return software

startMyBoiUp()