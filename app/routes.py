from flask import Blueprint, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

main = Blueprint("main", __name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@main.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    input_text = data.get("input", "").strip()
    output_text = data.get("output", "").strip()
    energy = data.get("energy", 5)
    focus = data.get("focus", 5)
    mood = data.get("mood", 5)

    if not input_text and not output_text:
        insight = "No reflection today — that's okay. 🌱"
        conversion = 0
    elif input_text and not output_text:
        insight = "You consumed but didn't apply it yet. Try tomorrow. 🧠➡️⚡"
        conversion = 20
    elif output_text and not input_text:
        insight = "Created from within — beautiful. ✍️"
        conversion = 50
    else:
        conversion = int((len(output_text) / (len(input_text) + len(output_text)) * 100))

        # Call ChatGPT
        try:
            prompt = f"""Today I consumed:
{input_text}

Today I produced:
{output_text}

Energy: {energy}/10
Focus: {focus}/10
Mood: {mood}/10

Give a short reflective insight (max 2 sentences). No generic advice — make it feel personal and thoughtful."""

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You're an insightful but concise reflection coach."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=60,
                temperature=0.7
            )

            insight = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API:\n{e}")
            insight = "(AI insight unavailable due to error)"


    return jsonify({
        "conversionRate": conversion,
        "summary": f"{insight} (Energy: {energy}/10, Focus: {focus}/10, Mood: {mood}/10)"
    })