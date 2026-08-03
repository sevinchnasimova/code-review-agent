"""
Runs the agent on every case in eval_cases.py and reports how many it got right.
Run this with: python3 run_eval.py
"""

from agent import review_diff
from eval_cases import CASES
import time

correct = 0

for case in CASES:
    print(f"\n=== Case: {case['name']} ===")
    time.sleep(20)
    review = review_diff(case["diff"])

    if case["expect_bug"]:
        # Did the review mention the keyword we'd expect for a real catch?
        caught = case["keyword"].lower() in review.lower()
        print("Expected: bug should be caught")
        print("Result:  ", "CAUGHT" if caught else "MISSED")
        if caught:
            correct += 1

    else:
        # For clean code, a good review should NOT sound alarmed 
        # A rough check: it shouldn't use strong bug-words like "bug" or "error",
        false_alarm = any(word in review.lower() for word in ["bug", "error", "incorrect"])
        print("Expected: no bug (clean_code)")
        print("Result: ", "FALSE ALARM" if false_alarm else "CORRECTLY QUIET")
        if not false_alarm:
            correct += 1

print(f"\n=== SCORE: {correct}/{len(CASES)} ===")


