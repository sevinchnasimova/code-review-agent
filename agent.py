from google import genai
from google.genai import types

client = genai.Client()

def read_file(path: str) -> str:
    """Read a file from the project and return its contents."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return f"ERROR: no file found at '{path}'. Try a different filename."
    

import os

def list_files() -> str:
    """List all files in the current project folder."""
    return "\n".join(os.listdir("."))

diff = '''
+def normalize(value):
+    return clamp(value) / 100
'''

conversation = [
    "You are a code reviewer. The diff below calls functions defined in "
    "OTHER files. First use list_files to see what files exist, then use "
    "read_file tool to read the ones you actually need - do not read the "
    "same file more than once. As soon as you have enough information, "
    "stop calling tools and give your review.\n\n" + diff
]

for turn in range(10):

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=conversation,
        config=types.GenerateContentConfig(
            tools=[read_file, list_files],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        ),
    )

    if response.function_calls:
        # --- this is the "if" else's partner: the model wants a tool ---
        call = response.function_calls[0]
        print(f"[agent wants to read: {call.name}]")

        if call.name == "read_file":
            result = read_file(call.args["path"])
        else:
            result = list_files()

        conversation.append(response.candidates[0].content)
        conversation.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result},
                    )
                ],
            )
        )
        continue

    else:
        # --- the model answered directly: no more tool calls, done! ---
        print("\n--- FINAL REVIEW ---\n")
        print(response.text)
        break

else:
    # --- this is the FOR loop's else: only runs if we never hit `break` ---
    print("[agent ran out of turns without finishing]")