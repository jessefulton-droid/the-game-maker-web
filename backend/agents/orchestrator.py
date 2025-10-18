"""
Game Orchestrator - Coordinates all agents in the game creation workflow.

This orchestrator manages the state machine:
1. Identifying → User tells us what book
2. Discussing → Story Analyst discusses the book
3. Designing → Game Designer collaborates on game mechanics
4. Generating → Code Generator creates the Phaser.js game
5. Complete → Game is ready to play

This demonstrates:
- Multi-agent coordination
- State management
- Phase transitions
- Data passing between agents
"""
from typing import Dict, Any, List, Optional
from enum import Enum
from langchain_core.messages import HumanMessage, AIMessage

from agents.story_analyst import get_story_analyst
from agents.game_designer import get_game_designer
from agents.code_generator import get_code_generator
from schemas.book_schema import BookInfo, BookAnalysis
from schemas.game_schema import GameDesign


class Phase(Enum):
    """Phases in the game creation workflow."""
    IDENTIFYING = "identifying"
    DISCUSSING = "discussing"
    DESIGNING = "designing"
    GENERATING = "generating"
    COMPLETE = "complete"


class GameOrchestrator:
    """
    Orchestrates the multi-agent workflow for game creation.
    
    Manages state transitions, routes messages to appropriate agents,
    and tracks progress through the game creation process.
    """
    
    def __init__(self):
        """Initialize the orchestrator."""
        self.phase = Phase.IDENTIFYING
        self.conversation_history: List[Any] = []
        
        # Data collected through the workflow
        self.book_info: Optional[BookInfo] = None
        self.book_analysis: Optional[BookAnalysis] = None
        self.game_design: Optional[Dict] = None
        self.game_html: Optional[str] = None
        
        # Initialize agents (lazy loading)
        self._story_analyst = None
        self._game_designer = None
        self._code_generator = None
    
    @property
    def story_analyst(self):
        """Lazy load Story Analyst agent."""
        if self._story_analyst is None:
            self._story_analyst = get_story_analyst()
        return self._story_analyst
    
    @property
    def game_designer(self):
        """Lazy load Game Designer agent."""
        if self._game_designer is None:
            self._game_designer = get_game_designer()
        return self._game_designer
    
    @property
    def code_generator(self):
        """Lazy load Code Generator agent."""
        if self._code_generator is None:
            self._code_generator = get_code_generator()
        return self._code_generator
    
    def get_initial_greeting(self) -> Dict[str, Any]:
        """
        Get the initial greeting to start the conversation.
        
        Returns:
            dict: Initial message and phase
        """
        greeting = self.story_analyst.get_initial_greeting()
        
        return {
            "message": greeting,
            "phase": self.phase.value,
            "agent": "story_analyst"
        }
    
    def process_message(self, user_message: str) -> Dict[str, Any]:
        """
        Process a user message through the appropriate agent.
        
        This is the main orchestration method that:
        1. Routes message to current agent based on phase
        2. Updates conversation history
        3. Handles phase transitions
        4. Returns appropriate response
        
        Args:
            user_message: What the user said/typed
        
        Returns:
            dict: Agent response, current phase, and any generated data
        """
        # Add user message to history
        self.conversation_history.append(HumanMessage(content=user_message))
        
        # Route to appropriate agent based on phase
        if self.phase in [Phase.IDENTIFYING, Phase.DISCUSSING]:
            response = self._handle_story_phase(user_message)
        
        elif self.phase == Phase.DESIGNING:
            response = self._handle_design_phase(user_message)
        
        elif self.phase == Phase.GENERATING:
            response = self._handle_generation_phase(user_message)
        
        elif self.phase == Phase.COMPLETE:
            response = {
                "message": "Your game is ready! Would you like to play it or create another one?",
                "phase": self.phase.value,
                "is_complete": True
            }
        
        else:
            response = {
                "message": "Something went wrong. Let's start over!",
                "phase": Phase.IDENTIFYING.value
            }
        
        # Add agent response to history
        if response.get("message"):
            self.conversation_history.append(AIMessage(content=response["message"]))
        
        return response
    
    def _handle_story_phase(self, user_message: str) -> Dict[str, Any]:
        """
        Handle messages during book identification and discussion phase.
        
        Args:
            user_message: User's message
        
        Returns:
            dict: Story Analyst's response
        """
        # Process through Story Analyst
        result = self.story_analyst.process_message(
            user_message,
            self.conversation_history[:-1]  # Exclude the message we just added
        )
        
        if not result.get("success"):
            return {
                "message": result.get("message", "Sorry, I had trouble understanding. Could you try again?"),
                "phase": self.phase.value,
                "agent": "story_analyst"
            }
        
        response = {
            "message": result["message"],
            "phase": self.phase.value,
            "agent": "story_analyst"
        }
        
        # Check if we've moved from identifying to discussing
        if self.phase == Phase.IDENTIFYING and result.get("book_identified"):
            # Extract book info from the conversation
            self.book_info = self._extract_book_info(result["message"])
            self.phase = Phase.DISCUSSING
            response["phase"] = self.phase.value
            response["book_info"] = self.book_info.dict() if self.book_info else None
        
        # Check if discussion is complete
        if result.get("is_complete"):
            # Create book analysis
            if self.book_info:
                analysis_result = self.story_analyst.create_book_analysis(
                    self.conversation_history,
                    self.book_info
                )
                
                if analysis_result.get("success"):
                    self.book_analysis = BookAnalysis(**analysis_result["analysis"])
                    
                    # Transition to game design phase
                    self.phase = Phase.DESIGNING
                    response["phase"] = self.phase.value
                    
                    # Create a friendly transition message
                    book_title = self.book_info.title
                    transition_msg = (
                        f"\n\n✨ Awesome! I've learned so much about '{book_title}'!\n\n"
                        f"Now let's switch gears and design your game! 🎮"
                    )
                    
                    # Get Game Designer's initial greeting
                    design_greeting = self.game_designer.get_initial_greeting(self.book_analysis)
                    response["message"] += transition_msg + "\n\n" + design_greeting
                    response["is_complete"] = False  # Not fully complete, just transitioning
            else:
                # No book info - shouldn't happen, but handle gracefully
                response["message"] += "\n\nHmm, I need to know which book we're discussing first. What book did you read?"
                self.phase = Phase.IDENTIFYING
                response["phase"] = self.phase.value
        
        return response
    
    def _handle_design_phase(self, user_message: str) -> Dict[str, Any]:
        """
        Handle messages during game design phase using Game Designer agent.
        
        Args:
            user_message: User's message
        
        Returns:
            dict: Game Designer's response
        """
        # Get the design conversation history (exclude earlier phases)
        design_history = []
        for msg in self.conversation_history:
            # Only include messages from the design phase
            if len(design_history) > 0 or isinstance(msg, AIMessage) and "game" in msg.content.lower():
                design_history.append(msg)
        
        # Process through Game Designer agent
        result = self.game_designer.process_message(
            user_message,
            design_history[:-1],  # Exclude the message we just added
            self.book_analysis
        )
        
        if not result.get("success"):
            return {
                "message": result.get("message", "Sorry, I had trouble with that. Could you try again?"),
                "phase": self.phase.value,
                "agent": "game_designer"
            }
        
        response = {
            "message": result["message"],
            "phase": self.phase.value,
            "agent": "game_designer"
        }
        
        # Check if design is complete
        if result.get("is_complete"):
            # Create game design
            if self.book_analysis:
                design_result = self.game_designer.create_game_design(
                    self.conversation_history,
                    self.book_analysis
                )
                
                if design_result.get("success"):
                    self.game_design = design_result["design"]
                    
                    # Transition to generation phase and build immediately
                    self.phase = Phase.GENERATING
                    response["message"] += "\n\n🔨 Awesome! Now I'm going to build your game. This will take just a minute..."
                    
                    # Generate the game immediately (don't wait for another user message)
                    generation_result = self.code_generator.generate_game(self.game_design)
                    
                    if generation_result.get("success"):
                        # Store the generated HTML
                        self.game_html = generation_result["html"]
                        self.phase = Phase.COMPLETE
                        
                        game_title = generation_result.get("game_title", "Your Game")
                        
                        # Add completion message
                        response["message"] += f"\n\n🎉 '{game_title}' is ready! Your game has been generated and is ready to play!"
                        response["phase"] = self.phase.value
                        response["is_complete"] = True
                        response["game_data"] = {
                            "ready": True,
                            "game_title": game_title,
                            "game_html": self.game_html
                        }
                    else:
                        # Generation failed
                        error_message = generation_result.get("error", "Unknown error")
                        response["message"] += f"\n\n❌ Sorry, there was an error generating the game: {error_message}"
                        response["phase"] = self.phase.value
        
        return response
    
    def _handle_generation_phase(self, user_message: str) -> Dict[str, Any]:
        """
        Handle the game generation phase using Code Generator agent.
        
        Args:
            user_message: User's message (usually not needed, auto-generates)
        
        Returns:
            dict: Generation status with game HTML
        """
        if not self.game_design:
            return {
                "message": "Error: No game design available. Please start over.",
                "phase": Phase.IDENTIFYING.value,
                "agent": "code_generator"
            }
        
        # Generate the game!
        result = self.code_generator.generate_game(self.game_design)
        
        if result.get("success"):
            # Store the generated HTML
            self.game_html = result["html"]
            self.phase = Phase.COMPLETE
            
            game_title = result.get("game_title", "Your Game")
            
            return {
                "message": f"🎉 '{game_title}' is ready! Your game has been generated and is ready to play!",
                "phase": self.phase.value,
                "agent": "code_generator",
                "is_complete": True,
                "game_data": {
                    "ready": True,
                    "game_title": game_title,
                    "game_html": self.game_html
                }
            }
        else:
            error_message = result.get("error", "Unknown error")
            return {
                "message": f"Sorry, there was an error generating the game: {error_message}. Let me try again...",
                "phase": self.phase.value,
                "agent": "code_generator"
            }
    
    def _extract_book_info(self, agent_message: str) -> Optional[BookInfo]:
        """
        Extract book title and author from agent's confirmation message.
        
        Args:
            agent_message: The agent's response
        
        Returns:
            BookInfo: Extracted book information, or None if not found
        """
        import re
        
        # Try multiple patterns for flexibility
        patterns = [
            # Pattern 1: "Is that 'Title' by Author?"
            r"[Ii]s that ['\"]([^'\"]+)['\"].*?by\s+([A-Z][^?.!\n]+?)(?:[?.!]|$)",
            # Pattern 2: "talking about 'Title' by Author"
            r"talking about ['\"]([^'\"]+)['\"].*?by\s+([A-Z][^?.!\n]+?)(?:[?.!]|$)",
            # Pattern 3: "confirmed 'Title' by Author"
            r"confirmed.*?['\"]([^'\"]+)['\"].*?by\s+([A-Z][^?.!\n]+?)(?:[?.!]|$)",
            # Pattern 4: "'Title' by Author" anywhere
            r"['\"]([^'\"]{3,})['\"].*?by\s+([A-Z][a-zA-Z\s]+?)(?:[?.!,]|$)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, agent_message)
            if match:
                title = match.group(1).strip()
                author = match.group(2).strip()
                
                # Validate - make sure we captured actual book info, not junk phrases
                invalid_titles = ["re talking about", "m so", "ve confirmed", "s that", "t that"]
                if (len(title) > 2 and len(author) > 2 and 
                    not any(invalid in title.lower() for invalid in invalid_titles)):
                    return BookInfo(
                        title=title,
                        author=author,
                        summary=f"A wonderful book by {author}"
                    )
        
        # No valid match found - return None instead of fallback
        # This will be handled by the orchestrator
        return None
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get the current state of the orchestrator.
        
        Returns:
            dict: Current phase, book info, conversation history, etc.
        """
        return {
            "phase": self.phase.value,
            "book_info": self.book_info.dict() if self.book_info else None,
            "book_analysis": self.book_analysis.dict() if self.book_analysis else None,
            "game_design": self.game_design,
            "game_html": self.game_html,
            "conversation_history": [
                {
                    "role": "user" if isinstance(msg, HumanMessage) else "agent",
                    "content": msg.content
                }
                for msg in self.conversation_history
            ],
            "message_count": len(self.conversation_history)
        }

