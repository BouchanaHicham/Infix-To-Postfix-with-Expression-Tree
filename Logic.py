import binarytree
# -------------------------------------------------- Infix To Post Fix --------------------------------------------------

def infix_to_postfix(expression): # Shunting Yard algorithm.
    precedence = {'!': 3, '&': 2, '|': 2, '>': 1, '#': 1}
    output = []
    stack = []

    def has_higher_precedence(op1, op2):
        return precedence[op1] <= precedence[op2]

    for token in expression:    
        # If Alphabet (Operand)
        if token.isalpha():
            output.append(token)
        # If Not Alphabet (Operator)
        elif token in "!&|>#":
            # If Stack is Not Empty and The Last Index in the Stack != '(' and The Last Index in the Stack has Higher Precedence than our Token
            while stack and stack[-1] != '(' and has_higher_precedence(token, stack[-1]):
                # Then Pop the last index in the stack and add it to our output to respect its precedence.
                output.append(stack.pop())  
            # if the Stack is empty or the precedence in the stack is respected, then just add our token (Operator) on top of it
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            # while the stack isn't empty and the last index in the stack isn't '(' which indicatesthat our job is done
            while stack and stack[-1] != '(':
                # pop the tokens inside the paranthesis from the stack and add them to our output
                output.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop() # This Removes the paranthesis
    
    # at the end we just add what is left from the stack to our output
    while stack:
        output.append(stack.pop())

    return ''.join(output)

# -------------------------------------------------- Build Tree --------------------------------------------------
# Quick Note: Here we Switch .
# We Used to Put The Operators(!&|>#) in The Stack and the Operands (abc) in the Output
# Now We Put The The Operands (abc) in The Stack and we work with Operators(!&|>#) to determine The Nodes Children

def build_expression_tree(postfix_expression):
        
        def is_operator(char):
            return char in "&|>!"

        stack = []

        for char in postfix_expression:
            if char.isalnum():
                stack.append(binarytree.Node(char))
            elif is_operator(char):
                right = stack.pop()
                if char == "!":    # Since NOT(!) doesn't include 2 options like (&,| ..) we have a special case for it where we put it to the Right
                    node = binarytree.Node(char)
                    node.right = right
                else:
                    left = stack.pop()
                    node = binarytree.Node(char)
                    node.left = left
                    node.right = right
                
                stack.append(node) #Then adds our Built up Branch to the stack

        if stack:
            return stack[0]
        else:
            return None

# -------------------------------------------------- Truth Or False --------------------------------------------------
def evaluate_expression(expression):
    stack = []

    for char in expression:
        if char.isalnum():
            # If it's a propositional variable, ask the user for its truth value
            value = input(f"Enter truth value for '{char}' (T for True, F for False): ")
            truth_value = True if value.lower() == 't' else False
            stack.append(truth_value)
        elif char in "!&|>":
            # If it's an operator, pop the required number of truth values and apply the operator
            if char == "!":
                operand = not stack.pop()
            elif char == "&":
                operand2 = stack.pop()
                operand1 = stack.pop()
                operand = operand1 and operand2
            elif char == "|":
                operand2 = stack.pop()
                operand1 = stack.pop()
                operand = operand1 or operand2
            elif char == ">":
                operand2 = stack.pop()
                operand1 = stack.pop()
                operand = (not operand1) or operand2
            stack.append(operand)

    # The final truth value of the expression will be on the top of the stack
    return stack[0]


# ----- Init Values -------
formula = "p&!q>r"
postfix_formula = infix_to_postfix(formula)
print("---------------------")
print("InFix: "+ formula )
print("---------------------")
print("PostFix: "+ postfix_formula )
print("---------------------")



# ----- Build Tree -------
tree = build_expression_tree(postfix_formula)
print(tree)
# ------------------------

result = evaluate_expression(postfix_formula)
print("Result: " + str(result))

#p&!q>r 
#(p>(q|r))|!(r>w)
#!(a & b | c) > (d | e & !(f | g) > h)
#((a | b) & (c > d)) | (e & f)