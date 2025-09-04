import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def main():
    api_key = os.getenv("GEMINI_API_KEY")

    response = completion(
        model="google/gemini-2.5-flash-image-preview:free",
        messages=[
            {
                "role": "user",
                "context": "Who is the founder of Pakistan?"
            }
        ],
    )

    print(response['choices'][0]['message']['content'])

if __name__ == "__main__":
    main()
