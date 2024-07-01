class MultiPanelCommand:
    def __init__(self) -> None:
        self.panels = {
            '0': [],
            '1': [],
            '2': [],
            '3': [],
        }

    def add_instruction(self, x, y, z, command):
        self.panels['0'].append(x)
        self.panels['1'].append(y)
        self.panels['2'].append(z)
        self.panels['3'].append(command)

    def get_instructions(self):
        return self.panels
