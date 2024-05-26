from flask import Blueprint, request, jsonify
from praxis.agent_manager import AgentManager
import os

praxis_blueprint = Blueprint('praxis', __name__)
agent_manager = AgentManager()

@praxis_blueprint.route('/praxis', methods=['POST'])
def chat_with_praxis():
    data = request.json
    message = data.get("message")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # Get Praxis assistant ID from environment variables
    praxis_assistant_id = os.getenv('PRAXIS_ASSISTANT_ID')
    if not praxis_assistant_id:
        return jsonify({"error": "Praxis assistant ID not found in environment variables"}), 500

    # Create and run thread with Praxis assistant
    run = agent_manager.create_and_run_thread(
        assistant_id=praxis_assistant_id,
        messages=[{"role": "user", "content": message}]
    )

    if run.status != 'completed':
        return jsonify({"error": "Failed to process message with Praxis assistant"}), 500

    # Extract the response from the assistant
    messages_list = agent_manager.list_thread_messages(run.thread_id)
    assistant_response = extract_assistant_response(messages_list)

    return jsonify({"response": assistant_response}), 200

def extract_assistant_response(messages_list):
    # Extract and return the response from the assistant
    for message in messages_list:
        if message['role'] == 'assistant':
            return message['content']
    return "No response from assistant."

# Remember to import and register the blueprint in your main app file