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
+ exr, tx, png and other image sequence support
+ Add OIIO support (I need to work out how to build stuff directly into the project)
+ Additional colorspace support including viewing transforms and stuff like that
+ Exposure, gamma and saturation adjustments
+ Add a non-linear timeline, basically a premiere pro, davinci resolve, sony vegas or avid type editing timeline.
  
Utility
+ Contact sheets views
+ Sequence views
+ Annotations being saved directly onto the QGraphics objects that an Imageclass is linked to - Done
+ It is important that we try to separate the underlying hardcode to any utility functionality that we might want to add. Creating
      an MPAR Resources directory and having easily accessible exposure to all aspects of the underlying code would be good. I:e An API ( We want an API to allow anyone at any level            to easily add what they want without needing to understand the entire source code.
+ Allow external DCC App Integration. (Basically can we call this program and have it launch in any software we like. ( This would make it useful for viewing image textures
      for whatever package you want) - Done but not tested

System
+ Sync sessions for multiple people viewing (I want this to be something that's hosted on a users machine and then streamed to a connected user)
