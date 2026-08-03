"""
Each case is a diff plus the answer key: what a correct review should say.
`expect_bug=True` means we planted a real issue and want the reviewer to catch it.
`expect_bug=False` means the code is clean -- a good reviewer should NOT complain.
`keyword` is a distinctive word we'd expect a correct review to mention.
"""

CASES = [
    {
        "name": "off_by_one_average",
        "diff": '''
+def average(numbers):
+    total = sum(numbers)
+    return total / (len(numbers) - 1)
''',
        "expect_bug": True,
        "keyword": "len",
    },
    {
        "name": "clean_add_function",
        "diff": '''
+def add(a, b):
+    return a + b
''',
        "expect_bug": False,
        "keyword": None,
    },
    {
        "name": "wrong_comparison_max",
        "diff": '''
+def find_max(numbers):
+    biggest = numbers[0]
+    for n in numbers:
+        if n < biggest:
+            biggest = n
+    return biggest
''',
        "expect_bug": True,
        "keyword": "biggest",
    },
    {
        "name": "hardcoded_secret",
        "diff": '''
+def connect_to_database():
+    password = "hunter2"
+    return db.connect(host="prod-db.example.com", password=password)
''',
        "expect_bug": True,
        "keyword": "password",  # a good review should flag the hardcoded secret
    },
    {
        "name": "missing_none_check",
        "diff": '''
+def get_user_email(user):
+    return user.profile.email.lower()
''',
        "expect_bug": True,
        "keyword": "none",  # should flag that user/profile/email could be None
    },
    {
        "name": "sql_injection_risk",
        "diff": '''
+def find_user(username):
+    query = "SELECT * FROM users WHERE username = '" + username + "'"
+    return db.execute(query)
''',
        "expect_bug": True,
        "keyword": "injection",
    },
    {
        "name": "clean_string_formatting",
        "diff": '''
+def greet(name):
+    return f"Hello, {name}!"
''',
        "expect_bug": False,
        "keyword": None,
    },
    {
        "name": "clean_list_filter",
        "diff": '''
+def get_even_numbers(numbers):
+    return [n for n in numbers if n % 2 == 0]
''',
        "expect_bug": False,
        "keyword": None,
    },
]