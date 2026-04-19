class Gate:
    def __init__(self, name):
        self.name = name

    def compute(self, inputs):
        raise NotImplementedError("Subclasses must implement compute method")

class AndGate(Gate):
    def __init__(self):
        super().__init__("AND")

    def compute(self, inputs):
        # AND: 1 se todas entradas forem 1
        return all(inputs)

class OrGate(Gate):
    def __init__(self):
        super().__init__("OR")

    def compute(self, inputs):
        # OR: 1 se pelo menos uma entrada for 1
        return any(inputs)

class NotGate(Gate):
    def __init__(self):
        super().__init__("NOT")

    def compute(self, inputs):
        # NOT: inverte a entrada (assume uma entrada)
        if len(inputs) != 1:
            raise ValueError("NOT gate requires exactly one input")
        return not inputs[0]

class XorGate(Gate):
    def __init__(self):
        super().__init__("XOR")

    def compute(self, inputs):
        # XOR: 1 se entradas forem diferentes
        if len(inputs) != 2:
            raise ValueError("XOR gate requires exactly two inputs")
        return inputs[0] != inputs[1]

class NandGate(Gate):
    def __init__(self):
        super().__init__("NAND")

    def compute(self, inputs):
        # NAND: NOT de AND
        return not all(inputs)

class NorGate(Gate):
    def __init__(self):
        super().__init__("NOR")

    def compute(self, inputs):
        # NOR: NOT de OR
        return not any(inputs)