# Getting Started with The Game Maker (Web Version)

## What We've Built So Far

Welcome to The Game Maker web application! This is Phase 1-2 of the implementation.

### ✅ What's Working Now

**Phase 1: Foundation** ✅
- Complete project structure
- Python virtual environment
- All dependencies installed
- Flask backend with API routes
- Basic session management

**Phase 2: Story Analyst Agent** ✅
- First AI agent fully implemented using LangChain Python
- Book identification through conversation (voice-first!)
- Conversational flow with Claude 4.5 Sonnet
- Pydantic schemas for data validation
- Tool calling patterns demonstrated

**Phase 3: Frontend** ✅
- Clean web chat interface with Tailwind CSS
- Voice input using Web Speech API (click 🎤 to talk)
- Real-time chat with the Story Analyst
- Phase indicators showing progress
- Responsive design for iPad/desktop

### 🚧 What's Next

**Phase 3-4: Remaining Agents**
- Game Designer agent (simple placeholder working)
- Code Generator agent
- Complete Phaser.js game templates

**Phase 5-6: Polish & Deploy**
- Enhanced UI animations
- Render deployment configuration
- Production testing

## Quick Start

### 1. Set Up Your API Key

You need an Anthropic API key to power the AI agents.

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Get your API key from the dashboard

### 2. Configure Environment

Create a `.env` file in the project root:

```bash
cp env.example .env
```

Edit `.env` and add your API key:

```bash
ANTHROPIC_API_KEY=your_actual_api_key_here
FLASK_SECRET_KEY=any_random_string_for_sessions
FLASK_ENV=development
```

### 3. Run the Application

The easiest way is to use the start script:

```bash
./start.sh
```

Or manually:

```bash
# Activate virtual environment
source venv/bin/activate

# Run Flask app
python backend/app.py
```

### 4. Open in Browser

Navigate to: **http://localhost:5000**

## How to Use

1. **Start**: The app loads and the Story Analyst greets you
2. **Talk or Type**: Click 🎤 to speak or type your message
3. **Tell about a book**: Say something like "I read Dragons Love Tacos"
4. **Confirm**: Agent will confirm the book - say "yes"
5. **Discuss**: Answer questions about the story
6. **Design**: (Coming soon) Collaborate on game design
7. **Play**: (Coming soon) Play your generated game!

### Voice Input

- **Click** the 🎤 button to start speaking
- **Speak clearly** - it will transcribe what you say
- **Works best in Chrome, Edge, or Safari**
- **Needs microphone permission** (browser will ask)
- **Fallback to typing** if voice doesn't work

## Testing the Story Analyst

You can test just the agent in Python without the web interface:

```bash
# Activate virtual environment
source venv/bin/activate

# Start Python
python3

# Test the agent
>>> from backend.agents.story_analyst import get_story_analyst
>>> agent = get_story_analyst()
>>> result = agent.process_message("I read Dragons Love Tacos")
>>> print(result['message'])
```

## Project Structure Overview

```
the-game-maker-web/
├── backend/
│   ├── app.py                  # Flask app (DONE ✅)
│   ├── agents/
│   │   ├── story_analyst.py    # First agent (DONE ✅)
│   │   ├── orchestrator.py     # Coordinates agents (DONE ✅)
│   │   ├── game_designer.py    # TODO
│   │   └── code_generator.py   # TODO
│   ├── tools/
│   │   ├── book_tools.py       # Agent tools (DONE ✅)
│   │   └── ...                 # More tools TODO
│   └── schemas/
│       ├── book_schema.py      # Data validation (DONE ✅)
│       └── game_schema.py      # Game schemas (DONE ✅)
├── frontend/
│   ├── templates/
│   │   └── index.html          # Chat UI (DONE ✅)
│   └── static/
│       ├── js/
│       │   ├── app.js          # Main logic (DONE ✅)
│       │   └── voice.js        # Voice API (DONE ✅)
│       └── css/
│           └── styles.css      # Styling (DONE ✅)
└── docs/
    └── EDUCATIONAL_PRD.md      # Full requirements
```

## What You Can Do Right Now

### Working Features

1. **Start a conversation** with the Story Analyst
2. **Use voice input** to tell it about a book
3. **Book identification** - it will identify title and author
4. **Book discussion** - answer questions about the story
5. **See the chat interface** - modern, responsive design
6. **Watch phase transitions** - from identifying to discussing

### What Happens Next

After you discuss the book (5-7 exchanges), the orchestrator will:
- Transition to "Designing" phase (placeholder for now)
- Eventually move to "Generating" phase
- Finally show "Complete" with a link to play

The Game Designer and Code Generator agents are the next step!

## Troubleshooting

### "ModuleNotFoundError"
```bash
# Make sure you're in the virtual environment
source venv/bin/activate
# Reinstall dependencies
pip install -r backend/requirements.txt
```

### "Invalid API key"
- Check your `.env` file has `ANTHROPIC_API_KEY=sk-ant-...`
- Make sure there are no quotes around the key
- Restart the Flask app after editing .env

### Voice not working
- Voice requires HTTPS or localhost (localhost works)
- Check browser console for errors
- Make sure you allowed microphone permission
- Try Chrome or Edge (best support)

### Port 5000 already in use
Edit `backend/app.py` line ~150:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Changed to 5001
```

## API Endpoints (For Developers)

### POST `/api/start_session`
Initializes a new game creation session.

### POST `/api/message`
Sends a message to the active agent.

**Body**:
```json
{
  "message": "your message here",
  "session_id": "optional_session_id"
}
```

### GET `/api/session/<session_id>`
Gets the current session state.

### GET `/api/health`
Health check endpoint.

## Next Steps

Now that Phase 1-2 is complete, here's what's coming:

1. **Game Designer Agent** - Collaborates on game mechanics
2. **Code Generator Agent** - Creates working Phaser.js games
3. **Game Templates** - Platformer, top-down, obstacle avoider
4. **Production Deploy** - Push to Render for always-available access

## Contributing

This is a learning project! Feel free to:
- Experiment with the agent prompts
- Add new tools for the agents
- Improve the UI
- Try different conversation flows

## Need Help?

- Check the `README.md` for full documentation
- Read `docs/EDUCATIONAL_PRD.md` for the complete vision
- See `backend/agents/story_analyst.py` for agent examples
- Check Flask logs in the terminal for debugging

---

**Current Status**: Phase 1-2 Complete ✅  
**Next Milestone**: Game Designer Agent 🎨  
**Version**: 2.0-alpha

**Made with ❤️ for Farrah and aspiring game makers!**

