# Lab 5 — Static Code Analysis

## 1. Objective

To identify and fix code quality, security, and style issues in `scholarship_system.py` using Pylint, Bandit, and Flake8.

## 2. Initial Static Analysis Results

The original Python program was analyzed using all three tools before making modifications.

| Tool | Initial Result |
|---|---|
| Pylint | 4.69/10 |
| Bandit | 2 security issues |
| Flake8 | 12 style violations |

## 3. Identified Issues and Fixes

The following issues were identified in the original program. Line numbers refer to the original source code.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe eval() | Security | 12 | Using `eval()` can execute potentially malicious Python expressions. | Replaced with restricted AST-based arithmetic evaluation. |
| Mutable default argument | Bug | 14 | Using `logs=[]` can cause the same list to be shared between function calls. | Changed the default argument to `None` and initialized a new list inside the function. |
| Bare exception handling | Reliability | 37–38 | Using `except: pass` silently ignores errors, making debugging difficult. | Replaced with specific exception handling and meaningful error messages. |
| Improper file handling | Reliability | 29, 36 | Files were opened without context managers or explicit encoding. | Used `with open()` and specified UTF-8 encoding. |
| Unused imports | Style | 2–3 | The `math` and `sys` modules were imported but never used. | Removed unused imports. |
| Missing docstrings | Documentation | 1, 11, 14, 24, 28, 33, 40, 46 | The module and several functions lacked documentation. | Added module-level and function-level docstrings. |
| Naming convention violation | Style | 40 | The function `printShortlist()` did not follow Python snake_case naming conventions. | Renamed it to `print_shortlist()`. |
| Unnecessary boolean comparison | Style | 43 | The condition compared a boolean value using `== True`. | Replaced it with a direct boolean condition. |
| Old-style string formatting | Style | 21 | String formatting used the `%` operator instead of modern f-strings. | Replaced with f-string formatting. |
| Global variable usage | Maintainability | 25, 34 | Functions used global statements to modify application state. | Removed global statements and used a configuration dictionary and in-place result updates. |
| Redefining built-in name | Style | 11, 16 | The variable name `credits` conflicted with a Python built-in. | Renamed the local variable and parameter to `credit_count`. |
| Missing input validation | Logic | 46–53 | The program accepted invalid GPA, negative credits, and negative income values. | Added validation checks and error handling for invalid applicant data. |
| Missing blank lines | Style | Multiple | Functions were not separated according to PEP 8 conventions. | Added appropriate blank lines between function definitions. |

## 4. Changes Implemented

The following improvements were made to `scholarship_system.py`:

1. Removed unsafe `eval()` usage and implemented restricted arithmetic expression evaluation using Python's `ast` module.
2. Replaced mutable default arguments with `None`.
3. Implemented specific exception handling instead of bare `except` blocks.
4. Improved file handling using context managers and UTF-8 encoding.
5. Added validation for GPA, credits, and income.
6. Removed unused imports and corrected naming conventions.
7. Added docstrings to improve code readability and maintainability.
8. Replaced old-style string formatting with f-strings.
9. Removed global statements and improved application state management.
10. Corrected formatting issues identified by Flake8.

## 5. Final Static Analysis Results

After implementing the fixes, all three tools were executed again.

| Tool | Before Refactoring | After Refactoring |
|---|---|---|
| Pylint | 4.69/10 | 10.00/10 |
| Bandit | 2 issues | 0 issues |
| Flake8 | 12 violations | 0 violations |

All reported issues were resolved in the final analysis.

## 6. Functional Testing

The updated program was executed successfully using the default merit formula.

The program correctly rejected applicant U003 because the GPA exceeded the valid range of 0 to 10.

The shortlisted applicants were:

- U001 — Merit Score: 99.0
- U005 — Merit Score: 90.0

Applicants U002 and U004 did not meet the minimum merit score requirement.

## 7. Conclusion

Static code analysis helped identify and resolve security vulnerabilities, programming errors, and style violations in the scholarship screening system.

The Pylint score improved from 4.69/10 to 10.00/10, while Bandit and Flake8 reported zero remaining issues.

The refactored program is more secure, readable, reliable, and maintainable. All identified static analysis issues were successfully addressed.