"""
Class to manage playing and control of video clips.

"""
import numpy as np

# Import OpenCV
# This gives us the video image handling functionality
# You also need to install opencv-python: https://pypi.org/project/opencv-python/
import cv2 

# Import FF Py Player
# This gives us the video sound handling functionality
# See https://pypi.org/project/ffpyplayer/
import ffpyplayer.player as ffp

# Other imports
import datetime
import time

# Window name that OpenCV will use
window_name = "window"

class Clip():
    '''A class to handle all the video play and control'''

    def __init__(self, fileName):
        '''Initialise the player with a video file'''

        self.fileName = fileName

        # Load the video part using cv2
        self.video = cv2.VideoCapture(fileName)

        # Read in the video metadata
        self.fps = self.video.get(cv2.CAP_PROP_FPS)                          # frame per second
        self.frameCount = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))      # number of frames in the clip
        self.durationSeconds = self.frameCount/self.fps                     # clip duration in seconds

        self.interactions = None

    def play(self):

        # Load the sound part using ffpyplayer
        self.player = ffp.MediaPlayer(self.fileName)

        # Compute average no of milliseconds between frames
        frame_delay = int(1000/self.fps)

        # Record the time we started the clip.  This will be needed to sync the video and sound
        startTime = datetime.datetime.now()

        # Loop, displaying one frame at a time
        frameNo = 0
        while True:
            # Get the video image frame
            grabbed, frame = self.video.read()
            if not grabbed:
                break # we reached the end of the video

            # Get the frame from the audio stream
            audio_frame, val = self.player.get_frame(show=False)    # show=False means don't get video frame
            if val == 'eof':
                break # we reached the end of the video

            # Calculate the time we need to wait before showing the current frame
            # Sound will play in real time.  We need to adjust image display to sync with the sound
            nowTime = datetime.datetime.now()                           # time now
            soundTime = (nowTime - startTime).total_seconds()*1000      # milliseconds since start of sound
            imageTime = frameNo*frame_delay                             # milliseconds position where this image should be shown 
            frame_wait = int(imageTime-soundTime)                       # time to wait before moving to the next image
            if frame_wait<0: frame_wait=0                               # if negative, means the sound is ahead of image, so skip this image

            #print(frameNo, frameTime, actualTime, frame_wait)

            # If we need to wait, display the frame for the wait time, otherwise we will skip the frame
            if frame_wait>0:
                # Process any interactions with this frame
                self._processInteractions(frame, soundTime) 

                # Display the image
                cv2.imshow(window_name, frame)
             
                # Display the image for the given number of milliseconds
                if cv2.waitKey(frame_wait) & 0xFF == ord("q"):
                    break

            # Increment the frame count
            frameNo += 1
            
        self.video.release()
        self.player.close_player()

    def addInteractions(self, interactions):
        '''Add a set of interactions to this clip'''
        self.interactions = interactions
        cv2.setMouseCallback(window_name, self.interactions.handleMouse)


    def _processInteractions(self, frame, t):
        '''Process any interactions on this clip'''
        if self.interactions is not None:
            self.interactions.processInteractions(frame, t) 

             
            

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()


# Set up for full screen display
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def stopVideos():
    cv2.destroyAllWindows()        

def showBlack():
    img = np.ones((512,512,3), np.uint8)
    cv2.imshow(window_name, img)
    cv2.waitKey(1)


    #cv2.setMouseCallback(window_name,mousey)