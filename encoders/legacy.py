import numpy as np


class Legacy:
    def __init__(self) -> None:
        self.encodedInstructions = np.empty(0, int)

    def addInstruction(self, pos, command, xyzScale=16):
        self.encodedInstructions = np.append(
            self.encodedInstructions, pos[2]+pos[1]*xyzScale+pos[0]*xyzScale**2+command*xyzScale**3)

    def getInstructions(self):
        return self.encodedInstructions
