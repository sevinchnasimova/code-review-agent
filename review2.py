import subprocess
from google import genai

client = genai.Client()

diff = subprocess.run(
    ["git", "diff"],
    capture_output=True,
    text=True,
).stdout

if not diff.strip():
    print("No changes to review.")
    exit()

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=f"Review this Python code for bugs:\n\n{diff}",
)

print(response.text)