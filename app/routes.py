from flask import Blueprint, request, jsonify

main = Blueprint("main", __name__)

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
        insight = "You consumed but didn’t apply it yet. Try tomorrow. 🧠➡️⚡"
        conversion = 20
    elif output_text and not input_text:
        insight = "Created from within — beautiful. ✍️"
        conversion = 50
    else:
        conversion = int((len(output_text) / (len(input_text) + len(output_text)) * 100))
        insight = "Great — you learned and applied. 🔄"

    return jsonify({
        "conversionRate": conversion,
        "summary": f"{insight} (Energy: {energy}/10, Focus: {focus}/10, Mood: {mood}/10)"
    })