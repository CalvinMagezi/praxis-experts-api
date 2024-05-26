from flask import Blueprint, request, jsonify
from praxis.agent_manager import AgentManager
import os

experts_blueprint = Blueprint('experts', __name__)
agent_manager = AgentManager()

@experts_blueprint.route('/experts', methods=['POST'])
def create_expert():
    data = request.json
    position = data.get("position")

    if not position:
        return jsonify({"error": "Position is required"}), 400

    # Pass position to Praxis assistant
    praxis_assistant_id = os.getenv('PRAXIS_ASSISTANT_ID')
    if not praxis_assistant_id:
        return jsonify({"error": "Praxis assistant ID not found in environment variables"}), 500

    # Create and run thread with Praxis assistant
    prompt = f"""
    Please provide the details of an expert for the position: {position}.
    Format the response as follows and keep it exactly in this format to ensure proper extraction:
    Name: [Expert's Name]
    Position: [Expert's Position]
    Description: [Expert's Description]
    """
    run = agent_manager.create_and_run_thread(
        assistant_id=praxis_assistant_id,
        messages=[{"role": "user", "content": prompt}]
    )

    if run.status != 'completed':
        return jsonify({"error": "Failed to process position with Praxis assistant"}), 500

    # Extract the suggested expert details from the response
    messages_list = agent_manager.list_thread_messages(run.thread_id)
    expert_details = extract_expert_details_from_response(messages_list)

    # Check if the necessary details are present
    if not expert_details or 'name' not in expert_details or 'position' not in expert_details or 'description' not in expert_details:
        return jsonify({"error": "Failed to extract necessary expert details from response"}), 500

    # Create the actual expert based on the suggested details
    expert = agent_manager.create_agent(
        name=expert_details["name"],
        instructions=f"You are an expert in {expert_details['position']}.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4o"
    )

    return jsonify({
        "expert_id": expert.id,
        "name": expert_details["name"],
        "instructions": f"You are an expert in {expert_details['position']}.",
        "description": expert_details["description"]
    }), 201

def extract_expert_details_from_response(messages_list):
    # Extract and return the details of the suggested expert from the messages
    expert_details = {}
    for message in messages_list:
        if message['role'] == 'assistant':
            content = message['content']
            print(f"Assistant Response Content: {content}")  # Log the response content for debugging
            expert_details = parse_expert_details(content)
            break
    return expert_details

def parse_expert_details(content):
    # Parse the content to extract the expert details
    details = {}

    lines = content.split("\n")
    for line in lines:
        if line.startswith("Name:"):
            details["name"] = line.split(":", 1)[1].strip()
        elif line.startswith("Position:"):
            details["position"] = line.split(":", 1)[1].strip()
        elif line.startswith("Description:"):
            details["description"] = line.split(":", 1)[1].strip()

    if "name" not in details:
        details["name"] = "Expert " + details.get("position", "Unknown")  # Fallback name if not found

    return details