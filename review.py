from google import genai

client = genai.Client()

code = '''
def average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / (len(numbers) - 1)
'''

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=f"Review this Python code for bugs:\n\n{code}",
)

print(response.text)