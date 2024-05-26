from flask import Blueprint, request, jsonify
from praxis.agent_manager import AgentManager
from praxis.globals import projects, project_id_counter
import os

projects_blueprint = Blueprint('projects', __name__)
agent_manager = AgentManager()

@projects_blueprint.route('/projects', methods=['POST'])
def create_project():
    global project_id_counter
    data = request.json
    project_id = project_id_counter
    projects[project_id] = {
        "project_name": data["project_name"],
        "description": data["description"],
        "experts": [],
        "manager": None
    }
    project_id_counter += 1

    # Pass project details to Praxis assistant
    praxis_assistant_id = os.getenv('PRAXIS_ASSISTANT_ID')
    if not praxis_assistant_id:
        return jsonify({"error": "Praxis assistant ID not found in environment variables"}), 500

    # Create and run thread with Praxis assistant
    run = agent_manager.create_and_run_thread(
        assistant_id=praxis_assistant_id,
        messages=[{"role": "user", "content": f"Project title: {data['project_name']}, Description: {data['description']}"}]
    )

    if run.status != 'completed':
        return jsonify({"error": "Failed to process project with Praxis assistant"}), 500

    # Extract the suggested experts from the response
    messages_list = agent_manager.list_thread_messages(run.thread_id)
    suggested_experts = extract_experts_from_response(messages_list)

    # Create the actual experts based on the suggested experts
    experts = generate_experts(suggested_experts)
    manager = generate_manager()

    projects[project_id]["experts"] = experts
    projects[project_id]["manager"] = manager

    return jsonify({"project_id": project_id, "experts": experts, "manager": manager}), 201

def extract_experts_from_response(messages_list):
    # Extract and return the list of suggested experts from the messages
    experts = []
    for message in messages_list:
        if message['role'] == 'assistant':
            content = message['content']
            # Assuming the content contains the list of experts with their positions
            experts = parse_expert_list(content)
            break
    return experts

def parse_expert_list(content):
    # Parse the content to extract the list of experts with their names and positions
    # This is a placeholder implementation, adjust based on actual response format
    experts = []
    for line in content.split("\n"):
        parts = line.split(": ")
        if len(parts) == 2:
            name, position = parts
            experts.append({"name": name.strip(), "position": position.strip()})
        else:
            # Log the unexpected format for debugging
            print(f"Unexpected format: {line}")
    return experts

def generate_experts(expert_data):
    experts = []
    for expert in expert_data:
        agent = agent_manager.create_agent(
            name=expert["name"],
            instructions=f"You are an expert in {expert['position']}.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4o"
        )
        experts.append({"id": agent.id, "name": expert["name"], "position": expert["position"]})
    return experts

def generate_manager():
    manager = agent_manager.create_agent(
        name="Project Manager",
        instructions="You are the project manager responsible for overseeing this project.",
        tools=[],
        model="gpt-4o"
    )
    return {"id": manager.id, "name": "Project Manager", "position": "Project Manager"}