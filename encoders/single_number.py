class SingleNumber:
    def __init__(self) -> None:
        self.encoded_instructions = []
    def add_instruction(self, sequence):
        self.encoded_instructions.extend(sequence)
        self.encoded_instructions.append(-1)
    def get_instructions(self):
        return self.encoded_instructions+[-1]
    