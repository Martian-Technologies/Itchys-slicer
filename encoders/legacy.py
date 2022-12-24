import numpy as np


class Legacy:
    def __init__(self) -> None:
        self.encodedInstructions = np.empty(0, int)


    def addInstruction(self, pos, command, xyzScail = 16):
        self.encodedInstructions = np.append(self.encodedInstructions,
            pos[0]+
            pos[1]*xyzScail+
            pos[2]*xyzScail**2+
            command*xyzScail**3
        )
    
    def getInstructions(self):
        return self.encodedInstructions