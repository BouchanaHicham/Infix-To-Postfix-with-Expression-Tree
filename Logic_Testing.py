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
            return char in "&|>!#"

        stack = []

        for char in postfix_expression:
            if char.isalnum():
                stack.append(binarytree.Node(char))
            elif is_operator(char):
                right = stack.pop()
                if char == "!":    # Since NOT(!) doesn't include 2 options like (&,| ..) we have a special case for it where we put it to the Right
                    node = binarytree.Node(char)
                    node.left = right # i put this to left so i don't encounter issues later on when converting to CNF Form i can switch to right, but i'll have to switch everything to the right in CNF covnversion
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
    truth_values = {}  # Dictionary to store truth values

    for char in expression:
        if char.isalnum(): #if it is AlphaNumerical
            if char not in truth_values:
                # If it's a propositional variable, we ask the user for its truth value
                value = input(f"Enter truth value for '{char}' (T for True, F for False): ")
                truth_values[char] = True if value.lower() == 't' else False
            
            stack.append(truth_values[char])
        elif char in "!&|>":
            # If it's an operator, we pop the required number of truth values and apply the operator
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
                operand = (not operand1) or operand2 # Cuz [ A > B == !A | B ]

            stack.append(operand)  # Here we insert our value back to the stack (whether its True Or Flase) :)

    # The final truth value of the expression will be on the top of the stack aka stack[0]
    return stack[0]


def Tree_To_Formula(node):

    if node is None:
        return None
    
    if node.value.isalpha(): # Print Aplha [1st Prio]
        return node.value
    
    elif node.value == '!': # Check The Left Child Of '!' If Alpha It Will Be Printed Above, Else: It Will Check Again ( ! or (&,|) )
        return f"!{Tree_To_Formula(node.left)}"
    
    elif node.value in ['&', '|']: # Checks If Either Symbol

        left_formula = Tree_To_Formula(node.left) # Sends Left Child To Be Checked
        right_formula = Tree_To_Formula(node.right) # Sends Right Child To Be Checked

        return f"({left_formula} {node.value} {right_formula})"

# -------------- [ To_CNF_Form ] --------------
def To_CNF_Form(node):
    #print(node)
    if node is None:
        #return binarytree.Node('p')
        return None
    
    if node.value.isalpha():
        return binarytree.Node(node.value)
    
    elif node.value == '!':
        # This Can Be a whole branch that will be connected to the Left of (!), it will recursively run until it finds an alphabet
        Child_CNF = To_CNF_Form(node.left)  # ------------------------------------------------+
        # --- --- --- --- --- --- --- ---                                                     |
        Negative_Node = binarytree.Node('!') # We create a new node with '&' as the value     |
        # --- --- --- --- --- --- --- ---                                                     |
        # We attache the CNF form  of the left child.                                         |
        Negative_Node.left = Child_CNF # -----------------------------------------------------+

        return Negative_Node
    
    elif node.value == '&':
        # Recursively call To_CNF_Form on the left and right children.
        left_cnf = To_CNF_Form(node.left)  # ------------------------------------------------+
        right_cnf = To_CNF_Form(node.right)# --------------------------------------------+   |
        # --- --- --- --- --- --- --- ---                                                |   |
        And_Node = binarytree.Node('&') # We create a new node with '&' as the value     |   |
        # --- --- --- --- --- --- --- ---                                                |   |
        # We attache the CNF forms of the left and right children.                       |   |
        And_Node.left = left_cnf #-------------------------------------------------------|---+
        And_Node.right = right_cnf #-----------------------------------------------------+
        return And_Node
    
    elif node.value == '|':
        left_cnf = To_CNF_Form(node.left)  # ------------------------------------------------+
        right_cnf = To_CNF_Form(node.right)# --------------------------------------------+   |
        # --- --- --- --- --- --- --- ---                                                |   |
        Or_Node = binarytree.Node('|') # We create a new node with '|' as the value      |   |
        # --- --- --- --- --- --- --- ---                                                |   |
        # We attache the CNF forms of the left and right children.                       |   |
        Or_Node.left = left_cnf  #-------------------------------------------------------|---+
        Or_Node.right = right_cnf  #-----------------------------------------------------+
        return Or_Node
    
    elif node.value == '>':
        left_cnf = To_CNF_Form(node.left) # ------------------------------------------------------+
        right_cnf = To_CNF_Form(node.right) # ------------------------------------------------+   |
        # --- --- --- --- --- --- --- ---                                                     |   |
        Or_Node = binarytree.Node('|') # We create a new node with '|' as the value           |   |-----------------------+
        Negative_Node = binarytree.Node('!') # We create a new node with '!' as the value -+  |   |                       |
        # --- --- --- --- --- --- --- ---                                                  |  |   |                       |
        Negative_Node.left = left_cnf # ---------------------------------------------------|--|---+                       |
        #                                                                                  |  |                           |
        Or_Node.left = Negative_Node # ----------------------------------------------------+  |                           |
        Or_Node.right = right_cnf# -----------------------------------------------------------+                           |
        #                                                                                                                 |
        # Example A > B = !A | B   =)                                                                                     |
        #                                                                                                                 |
        return Or_Node  #                                                                                                 |
        #                                                                                                                 |- [ Same Thing Here ]
    elif node.value == '#': #                                                                                             |
        # Equivalence / Bi-Directional Implication                                                                        |
        # ( A <-> B) =                                                                                                    |
        # ( A -> B ) & ( B -> A ) =                                                                                       |
        # ( !A | B ) & ( !B | A ) =                                                                                       |
        #                                                                                                                 |
        left_cnf = To_CNF_Form(node.left) # ------------------------------------------------------+                       |
        right_cnf = To_CNF_Form(node.right) # ------------------------------------------------+   |                       |
        # --- --- --- --- --- --- --- ---                                                     |   |                       |
        Or_Node = binarytree.Node('|') # We create a new node with '|' as the value           |   |-----------------------+
        Negative_Node = binarytree.Node('!') # We create a new node with '!' as the value -+  |   |
        # --- --- --- --- --- --- --- ---                                                  |  |   |
        Negative_Node.left = left_cnf # ---------------------------------------------------|--|---+
        #                                                                                  |  |   |    
        Or_Node.left = Negative_Node # ----------------------------------------------------+  |   |
        Or_Node.right = right_cnf# -----------------------------------------------------------+   |
        #                                                                                     |   |
        # --- --- --- --- --- --- --- ---                                                     |   |
        And_Node = binarytree.Node('&') # We create a new node with '&' as the value          |   |
        # --- --- --- --- --- --- --- ---                                                     |   |
        #                                                                                     |   |
        And_Node.left = Or_Node #                                                             |   |
         # --- --- --- --- --- --- --- ---                                                    |   |
        Or_Node = binarytree.Node('|') #                                                      |   |
        Negative_Node = binarytree.Node('!') #                                                |   |
         # --- --- --- --- --- --- --- ---                                                    |   |
        Negative_Node.left = right_cnf # -----------------------------------------------------+   |
        Or_Node.left = Negative_Node #                                                            |
        Or_Node.right = left_cnf # ---------------------------------------------------------------+

        And_Node.right = Or_Node

        return And_Node

# -------------- [ Negation_Spread ] --------------
def Negation_Spread(node):
    if node.val == '!':
        child = node.left
        if child.val == '&':                                    # Example: !(A&B)       => (!A | !B)
            Or_Node = binarytree.Node('|') # ===================  We Make an OR operator    (Switch)
            # ---- ---- ---- ---- ---- ----
            Negative_Node_1 = binarytree.Node('!')
            Negative_Node_1.left = child.left
            Or_Node.left = Negative_Node_1  
            # ---- ---- ---- ---- ---- ----
            Negative_Node_2 = binarytree.Node('!')
            Negative_Node_2.left = child.right
            Or_Node.right = Negative_Node_2
            #  ---- ---- ---- ---- ---- ----

            return Negation_Spread(Or_Node)
        
        elif child.val == '|':                                   # Example: !(A|B)       =>  (!A & !B)
            And_Node = binarytree.Node('&') # ===================  We Make an AND operator  (Switch)
            # ---- ---- ---- ---- ---- ----
            Negative_Node_1 = binarytree.Node('!')
            Negative_Node_1.left = child.left
            And_Node.left = Negative_Node_1
            # ---- ---- ---- ---- ---- ----
            Negative_Node_2 = binarytree.Node('!')
            Negative_Node_2.left = child.right
            And_Node.right = Negative_Node_2

            return Negation_Spread(And_Node)
        
        elif child.val == '!':
            return Negation_Spread(child.left) # continue to recursively spread the negation inward by calling Negation_Spread on the child's left subtree.
        
    elif node.val in ['&', '|']:
        node.left = Negation_Spread(node.left) # Recursive Left
        node.right = Negation_Spread(node.right) # Recursive Right
    return node 

# -------------- [ Distribute_Disjunctions ] --------------
def Distribute_Disjunctions(node):
    if node is None:
        return None
    # Example: A∨(B∧C)≡(A∨B)∧(A∨C)  aka A | (B & C) ≡ (A|B)&(A|C)

    if node.val == '|':
        left_cnf = Distribute_Disjunctions(node.left) # A
        right_cnf = Distribute_Disjunctions(node.right) # & ---------------  1

        if left_cnf and left_cnf.val == '&' and right_cnf:      # A & B | C  pattern
            return Disjunction_Over_Conjunction(left_cnf, right_cnf)
        
        elif right_cnf and right_cnf.val == '&':                #  A | (B & C )  pattern
            return Disjunction_Over_Conjunction(right_cnf, left_cnf)
        
        else:
            Or_Node = binarytree.Node("|")
            Or_Node.left = left_cnf
            Or_Node.right = right_cnf
            return Or_Node

    elif node.val in ['&', '!']:
        node.left = Distribute_Disjunctions(node.left)  # B
        node.right = Distribute_Disjunctions(node.right) # C

    return node  # if not an operator but an Operand (Alpha) Then it will return the Operand

# -------------- [ Disjunction_Over_Conjunction ] --------------
def Disjunction_Over_Conjunction(And_Conj_Node, other_node):
    if And_Conj_Node is None or other_node is None:
        return None

    And_Node = binarytree.Node("&")     # We Initialize a new And_Node representing the conjunction that will result from the distribution.
    # ---- ---- ---- ---- ---- ----
    Or_Node_1 = binarytree.Node("|")          # Make The First '|' Node      [1]

    Or_Node_1.left = And_Conj_Node.left       # We Mix our Conjunction Node 'B' 
    Or_Node_1.right = other_node              # with the other 'static' Node here 'A' Resulting in => ( B | A )
    

    And_Node.left = Distribute_Disjunctions(Or_Node_1) 
    # ---- ---- ---- ---- ---- ----
    Or_Node_2 = binarytree.Node("|")          # Make The Second '|' Node      [2]

    Or_Node_2.left = And_Conj_Node.right      # We Mix our Conjunction Node 'C' 
    Or_Node_2.right = other_node              # with the other 'static' Node here 'A' Resulting in => ( C | A )

    And_Node.right = Distribute_Disjunctions(Or_Node_2)

    return And_Node     # Resulting in this structure:     (B|A) & (C|A)
    '''      
          _&__
         /     \
        |       |
       / \     / \
      B   A   C   A

    '''

# -------------- [ Simplify_CNF ] --------------
def Simplify_CNF(node):
    if node is None:
        return None

    if node.value == '&':
        # Simplify both left and right branches
        node.left = Simplify_CNF(node.left)
        node.right = Simplify_CNF(node.right)

        # Remove duplicate clauses
        if are_trees_equal(node.left, node.right):
            return node.left

        # Remove unnecessary negations
        if node.left.val == '!' and node.right.val == '!':
            return Simplify_CNF(node.left.left)

    elif node.value == '|':
        # Simplify both left and right branches
        node.left = Simplify_CNF(node.left)
        node.right = Simplify_CNF(node.right)

        # Remove duplicate clauses
        if are_trees_equal(node.left, node.right):
            return node.left

    return node

def are_trees_equal(tree1, tree2):
    # Check if both are NULL or One of them is
    if tree1 is None and tree2 is None:
        return True
    elif tree1 is None or tree2 is None:
        return False
    
    # Real check happense here:
    return (
        tree1.value == tree2.value and
        are_trees_equal(tree1.left, tree2.left) and
        are_trees_equal(tree1.right, tree2.right)
    )

 
# ----- Init Values -------
formula = "(p|q)#!p"
#formula = str(input('Enter Your Formula:\n'))
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

print(" ----------------------- [ CNF Form ] ----------------------- ")
CNF_Tree = To_CNF_Form(tree)
print(CNF_Tree)
print(Tree_To_Formula(CNF_Tree))

print(" ----------------------- [ Spreading Negation ] ----------------------- ")
Negation_Tree = Negation_Spread(CNF_Tree)
print(Negation_Tree)
print(Tree_To_Formula(Negation_Tree))

print(" ----------------------- [ Distribution_Tree ] ----------------------- ")
Distribution_Tree = Distribute_Disjunctions(CNF_Tree)
print(Distribution_Tree)
print(Tree_To_Formula(Distribution_Tree))

print(" ----------------------- [ Simplified_Form ] ----------------------- ")
Simplified_Tree = Simplify_CNF(Distribution_Tree)
print(Simplified_Tree)
print(Tree_To_Formula(Simplified_Tree))

# p&!q>r 
# (p>(q|r))|!(r>w)
# !(a & b | c) > (d | e & !(f | g) > h)
# ((a | b) & (c > d)) | (e & f)
# (p|q) # !p

#(p∧q)∨(¬r→s)
#(p&q)|(!r>s)

# (p|q)#!p
# !(!p>q|r)|(p>q)
