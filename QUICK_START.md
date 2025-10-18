# 🚀 Quick Start Guide

## Run the App in 3 Steps

### 1. Add Your API Key

```bash
cd the-game-maker-web
cp env.example .env
# Edit .env and paste your ANTHROPIC_API_KEY
```

Get API key: https://console.anthropic.com/

### 2. Start the App

```bash
./start.sh
```

### 3. Open Browser

http://localhost:5000

**That's it!** 🎉

---

## Try It Out

1. Click 🎤 microphone button (or type)
2. Say: **"I read Dragons Love Tacos"**
3. Agent confirms: "Is that 'Dragons Love Tacos' by Adam Rubin?"
4. Say: **"Yes"**
5. Answer questions about the story
6. Watch the magic happen! ✨

---

## What Works Right Now

✅ Voice input (click 🎤)  
✅ Book identification  
✅ Story discussion  
✅ Phase transitions  
✅ Beautiful UI  

## What's Coming Next

⏳ Game design collaboration  
⏳ Code generation  
⏳ Playable Phaser.js games  
⏳ Production deployment  

---

## Keyboard Shortcuts

- `Ctrl+V` - Start voice input
- `Enter` - Send message
- `Escape` - Clear input

---

## Troubleshooting

**Voice not working?**
- Allow microphone permission in browser
- Use Chrome, Edge, or Safari

**API errors?**
- Check .env has correct ANTHROPIC_API_KEY
- Make sure no quotes around the key
- Restart Flask app

**Port busy?**
- Edit `backend/app.py` line 150: change port to 5001

---

## Quick Commands

```bash
# Start app
./start.sh

# Or manually
source venv/bin/activate
python backend/app.py

# Test agent in Python
python3
>>> from backend.agents.story_analyst import get_story_analyst
>>> agent = get_story_analyst()
>>> result = agent.process_message("Dragons Love Tacos")
```

---

## Project Status

**Phase 1-2**: ✅ Complete (Foundation + Story Analyst)  
**Phase 3-4**: ⏳ TODO (Game Designer + Code Generator)  
**Phase 5**: ⏳ TODO (Deploy to production)

**Time to MVP**: 2-3 weekends

---

## Important Files

📄 `STATUS.md` - Detailed status and progress  
📄 `GETTING_STARTED.md` - Full setup guide  
📄 `README.md` - Complete documentation  
📁 `backend/agents/story_analyst.py` - Agent example  
📁 `backend/app.py` - Flask application  

---

## Next Steps

1. ✅ Test current features
2. ⏳ Build Game Designer agent
3. ⏳ Port Phaser.js templates
4. ⏳ Build Code Generator
5. ⏳ Deploy to Render
6. 🎉 Show your daughter!

---

**Made with ❤️ for Farrah**

**Version**: 2.0-alpha  
**Last Updated**: October 17, 2025

