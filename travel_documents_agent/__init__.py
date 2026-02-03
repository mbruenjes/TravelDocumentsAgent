"""Travel Documents Agent - Creates visual travel documents with local events and attractions."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from .orchestrator import root_agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# Get the path to the custom agent card
_agent_card_path = os.path.join(os.path.dirname(__file__), "agent.json")

# Create A2A app for exposing the agent via A2A protocol
# Uses custom agent card for detailed skill definitions
a2a_app = to_a2a(root_agent, port=8002, agent_card=_agent_card_path)

__all__ = ["root_agent", "a2a_app"]
