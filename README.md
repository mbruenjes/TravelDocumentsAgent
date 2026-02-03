# Travel Documents Agent

A Google ADK agent that creates comprehensive, visually appealing travel documents with local events, attractions, and recommendations.

## Features

- Receives travel booking details (hotel, flights, dates)
- Searches for local events and festivals during travel dates via Google Search
- Finds top attractions, restaurants, and activities
- Generates beautiful HTML/PDF travel documents
- Supports A2A (Agent-to-Agent) protocol for integration with other agents

## Architecture

```
TravelDocumentsOrchestrator (root_agent)
    └─ ResearchAndGenerateAgent (sequential)
        ├─ EventsSearchAgent (Google Search)
        └─ DocumentGeneratorAgent (HTML/PDF generation)
```

## Installation

1. Install dependencies:
```bash
pip install -e .
```

2. Set up environment:
```bash
copy .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

## Usage

### A2A Server (Recommended)
```bash
uvicorn main:a2a_app --host localhost --port 8002
```
This exposes the agent via A2A protocol. The agent card is available at `http://localhost:8002/.well-known/agent-card.json`.

### Alternative: Run from package
```bash
uvicorn travel_documents_agent:a2a_app --host localhost --port 8002
```

### CLI Mode
```bash
python main.py
```

### Example Input

```json
{
  "traveler": "Max Mustermann",
  "destination": "Mallorca",
  "country": "Spain",
  "check_in": "2025-07-15",
  "check_out": "2025-07-22",
  "hotel": {
    "name": "Hotel Riu Palace Tres Islas",
    "address": "Playa de Palma, Mallorca",
    "rating": 5,
    "room_type": "Junior Suite Sea View",
    "board_type": "All Inclusive Plus"
  },
  "flights": {
    "outbound": "LH 4732 | Frankfurt → Palma | 15 Jul 09:45",
    "return": "LH 4733 | Palma → Frankfurt | 22 Jul 17:15"
  },
  "total_price": "€3,249"
}
```

## Output

The agent generates travel documents in the `travel_documents/` folder:
- HTML format (default): Can be opened in any browser
- PDF format (optional): Requires WeasyPrint

## A2A Integration

This agent uses the `to_a2a()` function from Google ADK to expose itself via the A2A protocol.

### Start the A2A Server

```bash
uvicorn main:a2a_app --host localhost --port 8002
```

This exposes:
- **Agent Card**: `http://localhost:8002/.well-known/agent-card.json`
- **A2A RPC Endpoint**: `http://localhost:8002/`

### How it works

The `to_a2a()` function wraps the ADK agent and:
- Auto-generates an agent card from the agent metadata
- Handles A2A protocol compatibility
- Provides direct control over service exposure

### Connecting from Another Agent

Other agents can discover this agent at the agent card URL and send messages via the A2A protocol.

## Dependencies

- `google-adk[a2a]`: Google Agent Development Kit with A2A support
- `google-genai`: Gemini API client
- `jinja2`: HTML templating
- `weasyprint`: PDF generation (optional)
- `uvicorn`: ASGI server for A2A
- `python-dotenv`: Environment variable management
