# Lab 5 — Static Code Analysis Reflection

### Q1. What is static code analysis, and why is it important?

Static code analysis is the process of examining source code without executing it to identify potential bugs, security vulnerabilities, and coding standard violations.

In this lab, Pylint, Bandit, and Flake8 were used to analyze `scholarship_system.py`. These tools helped improve code quality, security, readability, and maintainability.

### Q2. What issues were identified by the static analysis tools?

Pylint identified issues such as unused imports, missing docstrings, mutable default arguments, global statements, and naming convention violations.

Bandit detected two security-related issues: unsafe usage of `eval()` and silent exception handling using `except: pass`.

Flake8 identified 12 style violations, including missing blank lines, unused imports, and improper boolean comparisons.

### Q3. How were the identified issues fixed?

The unsafe `eval()` function was replaced with restricted AST-based arithmetic evaluation. Mutable default arguments were replaced with `None`, and specific exception handling was implemented.

File operations were improved using context managers and UTF-8 encoding. Input validation was added for GPA, credits, and income. Unused imports were removed, naming conventions were corrected, and docstrings were added.

### Q4. How did static analysis improve the final program?

Static analysis significantly improved the scholarship screening system.

| Tool | Before | After |
|---|---|---|
| Pylint | 4.69/10 | 10.00/10 |
| Bandit | 2 issues | 0 issues |
| Flake8 | 12 violations | 0 violations |

The final program successfully validates applicant information, rejects invalid inputs, and identifies eligible scholarship applicants.

The results demonstrate how static analysis helps produce more secure, reliable, readable, and maintainable software.