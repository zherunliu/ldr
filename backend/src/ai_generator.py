import os
import json
from openai import OpenAI
from typing import Dict, Any

"""for test"""
# from dotenv import load_dotenv
# load_dotenv()

client = OpenAI(
    api_key=os.getenv("ALIYUN_API_KEY"),
    base_url=os.getenv("ALIYUN_BASE_URL"),
)


def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    system_prompt = """
    You are a programming expert.
    Proficient in C++, Python, JavaScript, and TypeScript.
    Proficient in Node.js, React, Vue3, and the Express development framework.

    Your task is to generate a programming problem with a difficulty ranges from easy, medium, to hard.
    The problem has four options, with only one correct answer.
    The problem is formatted as JSON. Example:
    {
        "title": "Problem description",
        "difficulty": "Difficulty level of the problem, ranges from easy, medium, to hard",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "correct_answer_id": 1, // Index of the correct answer, starting at 0
        "explanation": "Explanation to the problem"
    }
    """
    try:
        response = client.chat.completions.create(
            model="qwen-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Generate a {difficulty} difficulty programming problem",
                },
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            extra_body={"enable_thinking": False},
        )
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("Missing response")
        else:
            challenge_data = json.loads(content)
            required_fields = [
                "title",
                "difficulty",
                "options",
                "correct_answer_id",
                "explanation",
            ]
            for field in required_fields:
                if field not in challenge_data:
                    raise ValueError(f"Missing required field: {field}")
            return challenge_data
    except Exception as e:
        print(e)
        return {
            "title": "This is a default challenge",
            "difficulty": "easy",
            "options": [
                "choose me",
                "choose option 1",
                "choose option 1",
                "choose option 1",
            ],
            "correct_answer_id": 0,
            "explanation": "Default explanation",
        }


if __name__ == "__main__":
    question_json = generate_challenge_with_ai("easy")
    print(question_json)
