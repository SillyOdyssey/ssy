# Pay attention that this is not the full ssycore.py. Download releases to get the full version.
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
