# Cursor AI Prompt: Upgrade the-game-maker-web to Production-Grade

## Context

I have a working Flask-based AI application (the-game-maker-web) that uses LangChain agents to turn children's books into playable games. I want to upgrade it with production-grade features from a reference project (ai-trip-planner) that uses FastAPI, LangGraph, and enterprise observability patterns.

## Current Stack

- **Backend**: Flask 3.0, LangChain, Claude Sonnet 4.5
- **Session**: In-memory dictionary
- **Orchestration**: Sequential state machine (5 phases)
- **Frontend**: Vanilla JS with Tailwind CSS
- **Deployment**: Basic Render configuration

## Target Improvements

Upgrade to production-grade architecture with:
1. **FastAPI** - Better async, auto docs, streaming
2. **LangGraph** - Sophisticated graph-based orchestration
3. **PostgreSQL + Redis** - Persistent sessions with caching
4. **LangSmith/Arize** - Production observability & tracing
5. **Docker** - Containerized deployment
6. **RAG** - Vector database for smart template selection
7. **Resilience** - Retry logic, circuit breakers, graceful degradation

## Detailed Implementation Plan

See `PRODUCTION_UPGRADE_PLAN.md` for the complete 9-week phased implementation guide.

---

## Quick Start Instructions for Cursor

### Phase 1: FastAPI Migration (Start Here)

**Task**: Convert the Flask application to FastAPI while maintaining all existing functionality.

**Files to Modify**:
- `backend/app.py` → `backend/main.py`
- `backend/requirements.txt`

**Implementation**:

1. **Install FastAPI dependencies**:
```bash
pip install fastapi uvicorn[standard] python-multipart
```

2. **Create `backend/main.py`**:
```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI(
    title="The Game Maker API",
    description="AI-powered game generation from children's books",
    version="2.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

# Request/Response Models
class StartSessionRequest(BaseModel):
    user_id: str | None = None

class StartSessionResponse(BaseModel):
    success: bool
    session_id: str
    message: str
    phase: str

class MessageRequest(BaseModel):
    message: str
    session_id: str

class MessageResponse(BaseModel):
    success: bool
    message: str
    phase: str
    agent: str | None = None
    is_complete: bool = False
    game_data: dict | None = None

# Convert ALL Flask routes to FastAPI routes here
# Start with /api/health, then /api/start_session, then /api/message

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "the-game-maker",
        "version": "2.0.0"
    }

# TODO: Convert remaining routes from app.py

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

3. **Testing**:
- Run: `uvicorn backend.main:app --reload`
- Check: `http://localhost:8000/docs` for auto-generated API docs
- Verify: All endpoints from Flask app are working

**Success Criteria**:
- [ ] All Flask endpoints converted to FastAPI
- [ ] Pydantic models for all requests/responses
- [ ] Auto-generated docs at /docs working
- [ ] Existing frontend still works (update port to 8000)
- [ ] Voice input still functioning

---

### Phase 2: LangSmith Observability

**Task**: Add production tracing for all AI agent calls.

**Files to Create**:
- `backend/observability/langsmith_config.py`
- `backend/observability/logging_config.py`

**Implementation**:

1. **Install dependencies**:
```bash
pip install langsmith python-json-logger prometheus-client
```

2. **Create observability module**:
```python
# backend/observability/langsmith_config.py

import os
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.tracers import LangChainTracer

def setup_langsmith():
    """Configure LangSmith tracing."""
    tracer = LangChainTracer(
        project_name="the-game-maker-production"
    )
    return CallbackManager([tracer])
```

3. **Update .env**:
```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=<your_key>
LANGCHAIN_PROJECT=the-game-maker-production
```

4. **Modify all agents** to use callbacks:
```python
# In backend/agents/story_analyst.py, game_designer.py, code_generator.py
from observability.langsmith_config import setup_langsmith

callbacks = setup_langsmith()
agent = create_react_agent(..., callbacks=callbacks)
```

**Success Criteria**:
- [ ] LangSmith project created
- [ ] All agent executions traced
- [ ] LLM calls visible with token counts
- [ ] Errors captured in traces

---

### Phase 3: Docker Containerization

**Task**: Create Docker setup for consistent deployment.

**Files to Create**:
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`

**Implementation**:

See `PRODUCTION_UPGRADE_PLAN.md` Phase 1.2 for complete Docker configuration.

**Quick commands**:
```bash
docker build -t game-maker .
docker-compose up
```

**Success Criteria**:
- [ ] Docker build succeeds
- [ ] App runs in container
- [ ] Database connections working
- [ ] Health check passing

---

### Phase 4: PostgreSQL + Redis

**Task**: Replace in-memory sessions with database persistence and caching.

**Files to Create**:
- `backend/database/models.py`
- `backend/database/db.py`
- `backend/database/repository.py`
- `backend/cache/redis_client.py`

**Dependencies**:
```bash
pip install sqlalchemy psycopg2-binary alembic redis
```

See `PRODUCTION_UPGRADE_PLAN.md` Phase 4 for detailed implementation.

**Success Criteria**:
- [ ] Sessions persisting to PostgreSQL
- [ ] Redis caching session lookups
- [ ] Database migrations working
- [ ] Games being saved to database

---

### Phase 5: LangGraph Migration

**Task**: Convert sequential state machine to LangGraph for better orchestration.

**Files to Create**:
- `backend/agents/graph_orchestrator.py`

**Dependencies**:
```bash
pip install langgraph
```

**Implementation**:

See `PRODUCTION_UPGRADE_PLAN.md` Phase 3.1 for complete LangGraph workflow.

**Key concept**:
- Current: Sequential phases (story → design → generate)
- New: Graph-based with conditional routing and parallel potential

**Success Criteria**:
- [ ] Graph compiles
- [ ] State transitions working
- [ ] Agents executing in graph
- [ ] Conditional edges functioning

---

### Phase 6: RAG for Template Selection

**Task**: Add vector search for intelligent game template selection.

**Files to Create**:
- `backend/rag/embeddings.py`
- `backend/data/game_knowledge.json`

**Dependencies**:
```bash
pip install langchain-openai chromadb
```

**Implementation**:

See `PRODUCTION_UPGRADE_PLAN.md` Phase 5.1 for RAG setup.

**Success Criteria**:
- [ ] Vector store initialized
- [ ] Templates searchable
- [ ] Best template selection working
- [ ] Fallback logic in place

---

## Implementation Order (Recommended)

### Sprint 1 (Week 1): Foundation
1. ✅ FastAPI migration
2. ✅ Docker setup
3. ✅ Update dependencies

### Sprint 2 (Week 2): Observability
4. ✅ LangSmith integration
5. ✅ Metrics & logging

### Sprint 3 (Week 3-4): Data Layer
6. ✅ PostgreSQL setup
7. ✅ Redis caching
8. ✅ Database migrations

### Sprint 4 (Week 5): Orchestration
9. ✅ LangGraph migration
10. ✅ Graph-based workflow

### Sprint 5 (Week 6): Intelligence
11. ✅ RAG implementation
12. ✅ Smart template selection

### Sprint 6 (Week 7-8): Production Hardening
13. ✅ Error handling & resilience
14. ✅ Circuit breakers
15. ✅ Streaming responses
16. ✅ Analytics

### Sprint 7 (Week 9): Deployment
17. ✅ Production deployment
18. ✅ Monitoring setup
19. ✅ Load testing

---

## Key Principles

1. **Maintain Working App**: Never break existing functionality
2. **Test Incrementally**: Each phase should be tested before moving on
3. **Use Reference Code**: Look at ai-trip-planner patterns for guidance
4. **Document Changes**: Update README as you go
5. **Measure Impact**: Track performance improvements

---

## Common Issues & Solutions

### Issue: FastAPI not finding templates
**Solution**: Check `template_folder` path is correct relative to main.py

### Issue: LangSmith traces not appearing
**Solution**: Verify environment variables are set and API key is valid

### Issue: Database connection failing in Docker
**Solution**: Ensure services start in correct order with `depends_on` in docker-compose

### Issue: Redis connection errors
**Solution**: Check REDIS_URL format: `redis://localhost:6379`

---

## Testing Each Phase

```bash
# After each major change, run:

# 1. Unit tests
pytest tests/

# 2. API tests
curl http://localhost:8000/api/health

# 3. Integration test
# Create session, send message, verify response

# 4. Load test
# Use Locust or Apache Bench for stress testing
```

---

## Success Metrics

After completion, you should achieve:

- ✅ **Performance**: <500ms API response time
- ✅ **Reliability**: 99.9% uptime
- ✅ **Observability**: 100% trace coverage
- ✅ **Scalability**: 1000+ concurrent sessions
- ✅ **Error Rate**: <0.1% failed requests

---

## Resources

- **Detailed Plan**: `PRODUCTION_UPGRADE_PLAN.md` (in this repo)
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **LangSmith Docs**: https://docs.smith.langchain.com/

---

## Getting Started in Cursor

1. Open this project in Cursor
2. Start with **Phase 1: FastAPI Migration**
3. Use Cursor's AI to help convert each Flask route
4. Test thoroughly after each phase
5. Refer to `PRODUCTION_UPGRADE_PLAN.md` for detailed implementation
6. Ask Cursor to implement specific sections from the plan

---

**Example Cursor Prompts**:

```
"Help me convert the Flask app in backend/app.py to FastAPI.
Use the patterns from PRODUCTION_UPGRADE_PLAN.md Phase 1.1"

"Create the LangSmith observability module as described in
PRODUCTION_UPGRADE_PLAN.md Phase 2.1"

"Set up Docker and docker-compose following the configuration
in PRODUCTION_UPGRADE_PLAN.md Phase 1.2"
```

---

Good luck with your upgrade! 🚀
