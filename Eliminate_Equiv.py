def eliminate_equivalence(expression):
    result = ""
    removable = ""
    i = 0
    numberof_Hash = expression.count('#')

   

    while i < len(expression):
        if expression[i]!='#' :
            removable += expression[i]

        if expression[i] == "(" and i + 1 < len(expression) and (expression[i + 1].isalpha() or expression[i + 1] == '!' ):
            # Extract the propositional variables inside parentheses
            j = i + 1
            while j < len(expression) and (expression[j].isalpha() or expression[j] == '!'):
                j += 1

            p = expression[i + 1:j]
            
            # Check for the equivalence operator
            if j < len(expression) and expression[j] == "#" and j + 1 < len(expression) and ( expression[j + 1].isalpha() or expression[j + 1] == '!') :
                k = j + 1
                while k < len(expression) and expression[k].isalpha():
                    k += 1

                q = expression[j + 1:k]

                # Replace the equivalence with the equivalent expression
                result += f"({p}>{q})&({q}>{p})"
                i = k
                continue

        elif expression[i] == "#" and i + 1 < len(expression) and ( expression[i + 1].isalpha() or expression[i + 1] == '!'):
            # If # is not preceded by (, consider everything from the matching ( to the current position
            j = i + 1
            while j < len(expression) and (expression[j].isalpha() or expression[i + 1] == '!'):
                j += 1

            q = expression[i + 1:j]

            # Find the matching opening parenthesis (
            count = 1
            k = i - 1
            while k >= 0 and count > 0:
                if expression[k] == ")":
                    count += 1
                elif expression[k] == "(":
                    count -= 1
                k -= 1

            p = expression[k + 1:i]

            # Replace the equivalence with the equivalent expression
            result += f"({p}>{q})&({q}>{p})"
            i = j
            continue

        result += expression[i]
        i += 1
    print("removable",removable)
    return result[len(removable):]        # This Means that i remove the removable extra Letters that come up in the beginning of the String

# Example usage:
formula_with_equivalence = "(p&q)#!q"
formula_without_equivalence = eliminate_equivalence(formula_with_equivalence)


print("Original Formula:", formula_with_equivalence)
print("Formula without Equivalence:", formula_without_equivalence)

# Example usage:
formula_with_equivalence = "A#!q"
formula_without_equivalence = eliminate_equivalence(formula_with_equivalence)

print("Original Formula:", formula_with_equivalence)
print("Formula without Equivalence:", formula_without_equivalence)

'''
# Example usage:
formula_with_equivalence = "(p#q)#!q"
formula_without_equivalence = eliminate_equivalence(formula_with_equivalence)
formula_without_equivalence = eliminate_equivalence(formula_without_equivalence)

print("Original Formula:", formula_with_equivalence)
print("Formula without Equivalence:", formula_without_equivalence)

'''