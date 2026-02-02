"""Root agent definition for ADK."""

from .orchestrator import root_agent

# ADK looks for 'root_agent' in agent.py
__all__ = ["root_agent"]
