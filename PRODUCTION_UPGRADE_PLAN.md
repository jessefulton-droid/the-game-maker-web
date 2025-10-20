# Production Upgrade Plan: the-game-maker-web

**Objective**: Upgrade the-game-maker-web with production-grade features from ai-trip-planner while maintaining the creative, user-friendly experience.

---

## Executive Summary

This plan transforms the-game-maker-web from a working prototype into a production-ready system by incorporating enterprise-grade patterns from ai-trip-planner:

### Key Upgrades
1. **FastAPI Migration** - Better async performance, auto-generated docs
2. **LangGraph Orchestration** - More sophisticated multi-agent coordination
3. **Observability Platform** - LangSmith/Arize integration for monitoring
4. **RAG Implementation** - Vector search for game templates and book knowledge
5. **Production Infrastructure** - Docker, better error handling, graceful degradation
6. **Database Backend** - PostgreSQL/Redis for session management
7. **Monitoring & Metrics** - Health checks, performance tracking, logging

### What We Keep
✅ Voice-first conversational UX
✅ Creative game generation output
✅ Claude 4.5 Sonnet AI model
✅ 5-phase workflow experience
✅ Phaser.js game templates

### What We Upgrade
🔄 Flask → FastAPI
🔄 LangChain → LangGraph
🔄 In-memory sessions → Database-backed
🔄 Basic logging → Production observability
🔄 Manual templates → RAG-powered template selection

---

## Phase 1: Foundation - Infrastructure Upgrade (Week 1)

### 1.1 Migrate Flask to FastAPI

**Why**: Better async support, automatic API docs, streaming support, better performance

**Implementation Steps**:

```python
# NEW: backend/main.py (replaces app.py)

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="The Game Maker API",
    description="AI-powered game generation from children's books",
    version="2.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

# Templates
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

# Routes (convert each Flask route)
@app.post("/api/start_session", response_model=StartSessionResponse)
async def start_session(request: StartSessionRequest):
    # Implementation
    pass

@app.post("/api/message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    # Implementation with streaming support
    pass

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "the-game-maker",
        "version": "2.0.0",
        "ai_model": "claude-sonnet-4.5",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

**Dependencies Update**:

```txt
# NEW: backend/requirements.txt additions

# FastAPI and ASGI
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
python-multipart>=0.0.9

# Keep existing
langchain>=0.3.0,<0.4.0
langchain-anthropic>=0.3.0,<0.4.0
anthropic>=0.34.0
pydantic>=2.7.4,<3.0.0
python-dotenv==1.0.0
```

**Testing Checklist**:
- [ ] All existing endpoints migrated to FastAPI
- [ ] Pydantic models for all request/response objects
- [ ] Auto-generated docs at `/docs` working
- [ ] Voice input still functioning
- [ ] Session management working

---

### 1.2 Add Docker Support

**Why**: Consistent deployment, easier production management, matches ai-trip-planner pattern

**Implementation**:

```dockerfile
# NEW: Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# NEW: docker-compose.yml

version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    volumes:
      - ./backend:/app/backend
      - ./frontend:/app/frontend
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=gamemaker
      - POSTGRES_USER=gamemaker
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

**Testing Checklist**:
- [ ] `docker build -t game-maker .` succeeds
- [ ] `docker-compose up` runs all services
- [ ] Health check endpoint accessible
- [ ] Database connection working
- [ ] Redis connection working

---

## Phase 2: Observability - Production Monitoring (Week 2)

### 2.1 Add LangSmith Integration

**Why**: Production-grade tracing for all LLM calls, agent execution, and debugging

**Implementation**:

```python
# NEW: backend/observability/langsmith_config.py

import os
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.tracers import LangChainTracer

def setup_langsmith():
    """Configure LangSmith tracing for all agents."""

    tracer = LangChainTracer(
        project_name="the-game-maker-production",
        client=None  # Uses LANGCHAIN_API_KEY from env
    )

    callback_manager = CallbackManager([tracer])
    return callback_manager

# Add to .env
"""
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_key_here
LANGCHAIN_PROJECT=the-game-maker-production
"""
```

**Update Agent Creation**:

```python
# MODIFY: backend/agents/story_analyst.py

from observability.langsmith_config import setup_langsmith

def get_story_analyst():
    callbacks = setup_langsmith()

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
        callbacks=callbacks  # Add this
    )

    return agent
```

**Testing Checklist**:
- [ ] LangSmith project created
- [ ] Traces appearing in LangSmith dashboard
- [ ] Agent executions visible with timing
- [ ] LLM calls captured with tokens/cost
- [ ] Error traces showing failures

---

### 2.2 Add Application Logging & Metrics

**Why**: Production debugging, performance monitoring, error tracking

**Implementation**:

```python
# NEW: backend/observability/logging_config.py

import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    """Configure structured JSON logging for production."""

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # JSON formatter
    logHandler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s %(pathname)s %(lineno)d'
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    return logger

# NEW: backend/observability/metrics.py

from prometheus_client import Counter, Histogram, Gauge
import time

# Metrics
session_counter = Counter('gamemaker_sessions_total', 'Total sessions created')
message_counter = Counter('gamemaker_messages_total', 'Total messages processed', ['phase', 'agent'])
game_generation_counter = Counter('gamemaker_games_generated_total', 'Total games generated')
error_counter = Counter('gamemaker_errors_total', 'Total errors', ['error_type'])

# Latency tracking
message_latency = Histogram('gamemaker_message_latency_seconds', 'Message processing latency', ['phase'])
llm_latency = Histogram('gamemaker_llm_latency_seconds', 'LLM call latency', ['agent'])

# Active sessions
active_sessions_gauge = Gauge('gamemaker_active_sessions', 'Current active sessions')

class MetricsMiddleware:
    """Track request metrics."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        start_time = time.time()

        try:
            await self.app(scope, receive, send)
        except Exception as e:
            error_counter.labels(error_type=type(e).__name__).inc()
            raise
        finally:
            duration = time.time() - start_time
            # Track latency
```

**Add Metrics Endpoint**:

```python
# ADD TO: backend/main.py

from prometheus_client import make_asgi_app

# Mount Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

**Dependencies**:

```txt
# Add to requirements.txt
python-json-logger>=2.0.7
prometheus-client>=0.19.0
```

**Testing Checklist**:
- [ ] JSON logs appearing in stdout
- [ ] Metrics endpoint `/metrics` working
- [ ] Session counter incrementing
- [ ] Latency histograms recording
- [ ] Error counter tracking failures

---

## Phase 3: LangGraph Migration - Advanced Orchestration (Week 3)

### 3.1 Convert Sequential State Machine to LangGraph

**Why**: Parallel agent execution, better state management, production patterns from ai-trip-planner

**Implementation**:

```python
# NEW: backend/agents/graph_orchestrator.py

from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
import operator

class GameMakerState(TypedDict):
    """Shared state across all agents."""
    messages: Annotated[List[dict], operator.add]
    session_id: str
    phase: str
    user_message: str

    # Agent outputs
    book_analysis: dict | None
    game_design: dict | None
    game_html: str | None

    # Metadata
    conversation_count: int
    agent_outputs: dict

def create_game_maker_graph():
    """Create LangGraph workflow for game generation."""

    # Define the graph
    workflow = StateGraph(GameMakerState)

    # Add nodes (agents)
    workflow.add_node("story_analyst", story_analyst_node)
    workflow.add_node("game_designer", game_designer_node)
    workflow.add_node("code_generator", code_generator_node)

    # Define edges (flow control)
    workflow.set_entry_point("story_analyst")

    # Conditional routing
    workflow.add_conditional_edges(
        "story_analyst",
        should_continue_to_design,
        {
            "design": "game_designer",
            "continue_story": "story_analyst",
            "end": END
        }
    )

    workflow.add_conditional_edges(
        "game_designer",
        should_continue_to_generation,
        {
            "generate": "code_generator",
            "continue_design": "game_designer",
            "end": END
        }
    )

    workflow.add_edge("code_generator", END)

    # Compile the graph
    app = workflow.compile()
    return app

# Node implementations
async def story_analyst_node(state: GameMakerState) -> GameMakerState:
    """Process message through story analyst."""
    from agents.story_analyst import get_story_analyst

    agent = get_story_analyst()
    result = await agent.ainvoke({
        "input": state["user_message"],
        "chat_history": state["messages"]
    })

    # Update state
    state["messages"].append({
        "role": "assistant",
        "content": result["output"]
    })

    # Check if book analysis complete
    if result.get("book_analysis"):
        state["book_analysis"] = result["book_analysis"]
        state["phase"] = "designing"

    return state

async def game_designer_node(state: GameMakerState) -> GameMakerState:
    """Process message through game designer."""
    from agents.game_designer import get_game_designer

    agent = get_game_designer()
    result = await agent.ainvoke({
        "input": state["user_message"],
        "book_analysis": state["book_analysis"],
        "chat_history": state["messages"]
    })

    state["messages"].append({
        "role": "assistant",
        "content": result["output"]
    })

    if result.get("game_design"):
        state["game_design"] = result["game_design"]
        state["phase"] = "generating"

    return state

async def code_generator_node(state: GameMakerState) -> GameMakerState:
    """Generate game code."""
    from agents.code_generator import get_code_generator

    agent = get_code_generator()
    result = await agent.ainvoke({
        "game_design": state["game_design"]
    })

    state["game_html"] = result["game_html"]
    state["phase"] = "complete"

    return state

# Conditional functions
def should_continue_to_design(state: GameMakerState) -> str:
    """Determine if ready to move to game design."""
    if state.get("book_analysis"):
        return "design"
    elif state["conversation_count"] > 10:
        return "end"
    else:
        return "continue_story"

def should_continue_to_generation(state: GameMakerState) -> str:
    """Determine if ready to generate code."""
    if state.get("game_design"):
        return "generate"
    elif state["conversation_count"] > 15:
        return "end"
    else:
        return "continue_design"
```

**Update API Endpoint**:

```python
# MODIFY: backend/main.py

from agents.graph_orchestrator import create_game_maker_graph

# Global graph instance
game_graph = create_game_maker_graph()

@app.post("/api/message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """Process message through LangGraph workflow."""

    # Get current state from database
    state = await get_session_state(request.session_id)

    # Update state with new message
    state["user_message"] = request.message
    state["conversation_count"] += 1

    # Run through graph
    result = await game_graph.ainvoke(state)

    # Save updated state
    await save_session_state(request.session_id, result)

    return MessageResponse(
        success=True,
        message=result["messages"][-1]["content"],
        phase=result["phase"],
        is_complete=(result["phase"] == "complete"),
        game_data=result.get("game_html")
    )
```

**Dependencies**:

```txt
# Add to requirements.txt
langgraph>=0.2.0
```

**Testing Checklist**:
- [ ] Graph compiles without errors
- [ ] State transitions working correctly
- [ ] Conditional routing functioning
- [ ] All agents executing in graph
- [ ] State persistence working
- [ ] LangGraph visualization available

---

## Phase 4: Database Integration - Session Persistence (Week 4)

### 4.1 Add PostgreSQL for Session Storage

**Why**: Replace in-memory sessions, enable horizontal scaling, data persistence

**Implementation**:

```python
# NEW: backend/database/models.py

from sqlalchemy import Column, String, JSON, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=True)
    state = Column(JSON, nullable=False)
    phase = Column(String, default="identifying")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    session_id = Column(String, nullable=False)
    book_title = Column(String)
    book_author = Column(String)
    game_type = Column(String)
    game_html = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# NEW: backend/database/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://gamemaker:password@localhost/gamemaker")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# NEW: backend/database/repository.py

from sqlalchemy.orm import Session as DBSession
from database.models import Session, Game
from typing import Dict, Optional

class SessionRepository:
    """Repository for session operations."""

    def __init__(self, db: DBSession):
        self.db = db

    async def create_session(self, session_id: str, initial_state: Dict) -> Session:
        """Create new session."""
        session = Session(
            id=session_id,
            state=initial_state,
            phase="identifying"
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    async def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID."""
        return self.db.query(Session).filter(Session.id == session_id).first()

    async def update_session(self, session_id: str, state: Dict, phase: str) -> Session:
        """Update session state."""
        session = await self.get_session(session_id)
        if session:
            session.state = state
            session.phase = phase
            self.db.commit()
            self.db.refresh(session)
        return session

    async def save_game(self, session_id: str, game_data: Dict) -> Game:
        """Save generated game."""
        game = Game(
            session_id=session_id,
            book_title=game_data.get("book_title"),
            book_author=game_data.get("book_author"),
            game_type=game_data.get("game_type"),
            game_html=game_data.get("game_html")
        )
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game
```

**Update API with Database**:

```python
# MODIFY: backend/main.py

from fastapi import Depends
from database.db import get_db, init_db
from database.repository import SessionRepository

@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    init_db()

@app.post("/api/start_session", response_model=StartSessionResponse)
async def start_session(
    request: StartSessionRequest,
    db: DBSession = Depends(get_db)
):
    """Create new session in database."""
    repo = SessionRepository(db)

    session_id = os.urandom(16).hex()
    initial_state = {
        "messages": [],
        "phase": "identifying",
        "conversation_count": 0
    }

    session = await repo.create_session(session_id, initial_state)

    return StartSessionResponse(
        success=True,
        session_id=session_id,
        message="Hi! I'm so excited...",
        phase="identifying"
    )
```

**Dependencies**:

```txt
# Add to requirements.txt
sqlalchemy>=2.0.25
psycopg2-binary>=2.9.9
alembic>=1.13.1
```

**Database Migrations**:

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

**Testing Checklist**:
- [ ] Database tables created
- [ ] Sessions persisting to PostgreSQL
- [ ] Session retrieval working
- [ ] State updates saving correctly
- [ ] Games being saved
- [ ] Migrations working

---

### 4.2 Add Redis for Caching

**Why**: Fast session lookup, reduce database load, temporary data storage

**Implementation**:

```python
# NEW: backend/cache/redis_client.py

import redis
import json
import os
from typing import Optional, Dict

class RedisCache:
    """Redis cache client for session management."""

    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.client = redis.from_url(self.redis_url, decode_responses=True)
        self.ttl = 3600 * 2  # 2 hours

    async def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session from cache."""
        data = self.client.get(f"session:{session_id}")
        return json.loads(data) if data else None

    async def set_session(self, session_id: str, state: Dict) -> bool:
        """Cache session state."""
        return self.client.setex(
            f"session:{session_id}",
            self.ttl,
            json.dumps(state)
        )

    async def delete_session(self, session_id: str) -> bool:
        """Remove session from cache."""
        return self.client.delete(f"session:{session_id}")

    async def get_or_fetch(self, session_id: str, fetch_func):
        """Get from cache or fetch from database."""
        cached = await self.get_session(session_id)
        if cached:
            return cached

        # Fetch from database
        data = await fetch_func(session_id)
        if data:
            await self.set_session(session_id, data)
        return data

# Usage in API
cache = RedisCache()

async def get_session_state(session_id: str) -> Dict:
    """Get session with cache layer."""
    return await cache.get_or_fetch(
        session_id,
        lambda sid: repo.get_session(sid)
    )
```

**Dependencies**:

```txt
# Add to requirements.txt
redis>=5.0.1
```

**Testing Checklist**:
- [ ] Redis connection working
- [ ] Sessions caching correctly
- [ ] Cache hits reducing DB queries
- [ ] TTL expiring old sessions
- [ ] Cache invalidation working

---

## Phase 5: RAG Implementation - Smart Template Selection (Week 5)

### 5.1 Vector Database for Game Templates

**Why**: Intelligent template selection based on book themes, better game generation

**Implementation**:

```python
# NEW: backend/rag/embeddings.py

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import os

class GameTemplateRAG:
    """RAG system for game template selection."""

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.vectorstore = None
        self._initialize_templates()

    def _initialize_templates(self):
        """Load game templates into vector store."""

        templates = [
            Document(
                page_content="Platformer game with jumping mechanics, collecting items while avoiding obstacles. Best for adventure stories with exploration.",
                metadata={
                    "template_type": "platformer",
                    "themes": ["adventure", "exploration", "journey"],
                    "mechanics": ["jumping", "collecting", "avoiding"]
                }
            ),
            Document(
                page_content="Top-down exploration game where player moves in all directions collecting items within time limit. Great for treasure hunt stories.",
                metadata={
                    "template_type": "topdown",
                    "themes": ["exploration", "treasure", "discovery"],
                    "mechanics": ["movement", "collection", "time-based"]
                }
            ),
            Document(
                page_content="Obstacle avoider where player dodges falling or moving objects. Perfect for chase or escape stories.",
                metadata={
                    "template_type": "obstacle_avoider",
                    "themes": ["danger", "chase", "survival", "escape"],
                    "mechanics": ["dodging", "reflexes", "timing"]
                }
            )
        ]

        self.vectorstore = Chroma.from_documents(
            documents=templates,
            embedding=self.embeddings,
            persist_directory="./data/template_vectors"
        )

    async def find_best_template(self, book_analysis: dict) -> str:
        """Find best game template based on book analysis."""

        # Create search query from book analysis
        query = f"""
        Book themes: {', '.join(book_analysis.get('themes', []))}
        Plot summary: {book_analysis.get('plot_summary', '')}
        Main conflict: {book_analysis.get('conflict', '')}
        """

        # Search for similar templates
        results = self.vectorstore.similarity_search_with_score(query, k=1)

        if results:
            doc, score = results[0]
            return doc.metadata["template_type"]

        # Fallback to platformer
        return "platformer"

# NEW: backend/data/game_knowledge.json

{
  "templates": [
    {
      "type": "platformer",
      "description": "Side-scrolling game with platforms and jumping",
      "best_for": ["adventure", "journey", "exploration"],
      "examples": ["Where the Wild Things Are", "The Very Hungry Caterpillar"]
    },
    {
      "type": "topdown",
      "description": "Top-down view with multi-directional movement",
      "best_for": ["treasure hunt", "collection", "discovery"],
      "examples": ["Dragons Love Tacos", "The Mitten"]
    },
    {
      "type": "obstacle_avoider",
      "description": "Dodge incoming obstacles or enemies",
      "best_for": ["chase", "escape", "danger", "conflict"],
      "examples": ["The Gruffalo", "Room on the Broom"]
    }
  ]
}
```

**Update Code Generator to Use RAG**:

```python
# MODIFY: backend/agents/code_generator.py

from rag.embeddings import GameTemplateRAG

template_rag = GameTemplateRAG()

async def generate_game(game_design: dict, book_analysis: dict) -> str:
    """Generate game using RAG-selected template."""

    # Use RAG to find best template
    recommended_template = await template_rag.find_best_template(book_analysis)

    # Override if designer specified different type
    template_type = game_design.get("game_type", recommended_template)

    # Generate game...
```

**Dependencies**:

```txt
# Add to requirements.txt
langchain-openai>=0.1.0
chromadb>=0.4.22
```

**Testing Checklist**:
- [ ] Vector store initialized
- [ ] Templates embedded correctly
- [ ] Similarity search working
- [ ] Best template selection accurate
- [ ] Fallback logic working

---

## Phase 6: Advanced Error Handling & Resilience (Week 6)

### 6.1 Graceful Degradation

**Why**: System should degrade gracefully when external services fail (like ai-trip-planner pattern)

**Implementation**:

```python
# NEW: backend/resilience/fallbacks.py

from functools import wraps
import asyncio
from typing import Callable, Any

class FallbackHandler:
    """Handle service failures with graceful degradation."""

    @staticmethod
    def with_fallback(fallback_func: Callable):
        """Decorator for fallback handling."""
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"{func.__name__} failed: {e}, using fallback")
                    return await fallback_func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def with_retry(max_attempts: int = 3, delay: float = 1.0):
        """Decorator for retrying failed operations."""
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(max_attempts):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        if attempt < max_attempts - 1:
                            await asyncio.sleep(delay * (2 ** attempt))
                raise last_exception
            return wrapper
        return decorator

# Example usage in agents

@FallbackHandler.with_fallback(fallback_func=generate_generic_response)
@FallbackHandler.with_retry(max_attempts=3)
async def call_claude_api(message: str) -> str:
    """Call Claude API with retry and fallback."""
    # API call implementation
    pass

async def generate_generic_response(*args, **kwargs) -> str:
    """Fallback when Claude API fails."""
    return "I'm having trouble connecting right now. Let's try again in a moment."
```

**Circuit Breaker Pattern**:

```python
# NEW: backend/resilience/circuit_breaker.py

from enum import Enum
import time

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered

class CircuitBreaker:
    """Circuit breaker for external service calls."""

    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""

        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """Reset on successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        """Track failure and potentially open circuit."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
claude_circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60)

async def call_claude_with_protection(message: str):
    return await claude_circuit_breaker.call(
        call_claude_api,
        message
    )
```

**Testing Checklist**:
- [ ] Retry logic working
- [ ] Fallback responses triggered on failure
- [ ] Circuit breaker opening after threshold
- [ ] Circuit breaker recovering after timeout
- [ ] Error metrics tracking failures

---

### 6.2 Enhanced Error Handling

**Implementation**:

```python
# NEW: backend/errors/exceptions.py

class GameMakerException(Exception):
    """Base exception for Game Maker errors."""
    pass

class SessionNotFoundError(GameMakerException):
    """Session doesn't exist."""
    pass

class AgentExecutionError(GameMakerException):
    """Agent failed to execute."""
    pass

class GameGenerationError(GameMakerException):
    """Game generation failed."""
    pass

class RateLimitError(GameMakerException):
    """API rate limit exceeded."""
    pass

# NEW: backend/errors/handlers.py

from fastapi import Request, status
from fastapi.responses import JSONResponse

async def session_not_found_handler(request: Request, exc: SessionNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "session_not_found",
            "message": str(exc),
            "action": "please_start_new_session"
        }
    )

async def agent_execution_handler(request: Request, exc: AgentExecutionError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "agent_execution_failed",
            "message": "Our AI agent encountered an issue. Please try again.",
            "retry": True
        }
    )

# Register in FastAPI
app.add_exception_handler(SessionNotFoundError, session_not_found_handler)
app.add_exception_handler(AgentExecutionError, agent_execution_handler)
```

---

## Phase 7: Advanced Features (Week 7-8)

### 7.1 Streaming Responses

**Why**: Better UX with real-time agent responses (like ChatGPT)

**Implementation**:

```python
# MODIFY: backend/main.py

from fastapi.responses import StreamingResponse
import json

@app.post("/api/message/stream")
async def send_message_stream(request: MessageRequest):
    """Stream agent responses in real-time."""

    async def generate():
        # Get session
        state = await get_session_state(request.session_id)

        # Stream through agent
        async for chunk in stream_agent_response(state, request.message):
            yield f"data: {json.dumps(chunk)}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )

async def stream_agent_response(state: dict, message: str):
    """Stream agent response token by token."""
    from agents.story_analyst import get_story_analyst

    agent = get_story_analyst()

    async for event in agent.astream_events({"input": message}):
        if event["event"] == "on_llm_stream":
            chunk = event["data"]["chunk"]
            yield {
                "type": "token",
                "content": chunk.content,
                "phase": state["phase"]
            }
```

**Frontend Update**:

```javascript
// MODIFY: frontend/static/js/app.js

async function sendMessageWithStreaming(message) {
    const response = await fetch('/api/message/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: message,
            session_id: sessionId
        })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let assistantMessage = '';

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n\n');

        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = line.slice(6);
                if (data === '[DONE]') break;

                const event = JSON.parse(data);
                if (event.type === 'token') {
                    assistantMessage += event.content;
                    updateMessageInUI(assistantMessage); // Update in real-time
                }
            }
        }
    }
}
```

---

### 7.2 Analytics & Insights

**Implementation**:

```python
# NEW: backend/analytics/tracker.py

from sqlalchemy import func
from database.models import Session, Game

class AnalyticsTracker:
    """Track usage analytics."""

    def __init__(self, db):
        self.db = db

    async def get_stats(self) -> dict:
        """Get usage statistics."""

        total_sessions = self.db.query(Session).count()
        total_games = self.db.query(Game).count()

        games_by_type = self.db.query(
            Game.game_type,
            func.count(Game.id)
        ).group_by(Game.game_type).all()

        popular_books = self.db.query(
            Game.book_title,
            func.count(Game.id)
        ).group_by(Game.book_title).order_by(
            func.count(Game.id).desc()
        ).limit(10).all()

        return {
            "total_sessions": total_sessions,
            "total_games": total_games,
            "games_by_type": dict(games_by_type),
            "popular_books": [{"title": title, "count": count} for title, count in popular_books]
        }

# Add endpoint
@app.get("/api/analytics")
async def get_analytics(db: DBSession = Depends(get_db)):
    """Get analytics dashboard data."""
    tracker = AnalyticsTracker(db)
    return await tracker.get_stats()
```

---

## Phase 8: Deployment & Operations (Week 9)

### 8.1 Update Render Configuration

```yaml
# MODIFY: render.yaml

services:
  - type: web
    name: the-game-maker-api
    runtime: docker
    plan: starter
    branch: main
    dockerfilePath: ./Dockerfile
    envVars:
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: DATABASE_URL
        fromDatabase:
          name: gamemaker-db
          property: connectionString
      - key: REDIS_URL
        fromService:
          type: redis
          name: gamemaker-redis
          property: connectionString
      - key: LANGCHAIN_TRACING_V2
        value: true
      - key: LANGCHAIN_API_KEY
        sync: false
      - key: LANGCHAIN_PROJECT
        value: the-game-maker-production
    healthCheckPath: /api/health

  - type: pserv
    name: gamemaker-db
    plan: starter
    databaseName: gamemaker
    databaseUser: gamemaker

  - type: redis
    name: gamemaker-redis
    plan: starter
```

---

## Summary Implementation Checklist

### Week 1: Foundation
- [ ] Migrate Flask → FastAPI
- [ ] Add Docker & docker-compose
- [ ] Update dependencies
- [ ] Test all endpoints in FastAPI
- [ ] Auto-generated docs working

### Week 2: Observability
- [ ] LangSmith integration
- [ ] Prometheus metrics
- [ ] JSON logging
- [ ] Metrics dashboard

### Week 3: LangGraph
- [ ] Convert to LangGraph orchestration
- [ ] Implement state graph
- [ ] Conditional routing
- [ ] Async agent execution

### Week 4: Database
- [ ] PostgreSQL integration
- [ ] SQLAlchemy models
- [ ] Redis caching
- [ ] Database migrations

### Week 5: RAG
- [ ] Vector database setup
- [ ] Template embeddings
- [ ] Smart template selection
- [ ] Book knowledge base

### Week 6: Resilience
- [ ] Retry logic
- [ ] Fallback handlers
- [ ] Circuit breakers
- [ ] Enhanced error handling

### Week 7-8: Advanced
- [ ] Streaming responses
- [ ] Analytics tracking
- [ ] Performance optimization
- [ ] Load testing

### Week 9: Deployment
- [ ] Docker build tested
- [ ] Render deployment
- [ ] Environment configuration
- [ ] Production monitoring

---

## Environment Variables

```bash
# NEW: .env.production

# API Keys
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
LANGCHAIN_API_KEY=ls__...

# Database
DATABASE_URL=postgresql://user:password@localhost/gamemaker
REDIS_URL=redis://localhost:6379

# Observability
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_PROJECT=the-game-maker-production

# Application
FLASK_ENV=production
LOG_LEVEL=INFO
CORS_ORIGINS=https://yourdomain.com
```

---

## Testing Strategy

```python
# NEW: tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_start_session():
    response = client.post("/api/start_session", json={})
    assert response.status_code == 200
    assert "session_id" in response.json()

def test_message_endpoint():
    # Create session first
    session_resp = client.post("/api/start_session", json={})
    session_id = session_resp.json()["session_id"]

    # Send message
    response = client.post("/api/message", json={
        "message": "I read Where the Wild Things Are",
        "session_id": session_id
    })
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

---

## Migration Path

### Option A: Big Bang (2-3 weeks intensive)
All phases at once, complete rewrite

### Option B: Incremental (8-9 weeks)
Phase by phase, maintain working app

### Option C: Parallel Track (Recommended)
Keep current app running, build v2 in parallel

**Recommended: Option C**
- Maintain current functionality
- Test thoroughly before switching
- Zero downtime migration

---

## Success Metrics

Track these to measure improvement:

- **Performance**: API response time < 500ms
- **Reliability**: 99.9% uptime
- **Observability**: 100% trace coverage
- **Scalability**: Support 1000 concurrent sessions
- **Error Rate**: < 0.1% failed requests

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Render Deployment Guide](https://render.com/docs)

---

**Ready to implement? Start with Phase 1 and work incrementally!**
