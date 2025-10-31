class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0

def evaluate_expression(expression):
    # Remove any whitespace from the expression
    expression = expression.replace(" ", "")
    
    # Stack for numbers
    values = Stack()
    # Stack for operators
    ops = Stack()
    
    i = 0
    while i < len(expression):
        # If current character is a number, push it to values stack
        if expression[i].isdigit():
            num = 0
            while i < len(expression) and expression[i].isdigit():
                num = num * 10 + int(expression[i])
                i += 1
            values.push(num)
            continue
        
        # If current character is '(', push it to ops stack
        elif expression[i] == '(':
            ops.push(expression[i])
        
        # If current character is ')', solve the entire bracket
        elif expression[i] == ')':
            while not ops.is_empty() and ops.peek() != '(':
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.push(apply_op(val1, val2, op))
            
            # Pop the opening bracket
            ops.pop()
        
        # If current character is an operator
        else:
            # While top of ops has same or greater precedence to current operator
            while (not ops.is_empty() and 
                   precedence(ops.peek()) >= precedence(expression[i])):
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.push(apply_op(val1, val2, op))
            
            # Push current operator to ops stack
            ops.push(expression[i])
        
        i += 1
    
    # Apply remaining operators to remaining values
    while not ops.is_empty():
        val2 = values.pop()
        val1 = values.pop()
        op = ops.pop()
        values.push(apply_op(val1, val2, op))
    
    # Top of values contains result
    return values.pop()

def precedence(op):
    if op in ['+', '-']:
        return 1
    if op in ['*', '/']:
        return 2
    return 0

def apply_op(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a // b  # Using integer division as per requirements

def main():
    # Read input file
    with open('input.txt', 'r') as file:
        expressions = file.read().splitlines()
    
    # Evaluate each expression and store results
    results = []
    for expr in expressions:
        if expr.strip():  # Skip empty lines
            try:
                result = evaluate_expression(expr)
                results.append(f"{expr} = {result}")
            except Exception as e:
                results.append(f"Error evaluating '{expr}': {str(e)}")
    
    # Write results to output file
    with open('output.txt', 'w') as file:
        file.write("\n".join(results))

if __name__ == "__main__":
    main()
