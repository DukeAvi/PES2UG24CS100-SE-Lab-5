# Lab 5: Static Analysis Issues in `online_exam.py`

## 1. Major Issues Identified and Fixed

| No. | Issue | Fix Implemented |
|---|---|---|
| 1 | **OS command injection:** `os.system()` used string concatenation to execute SSH commands, creating a security risk. | Replaced it with `subprocess.run()` using a list of arguments and no shell. |
| 2 | **Weak hashing algorithm:** MD5 was used to compare exam answers. | Replaced MD5 with SHA-256. |
| 3 | **Mutable default argument:** The default `penalties={}` could retain data across function calls. | Changed the default to `None` and initialized a new dictionary when required. |
| 4 | **Hard-coded password and predictable randomness:** The proctor password was stored in the source code, and `random.choice()` selected bonus questions. | Read the password from an environment variable and replaced `random.choice()` with `secrets.choice()`. |
| 5 | **Insufficient error handling:** `topper()` failed when no results were available, and `main()` executed whenever the module was imported. | Added an empty-results check and guarded execution with `if __name__ == "__main__":`. |

## 2. Other Improvements

- Renamed functions and variables to follow PEP 8 naming conventions.
- Added module and function docstrings.
- Improved loop structure using `enumerate()` and simplified conditional statements.
- Corrected formatting issues reported by Flake8.

## 3. Verification

All tools were run using the project virtual environment to avoid modifying the system Python installation.

| Tool | Original Result | Final Result |
|---|---|---|
| Pylint | 5.65/10 | 10.00/10 |
| Bandit | 2 High, 0 Medium, 2 Low | 0 High, 0 Medium, 1 Low |
| Flake8 | 4 warnings | No warnings |

The remaining Bandit warning concerns the import of `subprocess` and is informational. The program was executed before and after the changes, and its expected output remained unchanged apart from the randomly selected bonus question.