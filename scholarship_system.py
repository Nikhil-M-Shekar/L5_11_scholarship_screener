
"""Scholarship screening system for evaluating student applications."""

import ast
import json
import operator

DEFAULT_FORMULA = "gpa * 10 + credits * 2"
CONFIG = {"merit_formula": DEFAULT_FORMULA}
INCOME_LIMIT = 800000
CUTOFF = 85

results = {}

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate_merit_score(gpa, credit_count):
    """Calculate merit score using a safely parsed arithmetic formula."""
    variables = {"gpa": gpa, "credits": credit_count}

    def evaluate(node):
        """Evaluate only permitted arithmetic syntax."""
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.Name) and node.id in variables:
            return variables[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](
                evaluate(node.left), evaluate(node.right)
            )
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](evaluate(node.operand))
        raise ValueError("Unsupported merit formula")

    try:
        tree = ast.parse(CONFIG["merit_formula"], mode="eval")
        return evaluate(tree)
    except (SyntaxError, ZeroDivisionError, OverflowError) as error:
        raise ValueError("Invalid merit formula") from error


def evaluate_applicant(student_id, test_scores, logs=None):
    """Validate an applicant and store their scholarship eligibility."""
    if logs is None:
        logs = []

    gpa = test_scores["gpa"]
    credit_count = test_scores.get("credits", 0)
    income = test_scores.get("income", 0)

    if not 0 <= gpa <= 10:
        raise ValueError("GPA must be between 0 and 10")
    if credit_count < 0:
        raise ValueError("Credits cannot be negative")
    if income < 0:
        raise ValueError("Income cannot be negative")

    score = calculate_merit_score(gpa, credit_count)
    eligible = score >= CUTOFF and income < INCOME_LIMIT

    results[student_id] = {"score": score, "eligible": eligible}
    logs.append(f"{student_id} scored {score}")
    return eligible


def change_formula(new_formula):
    """Validate and update the merit formula."""
    try:
        ast.parse(new_formula, mode="eval")
    except SyntaxError as error:
        raise ValueError("Invalid merit formula") from error

    CONFIG["merit_formula"] = new_formula


def persist_results(file="scholarships.json"):
    """Save screening results to a JSON file."""
    with open(file, "w", encoding="utf-8") as output:
        json.dump(results, output, indent=4)


def load_results(file="scholarships.json"):
    """Load previously saved screening results."""
    try:
        with open(file, "r", encoding="utf-8") as source:
            saved_results = json.load(source)

        if not isinstance(saved_results, dict):
            raise ValueError("Results file must contain a JSON object")

        results.clear()
        results.update(saved_results)

    except (OSError, json.JSONDecodeError) as error:
        print(f"Unable to load results: {error}")


def print_shortlist():
    """Display applicants who meet the scholarship requirements."""
    print("Shortlisted applicants:")
    for student_id, details in results.items():
        if details["eligible"]:
            print(f"  {student_id} score = {details['score']}")


def main():
    """Run the scholarship screening demonstration."""
    applicants = [
        ("U001", {"gpa": 9.1, "credits": 4, "income": 450000}),
        ("U002", {"gpa": 7.2, "credits": 1, "income": 300000}),
        ("U003", {"gpa": 12.5, "credits": -3, "income": -1}),
        ("U004", {"gpa": 6.5}),
    ]

    for student_id, scores in applicants:
        try:
            evaluate_applicant(student_id, scores)
        except (ValueError, KeyError, TypeError) as error:
            print(f"Rejected {student_id}: {error}")

    formula = input("Merit formula (Enter to keep default): ").strip()

    if formula:
        try:
            change_formula(formula)
        except ValueError as error:
            print(f"Unable to change formula: {error}")

    try:
        evaluate_applicant(
            "U005", {"gpa": 8.4, "credits": 3, "income": 600000}
        )
    except (ValueError, KeyError, TypeError) as error:
        print(f"Unable to evaluate U005: {error}")

    persist_results()
    load_results()
    print_shortlist()


if __name__ == "__main__":
    main()
