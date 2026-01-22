# Agentic Meeting Assistant

An intelligent system that processes Google Meet transcripts, understands meeting intents using AI agents, and automatically executes actions like scheduling calendar events and sending emails.

## Features

- **Meeting Transcript Processing**: Capture and parse Google Meet transcripts
- **AI-Powered Intent Detection**: Uses agents to understand what actions were discussed in meetings
- **Automated Action Execution**: Automatically creates calendar events and sends emails based on meeting intents
- **Safety Guards**: Built-in safety mechanisms to prevent unintended automations
- **Chrome Extension**: Browser extension for seamless integration with Google Meet
- **API Endpoints**: RESTful API for intent classification, confirmation, and action logging

## Project Structure

```
├── backend/                 # Python backend application
│   ├── app/
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── agents/         # Intent detection agents
│   │   ├── api/            # API endpoints
│   │   ├── automation/     # Action execution and routing
│   │   │   ├── executors/  # Calendar and email executors
│   │   │   └── normalizers/# Data normalization utilities
│   │   ├── config/         # Configuration and credentials
│   │   ├── db/             # Database models
│   │   ├── prompts/        # AI prompt templates
│   │   ├── schemas/        # Data validation schemas
│   │   ├── services/       # Business logic services
│   │   └── data/           # Sample data
│   ├── transcripts/        # Stored meeting transcripts
│   └── requirements.txt    # Python dependencies
├── meet-transcript-extension/  # Chrome extension
│   ├── manifest.json       # Extension configuration
│   ├── content.js          # Content script
│   └── background.js       # Background script
└── README.md              # This file
```

## Getting Started

### Prerequisites

- Python 3.8+
- Google API credentials (for Calendar and Gmail)
- Chrome browser (for extension)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agentic-meeting-assistant
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure credentials**
   - Place your Google API `credentials.json` in `backend/app/config/`
   - Update `backend/app/config/settings.py` with your configuration

5. **Run the backend**
   ```bash
   python -m app.main
   ```

6. **Install the Chrome extension**
   - Open `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select `meet-transcript-extension/` folder

## API Endpoints

- `POST /intent` - Classify intent from a transcript
- `POST /clarify` - Request clarification for detected intents
- `POST /confirm` - Confirm actions to be executed
- `GET /logs` - Retrieve action logs
- `POST /transcript` - Submit a new transcript

## Configuration

### Backend Settings

Edit `backend/app/config/settings.py` to configure:
- LLM model and API keys
- Google Calendar and Gmail credentials
- Safety guard rules
- Logging preferences

### Environment Variables

Create a `.env` file in the backend directory:
```
OPENAI_API_KEY=your_key_here
GOOGLE_CREDENTIALS_PATH=./config/credentials.json
```

## Architecture

### Intent Detection
The system uses an AI agent to analyze transcripts and detect actionable intents such as:
- Calendar event creation
- Email sending
- Meeting scheduling

### Action Execution
Detected intents are routed to appropriate executors:
- **Calendar Executor**: Creates Google Calendar events
- **Email Executor**: Sends emails via Gmail
- **Safety Guard**: Validates actions before execution

### Data Flow
```
Transcript → Intent Agent → Intent Schema → Router → Executors → Actions
                                     ↓
                           Normalizers (Email, Datetime, Attendee)
```

## Usage Examples

### Basic Intent Detection

```python
from app.services.llm_service import LLMService
from app.agents.intent_agent import IntentAgent

agent = IntentAgent()
transcript = "Let's schedule a meeting with John next Tuesday at 2 PM"
intent = agent.detect_intent(transcript)
print(intent)
```

### With Safety Confirmation

```python
from app.api.confirm import confirm_action

# After intent detection
confirmed = confirm_action(intent)
if confirmed:
    # Execute the action
    pass
```

## Development

### Running Tests
```bash
pytest backend/tests/
```

### Code Structure
- Use FastAPI for API endpoints
- Pydantic for data validation
- SQLAlchemy for database operations
- Google API client for integrations

## Security Considerations

- Credentials are stored in `credentials.json` (not committed to git)
- Safety guards validate all automations before execution
- API endpoints should be protected with authentication in production
- Sensitive data in transcripts is handled carefully

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Create a Pull Request

## License

[Add your license here]

## Support

For issues and questions, please create an issue in the repository or contact the team.
