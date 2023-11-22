class NiknalVanillaV1Encoder:
    def __init__(self):
        self.encoded_instructions = []

    def addInstruction(self, pos, nozzle_offset, command):
        # 5 bits X, 5 bits Y (+1 bit nozzle offset toggle), 5 bits Z, 2 bits command
        x = pos[0]
        y = pos[1]
        z = pos[2]
        num = x*(2**13)+y*(2**8)+nozzle_offset*(2**7)+z*(2**2)+command
        binary = bin(num)[2:]
        binary = binary.zfill(18)
        self.encoded_instructions.append([int(i) for i in binary])

    def getInstructions(self) -> list[list[int]]:
        return self.encoded_instructions
