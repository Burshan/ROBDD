"""
ROBDD Implementation
Author: Omer Burshan
For Formal Verification and Synthesis - Assignment 3
"""

import urllib.parse
import urllib.request


class Node:
    """Represents a single node in the Binary Decision Diagram"""
    def __init__(self, identifier, variable, left_child, right_child):
        self.id = identifier
        self.variable = variable
        self.left = left_child   # False branch
        self.right = right_child  # True branch

    def is_leaf(self):
        return self.left is None and self.right is None

    def __repr__(self):
        if self.is_leaf():
            return f"Node({self.id}: {self.variable})"
        return f"Node({self.id}: {self.variable}, L={self.left.id}, R={self.right.id})"


class ROBDD:
    """Reduced Ordered Binary Decision Diagram implementation"""

    def __init__(self):
        # Hash table for ensuring uniqueness: (variable, left_id, right_id) -> Node
        self.node_cache = {}
        self.next_id = 2

        # Create terminal nodes for False (0) and True (1)
        self.false_node = Node(0, '0', None, None)
        self.true_node = Node(1, '1', None, None)
        self.root = None

    def create_or_find_node(self, variable, left_child, right_child):
        """
        Creates a new node or returns existing one, applying reduction rules:
        - Eliminates redundant nodes where both children are the same
        - Ensures structural uniqueness through hash table lookup
        """
        # Apply redundancy elimination rule
        if left_child == right_child:
            return left_child

        # Check if an identical node already exists
        lookup_key = (variable, left_child.id, right_child.id)

        if lookup_key in self.node_cache:
            return self.node_cache[lookup_key]

        # Create and register new node
        fresh_node = Node(self.next_id, variable, left_child, right_child)
        self.node_cache[lookup_key] = fresh_node
        self.next_id += 1
        return fresh_node

    def eval_formula(self, formula_str, var_assignment):
        """Evaluates a boolean formula string with given variable values"""
        # Convert formula syntax to Python-compatible format
        python_expr = formula_str.replace("xor", "^")
        python_expr = python_expr.replace("->", "<=")
        python_expr = python_expr.replace("<->", "==")
        python_expr = python_expr.replace("!", " not ")

        try:
            return eval(python_expr, {}, var_assignment)
        except Exception as err:
            print(f"Formula evaluation error: {err}")
            return False

    def construct_bdd(self, formula, var_order, depth=0, var_values=None):
        """
        Recursively constructs the BDD using Shannon decomposition:
        For any boolean function f and variable x: f = (¬x ∧ f|x=0) ∨ (x ∧ f|x=1)
        """
        if var_values is None:
            var_values = {}

        # Terminal case: all variables assigned, evaluate the formula
        if depth == len(var_order):
            if isinstance(formula, str):
                outcome = self.eval_formula(formula, var_values)
            else:
                outcome = formula(var_values)
            return self.true_node if outcome else self.false_node

        # Get current variable from ordering
        current_variable = var_order[depth]

        # Compute left subtree (variable = False)
        left_assignment = var_values.copy()
        left_assignment[current_variable] = False
        left_subtree = self.construct_bdd(formula, var_order, depth + 1, left_assignment)

        # Compute right subtree (variable = True)
        right_assignment = var_values.copy()
        right_assignment[current_variable] = True
        right_subtree = self.construct_bdd(formula, var_order, depth + 1, right_assignment)

        # Build node with reduction rules applied
        result_node = self.create_or_find_node(current_variable, left_subtree, right_subtree)

        # Store root reference at top level
        if depth == 0:
            self.root = result_node

        return result_node

    def export_to_dot(self, start_node=None):
        """Generates DOT format string for visualization"""
        if start_node is None:
            start_node = self.root

        output = ["digraph ROBDD {"]

        # Terminal nodes with color coding
        output.append('  0 [shape=box, label="0", style=filled, fillcolor="#AB1111", color="#AB1111"];')
        output.append('  1 [shape=box, label="1", style=filled, fillcolor="#67A15B", color="#67A15B"];')

        seen = set()
        to_visit = [start_node]

        while to_visit:
            current = to_visit.pop()
            if current.id in seen or current.id in [0, 1]:
                continue

            seen.add(current.id)
            output.append(f'  {current.id} [label="{current.variable}"];')

            # False edge (dashed, red)
            output.append(f'  {current.id} -> {current.left.id} [style=dashed, color="#AB1111", fontcolor="#AB1111", label="0"];')

            # True edge (solid, green)
            output.append(f'  {current.id} -> {current.right.id} [style=solid, color="#67A15B", fontcolor="#67A15B", label="1"];')

            to_visit.append(current.left)
            to_visit.append(current.right)

        output.append("}")
        return "\n".join(output)

    def render_to_file(self, filepath="output.dot", start_node=None):
        """Saves the BDD as a DOT file"""
        if start_node is None:
            start_node = self.root

        dot_content = self.export_to_dot(start_node)
        with open(filepath, 'w') as file:
            file.write(dot_content)
        print(f"  DOT file written: {filepath}")

    def render_to_image(self, filepath="output.png", start_node=None):
        """Uses QuickChart API to generate PNG image from DOT specification"""
        if start_node is None:
            start_node = self.root

        dot_spec = self.export_to_dot(start_node)

        api_endpoint = "https://quickchart.io/graphviz"
        query_params = {
            'graph': dot_spec,
            'format': 'png'
        }

        request_url = f"{api_endpoint}?{urllib.parse.urlencode(query_params)}"

        try:
            http_request = urllib.request.Request(
                request_url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(http_request) as response, open(filepath, 'wb') as file:
                file.write(response.read())
            print(f"  PNG image saved: {filepath}")

        except Exception as err:
            print(f"  Image generation failed: {err}")

    def node_count(self):
        """Returns total number of nodes in the BDD"""
        if not self.root:
            return 0

        counted = set()
        pending = [self.root]

        while pending:
            current = pending.pop()
            if current.id in counted:
                continue
            counted.add(current.id)

            if current.left is not None:
                pending.append(current.left)
            if current.right is not None:
                pending.append(current.right)

        return len(counted)
