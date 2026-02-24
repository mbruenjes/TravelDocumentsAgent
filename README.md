# Travel Documents Agent

A multi-agent system built with [Google ADK](https://github.com/google/adk-python) that creates comprehensive, visually appealing travel documents enriched with live destination research via Google Search.

## Features

- **Smart Research** - Automatically searches for local events, festivals, attractions, restaurants, and activities during your travel dates
- **Beautiful Documents** - Generates responsive HTML documents with professional styling, or optional PDF export
- **Multi-Agent Architecture** - Orchestrator delegates to specialized sub-agents for research and document generation
- **A2A Protocol** - Exposes the agent via [Agent-to-Agent](https://github.com/google/A2A) protocol for seamless integration with other agents
- **Flexible Input** - Accepts structured JSON or natural language travel booking details
- **CLI & Server Modes** - Run interactively from the terminal or as a standalone A2A server

## Architecture

```
TravelDocumentsOrchestrator (root_agent, gemini-2.5-pro)
│   Parses travel booking data and coordinates sub-agents
│
└── ResearchAndGenerateAgent (SequentialAgent)
    │
    ├── EventsSearchAgent
    │   Tool: google_search
    │   Searches for events, attractions, restaurants, activities, weather
    │
    └── DocumentGeneratorAgent
        Tools: generate_travel_document, save_document_to_file
        Compiles research into a styled HTML/PDF travel document
```

## Prerequisites

- Python >= 3.12
- A [Google API Key](https://aistudio.google.com/apikey) with access to the Gemini API

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd TravelDocumentsAgent
```

2. Install dependencies:
```bash
pip install -e .
```

3. Configure your API key:
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

## Usage

### A2A Server Mode (Recommended)

Start the agent as an A2A-compatible server:

```bash
uvicorn main:a2a_app --host localhost --port 8002
```

This exposes:
- **Agent Card**: `http://localhost:8002/.well-known/agent-card.json`
- **A2A RPC Endpoint**: `http://localhost:8002/`

Other agents can discover and interact with this agent via the A2A protocol.

### CLI Mode

Run the agent interactively from the terminal:

```bash
python main.py
```

Commands:
- `example` - Run with built-in example travel data
- `quit` - Exit the agent

### Example Input

You can provide travel details as structured JSON:

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
    "outbound": "LH 4732 | Frankfurt -> Palma | 15 Jul 09:45",
    "return": "LH 4733 | Palma -> Frankfurt | 22 Jul 17:15"
  },
  "total_price": "EUR 3,249"
}
```

Or as natural language:

> I'm traveling to Mallorca from July 15-22, staying at Hotel Riu Palace (5-star, All Inclusive). Flights with Lufthansa from Frankfurt. Please include local events and restaurant recommendations.

## Output

Generated documents are saved to the `travel_documents/` directory:

- **HTML** (default) - Responsive design with inline CSS, opens in any browser
- **PDF** (optional) - Requires [WeasyPrint](https://weasyprint.org/)

Each document includes:
- Trip overview and booking reference
- Hotel and flight details
- Weather forecast for your dates
- Local events and festivals
- Must-see attractions
- Restaurant recommendations
- Activities and experiences
- Practical travel tips (currency, transport, customs)

## Project Structure

```
TravelDocumentsAgent/
├── main.py                                  # Entry point (CLI + A2A server)
├── pyproject.toml                           # Project metadata and dependencies
├── .env.example                             # Environment variable template
│
├── travel_documents_agent/
│   ├── __init__.py                          # Exports root_agent, a2a_app
│   ├── agent.py                             # Agent setup
│   ├── orchestrator.py                      # Root orchestrator agent definition
│   ├── agent.json                           # A2A agent card metadata
│   │
│   ├── sub_agents/
│   │   ├── events_search_agent.py           # Google Search research agent
│   │   └── document_generator_agent.py      # HTML/PDF document generation agent
│   │
│   ├── tools/
│   │   └── document_tools.py                # Jinja2 rendering and file I/O
│   │
│   └── templates/
│       └── travel_document.html             # Jinja2 HTML template
│
└── travel_documents/                        # Generated output documents
```

## Dependencies

| Package | Purpose |
|---|---|
| `google-adk[a2a]` | Google Agent Development Kit with A2A support |
| `google-genai` | Gemini API client |
| `jinja2` | HTML templating engine |
| `weasyprint` | PDF generation (optional, falls back to HTML) |
| `uvicorn` | ASGI server for A2A |
| `python-dotenv` | Environment variable management |

## License

This project is provided as-is for demonstration and educational purposes.