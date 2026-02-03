"""Main entry point for the Travel Documents Agent.

Usage:
  A2A Server:  uvicorn main:a2a_app --host localhost --port 8002
  CLI Mode:    python main.py
"""

import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from travel_documents_agent import root_agent, a2a_app


# Example travel data for testing
EXAMPLE_TRAVEL_DATA = """
Please create a travel document for the following trip:

Traveler: Max Mustermann
Destination: Mallorca, Spain
Check-in: 2025-07-15
Check-out: 2025-07-22
Duration: 7 nights

Hotel: Hotel Riu Palace Tres Islas
Address: Avinguda de l'Albatros, Playa de Palma, 07610 Mallorca
Rating: 5 stars
Room: Junior Suite with Sea View
Board: All Inclusive Plus

Outbound Flight: LH 4732 | Frankfurt (FRA) → Palma de Mallorca (PMI) | 15 Jul 2025, 09:45 - 12:30
Return Flight: LH 4733 | Palma de Mallorca (PMI) → Frankfurt (FRA) | 22 Jul 2025, 17:15 - 20:00

Total Price: €3,249 (for 2 adults)

Please include local events, attractions, restaurants, and activities for our stay.
"""


async def run_cli():
    """Run the Travel Documents Agent in CLI mode."""
    session_service = InMemorySessionService()

    runner = Runner(
        agent=root_agent,
        app_name="TravelDocumentsAgent",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="TravelDocumentsAgent",
        user_id="user",
    )

    print("=" * 70)
    print("Travel Documents Agent - CLI Mode")
    print("=" * 70)
    print("\nFor A2A mode: uvicorn main:a2a_app --host localhost --port 8002")
    print("Agent card:   http://localhost:8002/.well-known/agent-card.json")
    print("\nThis agent creates visual travel documents with local events,")
    print("attractions, and recommendations based on your travel booking.")
    print("\nCommands:")
    print("  'example' - Run with example travel data")
    print("  'quit'    - Exit the agent")
    print("\nOr paste your travel booking details to get started.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except EOFError:
            break

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye! Have a great trip!")
            break

        if not user_input:
            continue

        # Use example data if requested
        if user_input.lower() == "example":
            user_input = EXAMPLE_TRAVEL_DATA
            print("\n[Using example travel data...]\n")

        content = types.Content(
            role="user",
            parts=[types.Part(text=user_input)],
        )

        print("\nAgent: ", end="", flush=True)

        try:
            async for event in runner.run_async(
                session_id=session.id,
                user_id="user",
                new_message=content,
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(part.text, end="", flush=True)
        except Exception as e:
            print(f"\nError: {e}")

        print("\n")


if __name__ == "__main__":
    asyncio.run(run_cli())
