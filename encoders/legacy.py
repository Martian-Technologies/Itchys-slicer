import numpy as np


class Legacy:
    def __init__(self) -> None:
        self.encodedInstructions = np.empty(0, int)


    def addInstruction(self, pos, command, xyzScale = 16):
        self.encodedInstructions = np.append(self.encodedInstructions,
            pos[0]+
<<<<<<< HEAD
            pos[1]*xyzScail+
            pos[2]*xyzScail**2+
            command**3
=======
            pos[1]*xyzScale+
            pos[2]*xyzScale**2+
            command*xyzScale**3
>>>>>>> 08975fe7389805c0ef2cf0129d22b405a74e0f5a
        )
    
    def getInstructions(self):
        return self.encodedInstructions