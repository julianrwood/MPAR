# MPAR
A pyqt based media player for vfx reviews


MPAR: stands for Media Player And Review

# Dependencies
- Pyqt5
- qdarkgraystyle (This will get removed as I manually set the themes and stylesheets
- imageio
- numpy

# Look at the project
It's currently a work in progress but this is what it's looking like so far. I will continue to expand and work on it as I go
![Capture](https://github.com/julianrwood/MPAR/assets/69379151/a1273b17-2ddd-4d29-88bc-e1db5212a10e)



# List of ToDos
production
+ Add exr support
+ Mov, mp4 and other movie type support
+ exr, png and other image sequence support
+ Add OIIO support (I need to work out how to build stuff directly into the project)
+ Additional colorspace support including viewing transforms and stuff like that
+ Exposure, gamma and saturation adjustments

Utility
+ Contact sheets views
+ Sequence views
+ Annotations being saved directly onto the QGraphics objects that an Imageclass is linked to

System
+ Sync sessions for multiple people viewing (I want this to be something that's hosted on a users machine and then streamed to a connected user)
