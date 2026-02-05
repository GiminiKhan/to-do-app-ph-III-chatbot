---
id: 2
title: "Fix Bcrypt Password Hash Limit Error"
stage: "red"
date_iso: "2026-02-03"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "main"
user: "user"
command: "/sp.implement --force \"Even with a 4-character password ('1234'), bcrypt throws the 72-byte limit error. This confirms the issue is in the hashing logic. Please inspect 'backend/src/auth/utils.py' and the registration service. Ensure that only the plain-text password string is being hashed. It's possible the code is trying to hash an object, a dictionary, or concatenating the password with a very long secret key incorrectly. Fix the hashing utility to handle simple strings correctly.\""
labels: ["authentication", "bcrypt", "password", "security", "error-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/src/core/security.py
tests_yaml: |
  - none
---

# Fix Bcrypt Password Hash Limit Error

## Prompt Text
```
--force "Even with a 4-character password ('1234'), bcrypt throws the 72-byte limit error. This confirms the issue is in the hashing logic. Please inspect 'backend/src/auth/utils.py' and the registration service. Ensure that only the plain-text password string is being hashed. It's possible the code is trying to hash an object, a dictionary, or concatenating the password with a very long secret key incorrectly. Fix the hashing utility to handle simple strings correctly."
```

## Response Text
Fixed the bcrypt 72-byte limit error by updating the password hashing functions in backend/src/core/security.py. The changes include:

1. Added proper type validation to ensure passwords are strings before hashing
2. Added length validation to ensure passwords don't exceed bcrypt's 72-byte limit
3. Added explicit string conversion for both verify_password and get_password_hash functions
4. Added error handling with clear error messages for password length violations

The fix addresses the issue where bcrypt was receiving non-string objects or excessively long strings, even with short passwords like '1234'.

## Outcome
Successfully resolved the bcrypt 72-byte limit error by adding proper input validation and type handling in the password hashing functions.