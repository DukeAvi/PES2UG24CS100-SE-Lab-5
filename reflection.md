## 1. Which issues were the easiest to fix, and which were the hardest? Why?

Ans: Formatting violations and naming issues were the easiest to fix, as the tools provided clear guidance. Security vulnerabilities involving shell injection and weak hashing were the hardest, as they required understanding the underlying risks and implementing appropriate fixes.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Ans: Bandit reported a low-severity warning for importing `subprocess`, despite its safe use with argument lists and without a shell. This informational warning was retained, as the implementation addressed the actual security risk.

## 3. How would you integrate static analysis tools into your actual software development workflow?

Ans: I would integrate Pylint, Bandit, and Flake8 into development using a virtual environment, editor feedback, pre-commit hooks, and CI pipelines. Automated checks would be complemented by testing and manual review to identify issues beyond static analysis.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

Ans: Pylint improved from 5.65/10 to 10/10, Flake8 reported zero warnings, and Bandit reported no high- or medium-severity issues. The fixes improved readability, eliminated identified security vulnerabilities, strengthened edge-case handling, and preserved the program's expected behaviour.