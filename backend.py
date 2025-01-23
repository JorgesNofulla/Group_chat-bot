from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from random import choice
from groq import Groq
import time

app = Flask(__name__, static_folder="static")
CORS(app)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# ---------------------------
# AI personality definitions
# ---------------------------
lion_system_prompt = {
    "role": "system",
    "content": ( "you are Joe Biden. there are 2 other users on the chat besides you, so dont get confused by their interaction."
                "Join this group chat seamlessly and have fun. Interact with them, say your opinion, counter their opinion or add to it."
                "In this chat it will be you, main user and Donald Trump. You love to make fun of Donald trump but you love the main user."
                                "Keep your answers relatively short."
  
                )
}

        # "Rules:\n"
        # "1) Respond ONLY as LionAI.\n"
        # "2) Do not speak on behalf of RaccoonAI.\n"
        # "3) If you need to quote RaccoonAI, do so explicitly as a direct quote, for example: 'RaccoonAI said: ...'\n"
        # "4) Remain respectful and regal in your tone.\n"
        # "5) If the user specifically addresses the other AI, you may remain silent.\n"

        #         "You are LionAI, a wise and regal AI with a lion-like personality. "
        # "You are in a group chat with RaccoonAI and the user.\n\n"
        # "You try to give a different opionion from RaccoonAI or support and add to his opinion, the choice is up to you. Of course you only do it when it makes common sense."
        # "Keep answers reasonably short but always answer, never stay silent."
        # "I repeat, you always have something to say.
raccoon_system_prompt = {
    "role": "system",
    "content": ( "you are Donald Trump. there are 2 other users on the chat besides you, so dont get confused by their interaction."
                "Join this group chat seamlessly and have fun. Interact with them, say your opinion, counter their opinion or add to it."
                "In this chat it will be you, main user and Joe Biden.You love to make fun of Joe Biden but you love the main user."
                "Keep your answers relatively short."

    )
}


        # "Rules:\n"
        # "1) Respond ONLY as RaccoonAI.\n"
        # "2) Do not speak on behalf of LionAI.\n"
        # "3) If you need to quote LionAI, do so explicitly as a direct quote, for example: 'LionAI said: ...'\n"
        # "4) Keep things playful but not disrespectful.\n"
        # "5) If the user specifically addresses LionAI, you may remain silent.\n"
# ---------------------------
# Global Chat History
# ---------------------------
chat_history = []

# ---------------------------
# Helper to generate responses
# ---------------------------
def generate_ai_response(messages):
    """Call Groq's chat completion."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.5,
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def build_messages_for_ai(ai_name, system_prompt, history):
    """
    Build the prompt for a particular AI.
    Skip that AI's own lines in history to avoid immediate self-repetition.
    """
    messages = [system_prompt]  # AI-specific system prompt

    for msg in history:
        if msg["role"] == "user":
            messages.append({"role": "user", "content": f"Main User (Jorges) said: {msg['content']}"})
        elif msg["role"] == "lion" and ai_name == "raccoon":
            # Raccoon sees Lion lines as 'assistant'
            messages.append({"role": "user", "content": f"Joe Biden said: {msg['content']}"})
        elif msg["role"] == "raccoon" and ai_name == "lion":
            # Lion sees Raccoon lines as 'assistant'
            messages.append({"role": "user", "content": f"Donald Trump said: {msg['content']}"})
        # if msg["role"] == ai_name, we skip it to avoid repeating own line

    return messages

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history

    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Error: Message cannot be empty."}), 400

    # Add user message to the chat history
    chat_history.append({"role": "user", "content": user_message})

    # Randomly decide who speaks first this round
    first_ai = choice(["raccoon", "lion"])
    second_ai = "lion" if first_ai == "raccoon" else "raccoon"

    # Prepare system prompts for each AI
    prompts = {
        "raccoon": raccoon_system_prompt,
        "lion": lion_system_prompt
    }

    responses_data = []

    # --- ROUND: each AI speaks exactly once ---
    # First AI's turn
    first_messages = build_messages_for_ai(
        ai_name=first_ai,
        system_prompt=prompts[first_ai],
        history=chat_history
    )
    first_ai_response = generate_ai_response(first_messages)
    chat_history.append({"role": first_ai, "content": first_ai_response})
    responses_data.append({"ai": first_ai, "response": first_ai_response})



    # Add a delay here
    time.sleep(1)  # Adjust the delay time as needed


    # Second AI's turn
    second_messages = build_messages_for_ai(
        ai_name=second_ai,
        system_prompt=prompts[second_ai],
        history=chat_history
    )
    second_ai_response = generate_ai_response(second_messages)
    chat_history.append({"role": second_ai, "content": second_ai_response})
    responses_data.append({"ai": second_ai, "response": second_ai_response})


    return jsonify({"responses": responses_data})

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
