"""
Main script to build ROBDDs for Assignment 3 formulas
Author: Omer Burshan
"""

from robdd import ROBDD

if __name__ == "__main__":
    # --- Task A ---
    # Formula: (a ∧ ¬c) ∨ (b ⊕ d)
    print("=" * 70)
    print("Building ROBDD for Formula A: (a ∧ ¬c) ∨ (b ⊕ d)")
    print("=" * 70)
    expr_a = "(a and not c) or (b ^ d)"
    bdd_a = ROBDD()
    bdd_a.construct_bdd(expr_a, ['a', 'c', 'b', 'd'])
    print(f"Number of nodes: {bdd_a.node_count()}")
    bdd_a.render_to_file("task_a.dot")
    bdd_a.render_to_image("task_a.png")
    print()

    # --- Task B ---
    # Formula: Returns 1 iff the number of 1's in {x1, x2, x3, x4, x5} is ≥ 3
    print("=" * 70)
    print("Building ROBDD for Formula B: |{x1, x2, x3, x4, x5}| >= 3")
    print("=" * 70)
    expr_b = "(x1 and x2 and x3) or (x1 and x2 and x4) or (x1 and x2 and x5) or (x1 and x3 and x4) or (x1 and x3 and x5) or (x1 and x4 and x5) or (x2 and x3 and x4) or (x2 and x3 and x5) or (x2 and x4 and x5) or (x3 and x4 and x5)"

    bdd_b = ROBDD()
    bdd_b.construct_bdd(expr_b, ['x1', 'x2', 'x3', 'x4', 'x5'])
    print(f"Number of nodes: {bdd_b.node_count()}")
    bdd_b.render_to_file("task_b.dot")
    bdd_b.render_to_image("task_b.png")
    print()

    # --- Task C ---
    # Formula: x > y (3-bit comparison)
    print("=" * 70)
    print("Building ROBDD for Formula C: x > y (3-bit comparison)")
    print("=" * 70)
    expr_c = "(x3 and not y3) or ((not (x3 ^ y3)) and (x2 and not y2)) or ((not (x3 ^ y3)) and (not (x2 ^ y2)) and (x1 and not y1))"

    bdd_c = ROBDD()
    bdd_c.construct_bdd(expr_c, ['x3', 'y3', 'x2', 'y2', 'x1', 'y1'])
    print(f"Number of nodes: {bdd_c.node_count()}")
    bdd_c.render_to_file("task_c.dot")
    bdd_c.render_to_image("task_c.png")
    print()

    # --- Additional Formula ---
    # Formula: a ⊕ b ⊕ c ⊕ d ⊕ e (XOR of all variables)
    print("=" * 70)
    print("Building ROBDD for Additional Formula: a ⊕ b ⊕ c ⊕ d ⊕ e")
    print("=" * 70)
    expr_d = "a ^ b ^ c ^ d ^ e"

    bdd_d = ROBDD()
    bdd_d.construct_bdd(expr_d, ['a', 'c', 'b', 'd', 'e'])
    print(f"Number of nodes: {bdd_d.node_count()}")
    bdd_d.render_to_file("task_d.dot")
    bdd_d.render_to_image("task_d.png")
    print()

    print("=" * 70)
    print("All ROBDDs generated and saved!")
    print("DOT files can be visualized at: https://dreampuf.github.io/GraphvizOnline/")
    print("=" * 70)
