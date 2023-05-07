class Legacy:
    def __init__(self) -> None:
        self.encodedInstructions = []

    def addInstruction(self, pos, command, xyzScale=16) -> None:
        self.encodedInstructions.append(
            pos[2]+pos[1]*xyzScale+pos[0]*xyzScale**2+command*xyzScale**3)

    def getInstructions(self) -> list[int]:
        return self.encodedInstructions
