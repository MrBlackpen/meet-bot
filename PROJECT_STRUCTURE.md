agentic-meeting-assistant/
│
├── backend/
│   ├── agent_logs.db                  # SQLite database for agent logs
│   │
│   ├── app/
│   │   ├── main.py                   # FastAPI application entry point
│   │   │
│   │   ├── agents/                   # AI agent modules
│   │   │   └── intent_agent.py       # Intent detection agent
│   │   │
│   │   ├── api/                      # API route handlers
│   │   │   ├── clarify.py            # Clarification API endpoints
│   │   │   ├── confirm.py            # Confirmation API endpoints
│   │   │   ├── intent.py             # Intent API endpoints
│   │   │   ├── logs.py               # Logs API endpoints
│   │   │   └── transcript.py         # Transcript API endpoints
│   │   │
│   │   ├── automation/               # Automation and action execution
│   │   │   ├── __init__.py
│   │   │   ├── action_dispatcher.py  # Action dispatcher/routing
│   │   │   ├── logger.py             # Automation logger
│   │   │   ├── router.py             # Automation router
│   │   │   ├── safety_guard.py       # Safety checks and validations
│   │   │   │
│   │   │   ├── executors/            # Action executors
│   │   │   │   ├── calendar_executor.py  # Calendar action executor
│   │   │   │   └── email_executor.py     # Email action executor
│   │   │   │
│   │   │   └── normalizers/          # Data normalizers
│   │   │       ├── attendee_normalizer.py  # Attendee data normalizer
│   │   │       ├── datetime_normalizer.py  # Datetime normalizer
│   │   │       └── email_normalizer.py     # Email normalizer
│   │   │
│   │   ├── config/                   # Configuration files
│   │   │   ├── credentials.json      # Google API credentials
│   │   │   ├── settings.py           # Application settings/config
│   │   │   └── token.json            # Local OAuth token (do not commit)
│   │   │
│   │   ├── data/                     # Data files
│   │   │   └── demo_transcript.txt   # Demo transcript data
│   │   │
│   │   ├── db/                       # Database layer
│   │   │   ├── database.py           # Database connection and setup
│   │   │   └── models.py             # SQLAlchemy database models
│   │   │
│   │   ├── prompts/                  # LLM prompt templates
│   │   │   └── intent_prompt.txt     # Intent detection prompt template
│   │   │
│   │   ├── schemas/                  # Pydantic models/schemas
│   │   │   ├── intent_schema.py      # Intent data schemas
│   │   │   └── transcript_schema.py  # Transcript data schemas
│   │   │
│   │   └── services/                 # Business logic services
│   │       ├── google_auth_service.py      # Google OAuth service
│   │       ├── llm_service.py              # LLM service wrapper
│   │       ├── transcript_service.py       # Transcript service
│   │       └── transcript_session_service.py  # Transcript session service
│   │
│   ├── transcripts/                  # Stored meeting transcripts
│   │   └── meet_*.txt                # Transcript files (timestamped)
│   │
│   └── requirements.txt              # Python dependencies
│                                    # (fastapi, uvicorn, pydantic, 
│                                    #  python-dotenv, google-generativeai,
│                                    #  google-genai, google-api-python-client,
│                                    #  google-auth, google-auth-oauthlib,
│                                    #  google-auth-httplib2, sqlalchemy)
│
├── meet-transcript-extension/         # Chrome extension (Google Meet transcript capture)
│   ├── manifest.json                 # Extension configuration
│   ├── content.js                    # Content script for transcript capture
│   └── background.js                 # Background script for extension
│
├── .gitignore                        # Git ignore rules
├── README.md                         # Project documentation
└── PROJECT_STRUCTURE.md              # This file


## Structure Overview

### Root Level
- `backend/` — Main backend application directory
- `meet-transcript-extension/` — Chrome extension for capturing Google Meet transcripts
- `.gitignore` — Git ignore rules for version control
- `README.md` — Project documentation and getting started guide
- `PROJECT_STRUCTURE.md` — This file - detailed project structure

### Backend (`backend/app/`)

**Core Application:**
- `main.py` — FastAPI application entry point

**Agents:**
- `agents/` — AI agent implementations
  - `intent_agent.py` — Intent detection and classification agent

**API Layer:**
- `api/` — API route handlers (FastAPI routers)
  - `clarify.py` — Clarification endpoints for user queries
  - `confirm.py` — Confirmation endpoints for user actions
  - `intent.py` — Intent detection endpoints
  - `logs.py` — Agent logs retrieval endpoints
  - `transcript.py` — Transcript submission and management endpoints

**Automation System:**
- `automation/` — Automation and action execution framework
  - `action_dispatcher.py` — Routes actions to appropriate executors
  - `router.py` — Automation routing logic
  - `safety_guard.py` — Safety checks and validations before execution
  - `logger.py` — Automation-specific logging
  - `executors/` — Action executors for different services
    - `calendar_executor.py` — Calendar operations (create events, etc.)
    - `email_executor.py` — Email operations
  - `normalizers/` — Data normalization utilities
    - `attendee_normalizer.py` — Normalize attendee information
    - `datetime_normalizer.py` — Normalize date/time formats
    - `email_normalizer.py` — Normalize email addresses

**Configuration:**
- `config/` — Configuration and settings
  - `settings.py` — Application settings and environment variables
  - `token.json` — Local OAuth token cache (should not be committed)

**Data Layer:**
- `data/` — Data files and demos
  - `demo_transcript.txt` — Sample transcript data for testing
- `db/` — Database layer
  - `database.py` — Database connection and session management
  - `models.py` — SQLAlchemy ORM models

**Services:**
- `services/` — Business logic and service layers
  - `llm_service.py` — LLM (Language Model) service wrapper
  - `google_auth_service.py` — Google OAuth authentication service
  - `transcript_service.py` — Transcript processing and management
  - `transcript_session_service.py` — Transcript session state management

**Prompts:**
- `prompts/` — LLM prompt templates
  - `intent_prompt.txt` — Intent detection prompt template

**Schemas:**
- `schemas/` — Pydantic data models/schemas
  - `intent_schema.py` — Intent detection data schemas

### Configuration & Data Files

**Dependencies:**
- `requirements.txt` — Python package dependencies
  - FastAPI, Uvicorn, Pydantic
  - Google APIs (generative AI, API client, auth)
  - SQLAlchemy for database operations

**Database:**
- `agent_logs.db` — SQLite database for storing agent execution logs
- `transcripts/` — Directory storing captured meeting transcripts
  - Transcript files are named with format: `meet_YYYY-MM-DDTHH-MM-SS-sssZ.txt`
  - Each file contains the transcript from a single Google Meet session

**Virtual Environment:**
- Not checked into the repo (create locally as needed)

### Architecture Notes

This project follows a FastAPI application architecture with clear separation of concerns:

1. **API Layer** (`api/`) — HTTP endpoints and request/response handling
2. **Agent Layer** (`agents/`) — AI agent implementations for intent detection
3. **Automation Layer** (`automation/`) — Action execution framework with:
   - Executors for different service integrations (calendar, email)
   - Normalizers for data standardization
   - Safety guards for validation
   - Action routing and dispatching
4. **Service Layer** (`services/`) — External service integrations (LLM, Google Auth)
5. **Data Layer** (`db/`) — Database models and connections
6. **Configuration** (`config/`) — Application settings

The automation system enables the meeting assistant to execute actions like scheduling calendar events and sending emails based on detected intents from meeting transcripts. The clarification API allows the system to ask for additional information when needed.