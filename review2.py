from google import genai

client = genai.Client()

with open("sample.py") as f:
    code = f.read()

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=f"Review this Python code for bugs:\n\n{code}",
)

print(response.text)