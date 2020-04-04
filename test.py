'''
Sample program
'''

# Imports
from clip import *                      # code for playing videos
from clip_interactions import *         # code for interacting with user


# Show a black screen
showBlack()
# could put a pause here, so viewers see a blank screen until we are ready

# Prepare all the clips
eyes = Clip('eyes.mp4')
laser = Clip('laser.mp4')
print3d = Clip('print3d.mp4')

# Create some interactions on the eyes clips
eyesInteractions = ClipInteractions()
eyesInteractions.addInteraction("Laser", ButtonInteraction(600,500,250,125, "Laser", time=10, duration=5, activated=True))
eyesInteractions.addInteraction("3DPrint", ButtonInteraction(300,500,250,125, "3D Print", time=10, duration=5, activated=False))
eyes.addInteractions(eyesInteractions)

# Play the clips
eyes.play()
if eyesInteractions["3DPrint"].activated:
    print3d.play()
else:
    laser.play()

stopVideos()
