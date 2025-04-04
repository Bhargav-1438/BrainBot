from flask import Flask, request, jsonify, render_template
import math

app = Flask(__name__)

# Formula Solver Function
def solve_formula(question):
    try:
        question = question.lower()

        # Greetings
        if any(greet in question for greet in ["hello", "hi", "hey"]):
            return "Hi there! 👋 I'm BrainBot. Ask me to solve formulas like force, speed, etc."

        # Help / Instructions
        if "help" in question:
            return ("🧠 I can solve basic physics formulas!\n"
                    "Try asking things like:\n"
                    "- What is force if mass is 10 and acceleration is 5?\n"
                    "- What is speed if distance is 100 and time is 10?")

        # Example: Force = mass × acceleration
        if "force" in question:
            m = float(question.split("mass is")[1].split()[0])
            a = float(question.split("acceleration is")[1].split()[0])
            return f"✅ Force = {m * a} N"

        # Example: Speed = distance / time
        elif "speed" in question:
            d = float(question.split("distance is")[1].split()[0])
            t = float(question.split("time is")[1].split()[0])
            return f"✅ Speed = {d / t} m/s"

        # Add more formulas here...

        else:
            return "🤖 Hmm... I didn't understand that. Type 'help' to see what I can do."
    except:
        return "⚠️ Oops! Make sure your question is in the correct format like 'mass is 10'."

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()
    question = data.get("question", "")
    answer = solve_formula(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
