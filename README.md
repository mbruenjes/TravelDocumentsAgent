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

### Web UI with A2A (Recommended)
```bash
adk web --a2a travel_documents_agent
```
This starts the web UI AND exposes the A2A endpoint at `/.well-known/agent.json`.

### API Server with A2A (Headless)
```bash
adk api_server --a2a travel_documents_agent
```

### Web UI Only (No A2A)
```bash
adk web travel_documents_agent
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

Google ADK has built-in A2A support. Just add the `--a2a` flag:

```bash
adk web --a2a travel_documents_agent
```

This exposes:
- **Agent Card**: `http://localhost:8000/.well-known/agent.json`
- **A2A Endpoints**: For task creation and message exchange

### Connecting from Another Agent

Other ADK agents can discover and communicate with this agent using the standard A2A protocol at the `/.well-known/agent.json` endpoint.

## Dependencies

- `google-adk`: Google Agent Development Kit
- `google-genai`: Gemini API client
- `jinja2`: HTML templating
- `weasyprint`: PDF generation (optional)
- `python-dotenv`: Environment variable management
