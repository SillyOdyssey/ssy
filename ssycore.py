import sys
import re

class InlineCalcNode:
    def __init__(self, raw_label, math_expression):
        self.raw_label = raw_label          
        self.math_expression = math_expression  

class AssignNode:
    def __init__(self, name, expression, is_raw_val=False):
        self.name = name          
        self.expression = expression  
        self.is_raw_val = is_raw_val 

class PrintNode:
    def __init__(self, value, is_variable=False):
        self.value = value        
        self.is_variable = is_variable

class TableNode:
    def __init__(self, rows_data):
        self.rows_data = rows_data

class NativePythonNode:
    def __init__(self, target_command, argument=None, target_var=None):
        self.target_command = target_command  
        self.argument = argument              
        self.target_var = target_var          

class GuideNode:
    pass 

class RestartNode:
    pass 

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.should_exit = False

    def clear_terminal_screen(self):
        """Safely clears the Pydroid 3 screen using universal ANSI escape codes instead of os.system."""
        print("\033[H\033[J", end="")

    def prepare_expression(self, expr):
        var_patterns = re.findall(r'-[a-zA-Z0-9_]+', expr)
        for var_name in var_patterns:
            if var_name in self.variables:
                expr = expr.replace(var_name, str(self.variables[var_name]))
            else:
                raise NameError(f"SSY Runtime Error: Variable '{var_name}' is not defined.")
        return expr

    def clean_math_expression(self, expr):
        expr = expr.strip()
        if not re.match(r'^[0-9.+\-*/()\s]+$', expr):
            raise ValueError(f"Invalid characters in math expression: {expr}")
        return expr

    def print_guide(self):
        guide_text = """
========================================
             SSY COMMAND GUIDE          
========================================

1. STRINGS & PRINTING
   • "Hello World" -> Prints text inside quotes directly.
   • -result       -> Prints the value stored in variable '-result'.

2. CALCULATOR & MEMORY
   • (calc: 1+1)-result -> Evaluates math and outputs it with a label.
   • ?-result=(1+1)     -> Stores a math evaluation in a variable.
   • ?-final=(-result*2)-> Uses existing variables inside math formulas.

3. EXPERT TABLES
   • !row1"Name"=(Alex)!row2"ID"=(-id)
     Creates a clean, aligned console table layout block.

4. NATIVE PYTHON BRIDGES
   • PY:print("Text")   -> Uses Python to print.
   • PY:clear           -> Clears the terminal layout.
   • PY:break           -> Breaks out of execution instantly.
   • PY:input("P:")=var -> Pauses to accept player terminal keyboard text.

5. COMMENTS
   • <com# Note here > -> Completely ignored by the engine pipeline.

6. UTILITIES
   • ::guide            -> Shows this reference sheet.
   • ::restart          -> Wipes variable memory and clears the screen.
   • exit               -> Closes the active interactive shell.
========================================
"""
        print(guide_text)

    def lex_and_parse(self, code):
        code = re.sub(r'<com#[^>]*>', '', code)
        code = code.strip()
        
        if not code:
            return None

        # 1. SSY System Utilities
        if code == "::guide":
            return GuideNode()
        if code == "::restart":
            return RestartNode()

        # 2. Native Python Bridge Syntax: PY:
        if code.startswith("PY:"):
            py_instruction = code[3:].strip()
            
            # PY:print("...")
            print_match = re.match(r'^print\("([^"]*)"\)$', py_instruction)
            if print_match:
                return NativePythonNode("print", print_match.group(1))
                
            # PY:clear
            if py_instruction == "clear":
                return NativePythonNode("clear")
                
            # PY:break
            if py_instruction == "break":
                return NativePythonNode("break")

            # PY:input("...")=variable
            input_match = re.match(r'^input\("([^"]*)"\)\s*=\s*([a-zA-Z0-9_]+)$', py_instruction)
            if input_match:
                prompt_text = input_match.group(1)
                var_name = "-" + input_match.group(2)
                return NativePythonNode("input", prompt_text, var_name)
                
            raise SyntaxError(f"SSY Error: Python command not supported under PY: prefix -> {py_instruction}")

        # 3. Expert Table Syntax: !row1"Name"=(name)
        if code.startswith("!row"):
            row_segments = re.findall(r'(!row\d+)"([^"]*)"=\(([^)]*)\)', code)
            if row_segments:
                return TableNode(row_segments)

        # 4. Inline Calculator: (calc: 1+1)-result
        if code.startswith("(calc:"):
            inline_match = re.match(r'^\(calc:\s*([^)]+)\)(.*)$', code)
            if inline_match:
                return InlineCalcNode(code, inline_match.group(1))
            
        # 5. Math Calculator Assignment: ?-result=(1+1)
        calc_match = re.match(r'^\?-\s*([a-zA-Z0-9_]+)\s*=\s*\(([^)]+)\)$', code)
        if calc_match:
            return AssignNode("-" + calc_match.group(1), calc_match.group(2))

        # 6. Direct String: "value"
        string_match = re.match(r'^"([^"]*)"$', code)
        if string_match:
            return PrintNode(string_match.group(1), is_variable=False)
            
        # 7. Variable Print Reference: -result
        var_ref_match = re.match(r'^(-[a-zA-Z0-9_]+)$', code)
        if var_ref_match:
            return PrintNode(var_ref_match.group(1), is_variable=True)
            
        raise SyntaxError(f"SSY Error: Invalid syntax -> {code}")

    def execute(self, ast_node):
        if ast_node is None:
            return
            
        if isinstance(ast_node, GuideNode):
            self.print_guide()
        elif isinstance(ast_node, RestartNode):
            self.variables.clear() 
            self.clear_terminal_screen() # Safe ANSI clear call
            print("Welcome to SSY!") 

        elif isinstance(ast_node, NativePythonNode):
            if ast_node.target_command == "print":
                print(ast_node.argument)
            elif ast_node.target_command == "clear":
                self.clear_terminal_screen() # Safe ANSI clear call
            elif ast_node.target_command == "break":
                self.should_exit = True
            elif ast_node.target_command == "input":
                user_value = input(ast_node.argument)
                try:
                    if '.' in user_value:
                        self.variables[ast_node.target_var] = float(user_value)
                    else:
                        self.variables[ast_node.target_var] = int(user_value)
                except ValueError:
                    self.variables[ast_node.target_var] = user_value

        elif isinstance(ast_node, TableNode):
            headers = []
            cells = []
            for row_label, title, val in ast_node.rows_data:
                headers.append(title)
                cells.append(self.prepare_expression(val))
            header_line = " | ".join(f"{h:<12}" for h in headers)
            divider = "-" * len(header_line)
            content_line = " | ".join(f"{c:<12}" for c in cells)
            print(f"\n[SSY EXPERT TABLE]\n{divider}\n{header_line}\n{divider}\n{content_line}\n{divider}\n")

        elif isinstance(ast_node, InlineCalcNode):
            try:
                ready_expr = self.prepare_expression(ast_node.math_expression)
                print(f"{ast_node.raw_label}\n{eval(self.clean_math_expression(ready_expr))}")
            except Exception as e:
                print(f"SSY Math Error: {e}")

        elif isinstance(ast_node, AssignNode):
            try:
                ready_expr = self.prepare_expression(ast_node.expression)
                self.variables[ast_node.name] = eval(self.clean_math_expression(ready_expr))
            except Exception as e:
                print(f"SSY Math Error: {e}")
            
        elif isinstance(ast_node, PrintNode):
            if ast_node.is_variable:
                print(self.variables.get(ast_node.value, f"SSY Runtime Error: Variable '{ast_node.value}' is not defined."))
            else:
                print(ast_node.value)

def main():
    interpreter = Interpreter()
    if len(sys.argv) > 1:
        filename = sys.argv
        try:
            with open(filename, 'r') as file:
                for line_num, line in enumerate(file.readlines(), 1):
                    try:
                        ast = interpreter.lex_and_parse(line)
                        interpreter.execute(ast)
                        if interpreter.should_exit:
                            break
                    except SyntaxError as e:
                        print(f"Line {line_num}: {e}")
                        break
        except FileNotFoundError:
            print(f"Error: Could not find the file '{filename}'")
    else:
        print("Welcome to SSY!")
        while True:
            try:
                user_input = input("SSY > ")
                if user_input.strip() == "exit": 
                    break
                
                ast = interpreter.lex_and_parse(user_input)
                if ast is None and not user_input.strip().startswith("<com#") and user_input.strip() not in ["::guide", "::restart"]:
                    print("SSY Syntax Error: Code skipped! Please input an expression.")
                    continue
                
                interpreter.execute(ast)
                if interpreter.should_exit:
                    break
            except SyntaxError as e: 
                print(e)

if __name__ == "__main__":
    main()
        
