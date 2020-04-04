"""
Class to manage video interactions

"""
import cv2 

class Interaction():
    pass

class ButtonInteraction(Interaction):
    def __init__(self, x, y, w, h, text, time, duration, activated = False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.time = time
        self.duration = duration
        self.activated = activated

class ClipInteractions():
    def __init__(self):
        self.interactions = {}

    def __getitem__(self, item):
         return self.interactions[item]        

    def addInteraction(self, name, interaction):
        self.interactions[name] = interaction

    def processInteractions(self, frame, timeSeconds):
        for name in self.interactions: 
            interaction = self.interactions[name]
            if timeSeconds > interaction.time*1000 and timeSeconds < (interaction.time+interaction.duration)*1000:
                cv2.rectangle(frame, (interaction.x, interaction.y),(interaction.x+interaction.w, interaction.y+interaction.h), (0,255,0), 3)
                cv2.putText(frame, interaction.text, (interaction.x, interaction.y), cv2.FONT_HERSHEY_SIMPLEX , fontScale=1, color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA) 

    def handleMouse(self, event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:  
            print("EVENT_LBUTTONDBLCLK")
        elif event == cv2.EVENT_LBUTTONDOWN:
            print("EVENT_LBUTTONDOWN")   


            for name in self.interactions: 
                interaction = self.interactions[name]
                if x > interaction.x and x < interaction.x + interaction.w and y > interaction.y and y < interaction.y + interaction.h:
                    interaction.activated = True           