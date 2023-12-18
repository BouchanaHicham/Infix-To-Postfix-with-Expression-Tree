def eliminate_implication(expression):
    result = ""
    i = 0

    while i < len(expression):
        if expression[i] == "(" and i + 1 < len(expression) and expression[i + 1].isalpha():
            # Extract the propositional variables inside parentheses
            j = i + 1
            while j < len(expression) and expression[j].isalpha():
                j += 1

            p = expression[i + 1:j]

            # Check for the implication operator
            if j < len(expression) and expression[j] == ">" and j + 1 < len(expression) and expression[j + 1].isalpha():
                k = j + 1
                while k < len(expression) and expression[k].isalpha():
                    k += 1

                q = expression[j + 1:k]

                # Replace the implication with the equivalent expression
                result += f"(!{p}|{q})"
                i = k
                continue

        result += expression[i]
        i += 1

    return result

# Example usage:
formula_with_implication = "(p&q) > p"
formula_without_implication = eliminate_implication(formula_with_implication)

print("Original Formula:", formula_with_implication)
print("Formula without Implication:", formula_without_implication)
