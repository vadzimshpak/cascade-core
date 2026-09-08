class Stack:
    def __init__(self):
        self.stack = [{}]

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        return self.stack.pop()

    def top(self):
        if len(self.stack) == 0:
            return None
        return self.stack[-1]

    def update(self, key, value):
        self.stack[-1].update({key: value})

    def raw(self):
        return self.stack

    def top_value(self, var_name):
        return self.top().get(var_name)

    def __repr__(self):
        return repr(self.stack)