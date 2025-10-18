# 🎮 The Game Maker - Web Version

Transform children's books into playable arcade games using AI agents!

## What Is This?

The Game Maker is a web application that uses three specialized AI agents to turn books into games:

1. **Story Analyst** - Identifies books and discusses them through conversation
2. **Game Designer** - Collaborates on game design and mechanics  
3. **Code Generator** - Generates working Phaser.js games

Built with **voice-first** interaction - just talk about your book and watch it become a game!

## Game Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERACTION                            │
│                    (Voice or Text Input 🎤💬)                       │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    ORCHESTRATOR      │
                    │  (Coordinates Flow)  │
                    └──────────┬───────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
            ▼                  ▼                  ▼
   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
   │ STORY ANALYST  │  │ GAME DESIGNER  │  │ CODE GENERATOR │
   │    Agent 1     │  │    Agent 2     │  │    Agent 3     │
   └────────┬───────┘  └────────┬───────┘  └────────┬───────┘
            │                   │                   │
            ▼                   ▼                   ▼
    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
    │  Identifies  │    │  Collaborates│    │  Generates   │
    │  the book    │───▶│  on game     │───▶│  Phaser.js   │
    │  & discusses │    │  mechanics   │    │  game code   │
    │  the story   │    │  & design    │    │              │
    └──────────────┘    └──────────────┘    └──────┬───────┘
                                                    │
                                                    ▼
                                            ┌──────────────┐
                                            │  PLAYABLE    │
                                            │   GAME! 🎮   │
                                            └──────────────┘

Phase Flow:
───────────
1. IDENTIFYING  → "What book did you read?"
2. DISCUSSING   → Deep dive into story, characters, plot
3. DESIGNING    → Brainstorm mechanics, objectives, interactions
4. GENERATING   → Create working game code
5. PLAYING      → Launch and enjoy your game!
```

## Why This Version?

This is a **pivot from the React Native mobile version** to solve technical issues (streaming support) and improve the experience:

- ✅ **Simpler**: Web app vs mobile complexity
- ✅ **Faster development**: Python + Flask + LangChain (battle-tested)
- ✅ **Better UX**: Voice-first, no camera/upload friction
- ✅ **Same learning**: All agent architecture patterns intact
- ✅ **Works everywhere**: iPad, desktop, any browser

See `../the-game-maker-mobile-v1/ARCHIVED.md` for the pivot decision.

## Tech Stack

**Backend**:
- Python 3.11+
- Flask (web framework)
- LangChain (agent framework)
- Anthropic Claude 4.5 Sonnet (AI model)
- Pydantic (data validation)

**Frontend**:
- HTML/CSS/JavaScript
- Tailwind CSS (styling)
- Web Speech API (voice input)
- Phaser.js (game engine)

**Deployment**:
- Render (production hosting)

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Installation

1. **Clone or navigate to this directory**:
   ```bash
   cd the-game-maker-web
   ```

2. **Set up Python virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

5. **Run the app**:
   ```bash
   python backend/app.py
   ```

6. **Open in browser**:
   ```
   http://localhost:5000
   ```

## Usage

1. **Open the app** in your browser
2. **Start talking** - the agent will ask "What book did you read?"
3. **Tell it the book name** - e.g., "Dragons Love Tacos"
4. **Confirm** - the agent will confirm the title and author
5. **Discuss the book** - answer questions about the story
6. **Design the game** - collaborate on game mechanics
7. **Play your game** - it generates and you play!

### Voice Input

- Click the **🎤 microphone button** to speak
- Or type in the text input
- Or press **Ctrl+V** to start voice input

## Project Structure

```
the-game-maker-web/
├── backend/
│   ├── app.py                  # Flask app with API routes
│   ├── agents/
│   │   ├── story_analyst.py    # Book identification & discussion
│   │   ├── game_designer.py    # Game design (TODO)
│   │   ├── code_generator.py   # Code generation (TODO)
│   │   └── orchestrator.py     # Multi-agent coordination
│   ├── tools/
│   │   ├── book_tools.py       # Tools for Story Analyst
│   │   ├── game_tools.py       # Tools for Game Designer (TODO)
│   │   └── code_tools.py       # Tools for Code Generator (TODO)
│   ├── schemas/
│   │   ├── book_schema.py      # Pydantic schemas for books
│   │   └── game_schema.py      # Pydantic schemas for games
│   ├── templates/
│   │   └── phaser_templates.py # Phaser.js game templates (TODO)
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css      # Custom styles
│   │   └── js/
│   │       ├── app.js          # Main app logic
│   │       └── voice.js        # Web Speech API
│   └── templates/
│       ├── index.html          # Main chat interface
│       └── game.html           # Game player page
├── docs/
│   └── EDUCATIONAL_PRD.md      # Full project requirements
├── env.example                 # Environment variables template
├── render.yaml                 # Render deployment config (TODO)
└── README.md                   # This file
```

## Current Status

### ✅ Completed (Phase 1-2)

- [x] Project structure and setup
- [x] Flask backend with API endpoints
- [x] Story Analyst agent with LangChain
- [x] Book identification through conversation
- [x] Web chat interface
- [x] Voice input with Web Speech API
- [x] Session management
- [x] Orchestrator for agent coordination
- [x] Pydantic schemas for data validation

### 🚧 In Progress (Phase 3)

- [ ] Game Designer agent
- [ ] Game design tools
- [ ] Complete orchestrator transitions

### 📋 TODO (Phase 4-7)

- [ ] Code Generator agent
- [ ] Phaser.js game templates
- [ ] Code generation tools
- [ ] Game rendering and playback
- [ ] UI polish and styling
- [ ] Render deployment configuration
- [ ] Production deployment

## API Endpoints

### `POST /api/start_session`
Initialize a new game creation session.

**Response**:
```json
{
  "success": true,
  "session_id": "...",
  "message": "Hi! I'm so excited...",
  "phase": "identifying"
}
```

### `POST /api/message`
Send a message and get agent response.

**Request**:
```json
{
  "message": "Dragons Love Tacos",
  "session_id": "..."
}
```

**Response**:
```json
{
  "success": true,
  "message": "Is that 'Dragons Love Tacos' by Adam Rubin?",
  "phase": "discussing",
  "agent": "story_analyst",
  "is_complete": false
}
```

### `GET /api/session/<session_id>`
Get current session state.

### `GET /api/game/<session_id>`
Get generated game HTML.

## Development

### Running in Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
python backend/app.py
```

The Flask app runs with `debug=True` by default, so changes auto-reload.

### Testing the Story Analyst

You can test just the agent in Python:

```python
from agents.story_analyst import get_story_analyst

agent = get_story_analyst()
result = agent.process_message("I read Dragons Love Tacos")
print(result)
```

### Environment Variables

See `env.example` for all configuration options:

- `ANTHROPIC_API_KEY` - Your Anthropic API key (required)
- `FLASK_SECRET_KEY` - Secret key for sessions (auto-generated if not set)
- `FLASK_ENV` - `development` or `production`

## Deployment to Render

### Setup

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect to your repository
4. Configure:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `gunicorn backend.app:app`
   - **Environment**: Add `ANTHROPIC_API_KEY`

### Configuration File

Create `render.yaml` (coming soon) for automated deployment.

## Learning Objectives

This project teaches:

**For You (Dad)**:
- Agent creation with LangChain Python
- Tool calling patterns
- Multi-agent orchestration
- Flask API development
- Session management
- Production deployment

**For Your Daughter**:
- Book discussion and analysis
- Creative game design thinking
- Seeing her ideas come to life
- Understanding what Dad builds

See `docs/EDUCATIONAL_PRD.md` for complete educational goals.

## Troubleshooting

### "ModuleNotFoundError"
Make sure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r backend/requirements.txt
```

### "Invalid API key"
Check your `.env` file has correct `ANTHROPIC_API_KEY`.

### Voice not working
Voice input requires HTTPS or localhost. Works fine in development (localhost).
Some browsers don't support Web Speech API (works in Chrome, Edge, Safari).

### Port already in use
Change port in `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

## Contributing

This is a personal learning project, but feel free to:
- Report issues
- Suggest improvements
- Share your own adaptations

## License

MIT License - feel free to use for your own learning!

## Acknowledgments

- **Concept**: Inspired by a daughter's wish to turn books into games
- **Architecture**: Based on modern agent-based AI patterns
- **Powered by**: Claude 4.5 Sonnet, LangChain, Flask, Phaser.js

---

**Made with ❤️ for aspiring game makers everywhere!**

*Version 2.0 - Web Edition*

