class ShuntingYard:
    """Class to convert an infix regex expression into postfix notation using the Shunting Yard algorithm."""

    def __init__(self, regex):
        self.regex = regex
        self.operators = {'*': 3, '.': 2, '|': 1}  
        self.output = []
        self.stack = []

    def is_operator(self, char):
        """Check if the character is an operator."""
        return char in self.operators

    def precedence(self, op):
        """Get precedence of an operator."""
        return self.operators.get(op, 0)

    def to_postfix(self):
        """Convert infix regex to postfix notation."""
        for char in self.regex:
            if char.isalnum():  
                self.output.append(char)
            elif self.is_operator(char):
                while (self.stack and self.stack[-1] != '(' and
                       self.precedence(self.stack[-1]) >= self.precedence(char)):
                    self.output.append(self.stack.pop())
                self.stack.append(char)
            elif char == '(':
                self.stack.append(char)
            elif char == ')':
                while self.stack and self.stack[-1] != '(':
                    self.output.append(self.stack.pop())
                self.stack.pop()  

        while self.stack:
            self.output.append(self.stack.pop())

        return ''.join(self.output)
