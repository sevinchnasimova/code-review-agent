from google import genai
from google.genai import types
import os
import time

client = genai.Client()

def read_file(path: str) -> str:
    """Read a file from the project and return its contents."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return f"ERROR: no file found at '{path}'. Try a different filename."

def list_files() -> str:
    """List all files in the current project folder."""
    return "\n".join(os.listdir("."))

def review_diff(diff: str) -> str:
    """Send a diff to the agent and return its final review as text."""
    conversation = [
        "You are a code reviewer. Review this diff. If you need to see "
        "another file to judge it correctly, use list_files then read_file. "
        "Do not read the same file twice. Stop and answer as soon as you "
        "have enough information.\n\n" + diff
    ]
    already_read = set()

    for turn in range(10):
        time.sleep(12)  # stay under the free tier's per-minute limit

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
            # --- the model wants to use a tool ---
            call = response.function_calls[0]
            print(f"[agent wants to: {call.name}]")

            if call.name == "read_file":
                path = call.args["path"]
                if path in already_read:
                    result = (f"You already read '{path}'. Use what "
                            f"you already have - do not request it again.")
                else:
                    result = read_file(path)
                    already_read.add(path)
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
            return response.text

    else:
        # --- ran out of turns without finishing ---
        print("[agent ran out of turns without finishing]")
        return "[agent ran out of turns without finishing]"


if __name__ == "__main__":
    diff = '''
+def normalize(value):
+   return clamp(value) / 100
'''
    print(review_diff(diff))
