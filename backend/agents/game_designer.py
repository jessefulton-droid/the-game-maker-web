"""
Game Designer Agent - The second agent in the game creation workflow.

This agent:
1. Receives book analysis from Story Analyst
2. Suggests appropriate game types
3. Collaborates with user on game mechanics
4. Designs collectibles, obstacles, and win conditions
5. Prepares complete game design for Code Generator

This demonstrates:
- Agent collaboration (receiving data from Story Analyst)
- Creative design through conversation
- Structured output for next agent
"""
import os
from typing import List, Dict, Any, Optional
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from tools.game_tools import GAME_TOOLS
from schemas.book_schema import BookAnalysis
from schemas.game_schema import GameDesign, GameMechanics, GameObject


class GameDesignerAgent:
    """
    Game Designer Agent - Collaborates on game design based on books.
    
    This agent is creative, enthusiastic about games, and helps translate
    story elements into fun, playable game mechanics.
    """
    
    def __init__(self):
        """Initialize the Game Designer agent with Claude and tools."""
        
        # Initialize Claude model
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
            temperature=0.8,  # More creative for game design
            max_tokens=4096
        )
        
        # Define the agent's personality and instructions
        self.system_prompt = """You are a friendly Game Designer AI helping create games from books.

CRITICAL - NEVER show code, JSON, or technical implementation details to users.
Only discuss game concepts, characters, collectibles, and obstacles in plain English.

COMMUNICATION STYLE - CRITICAL:
- Maximum 2 sentences per response
- Use line breaks between sentences for readability
- Be friendly but concise - no long explanations
- Get straight to the point
- NO code, NO JSON, NO technical details

GAME DESIGN FLOW:
1. Suggest 2-3 game types (platformer, top-down, or obstacle-avoider)
2. Ask what to collect (from story)
3. Ask what to avoid (from story)
4. Confirm and finalize

GAME TYPES:
- Platformer: Jump and collect
- Top-Down: Explore and collect  
- Obstacle Avoider: Dodge and survive

Keep responses SHORT and actionable. Ask one clear question at a time."""
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent with tools
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=GAME_TOOLS,
            prompt=self.prompt
        )
        
        # Create the executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=GAME_TOOLS,
            verbose=True,
            max_iterations=15,  # Increased to allow more conversation
            handle_parsing_errors=True
        )
    
    def get_initial_greeting(self, book_analysis: BookAnalysis) -> str:
        """
        Get the initial greeting for game design phase.
        
        Args:
            book_analysis: The completed book analysis from Story Analyst
        
        Returns:
            str: Enthusiastic greeting about designing the game
        """
        book_title = book_analysis.book.title
        return f"🎮 Let's design your game for '{book_title}'!\n\n" \
               f"Which type: **platformer** (jump & collect), **top-down** (explore), or **obstacle-avoider** (dodge)?"
    
    def process_message(self, user_message: str, chat_history: List[Any] = None, 
                       book_analysis: Optional[BookAnalysis] = None) -> Dict[str, Any]:
        """
        Process a user message during game design.
        
        Args:
            user_message: What the user said
            chat_history: Previous conversation messages
            book_analysis: The book analysis (for context)
        
        Returns:
            dict: Agent response with message and any extracted data
        """
        if chat_history is None:
            chat_history = []
        
        # Add book context to the input if available
        enhanced_input = user_message
        if book_analysis and len(chat_history) == 0:
            # First message - include book context
            enhanced_input = f"""Book: "{book_analysis.book.title}" by {book_analysis.book.author}
Themes: {', '.join(book_analysis.themes[:3])}
Main elements: {', '.join([e.name for e in book_analysis.game_elements[:5]])}

User says: {user_message}"""
        
        try:
            # Invoke the agent
            result = self.agent_executor.invoke({
                "input": enhanced_input,
                "chat_history": chat_history
            })
            
            # Extract text from the output (handle both string and list formats)
            output = result.get("output", "")
            
            # Handle list of content blocks (Claude's format)
            if isinstance(output, list):
                text_parts = []
                for block in output:
                    if isinstance(block, dict) and block.get('type') == 'text':
                        text_parts.append(block.get('text', ''))
                response_text = ''.join(text_parts)
            # Handle simple string output
            elif isinstance(output, str):
                response_text = output
            else:
                response_text = str(output)
            
            # Check if game type has been chosen
            game_type_chosen = self._check_for_game_type(response_text, chat_history)
            
            # Check if design is complete
            is_complete = self._check_if_complete(response_text, chat_history)
            
            return {
                "success": True,
                "message": response_text,
                "game_type_chosen": game_type_chosen,
                "is_complete": is_complete,
                "agent": "game_designer"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Hmm, I had a little trouble there. Could you say that again?"
            }
    
    def _check_for_game_type(self, response: str, history: List[Any]) -> Optional[str]:
        """Check if a game type has been chosen."""
        response_lower = response.lower()
        
        if "platformer" in response_lower:
            return "platformer"
        elif "top-down" in response_lower or "top down" in response_lower:
            return "top-down"
        elif "obstacle" in response_lower or "avoider" in response_lower or "dodg" in response_lower:
            return "obstacle-avoider"
        
        return None
    
    def _check_if_complete(self, response: str, history: List[Any]) -> bool:
        """Check if the game design is complete."""
        # After 4-6 exchanges, or if agent signals completion
        if len(history) >= 10:  # 5 exchanges
            return True
        
        completion_phrases = [
            "design is complete",
            "ready to build",
            "let's make it",
            "generate the game",
            "build your game",
            "create the code"
        ]
        
        response_lower = response.lower()
        return any(phrase in response_lower for phrase in completion_phrases)
    
    def create_game_design(self, conversation_history: List[Any], 
                          book_analysis: BookAnalysis) -> Dict[str, Any]:
        """
        Create a structured game design from the conversation.
        
        Args:
            conversation_history: All design discussion messages
            book_analysis: The book analysis for context
        
        Returns:
            dict: Structured game design
        """
        # Create a summary prompt with clear JSON structure
        summary_prompt = f"""Based on our game design conversation for "{book_analysis.book.title}", 
create a complete game design specification.

Book Context:
- Title: {book_analysis.book.title}
- Author: {book_analysis.book.author}
- Themes: {', '.join(book_analysis.themes)}
- Characters: {', '.join([c.name for c in book_analysis.characters[:3]])}

Design Conversation Summary:
{self._summarize_conversation(conversation_history)}

IMPORTANT: Return ONLY a valid JSON object with no other text, markdown, or explanations. Use this exact structure:

{{
    "game_title": "string - creative game name",
    "game_type": "platformer or top-down or obstacle-avoider",
    "book_title": "{book_analysis.book.title}",
    "theme": "string - visual theme",
    "story_premise": "string - 1-2 sentence game story",
    "mechanics": {{
        "player_movement": "string - how to control",
        "primary_action": "string - main gameplay action",
        "win_condition": "string - how to win",
        "difficulty": "easy or medium or hard"
    }},
    "player_character": {{
        "name": "string - character name from book",
        "type": "player",
        "appearance": "string - how they look",
        "behavior": "string - how they move/act",
        "story_connection": "string - connection to book"
    }},
    "collectibles": [
        {{
            "name": "string - item name from book",
            "type": "collectible",
            "appearance": "string - visual description",
            "behavior": "string - what happens when collected",
            "story_connection": "string - importance in book"
        }}
    ],
    "obstacles": [
        {{
            "name": "string - obstacle name from book",
            "type": "obstacle",
            "appearance": "string - visual description",
            "behavior": "string - what it does to player",
            "story_connection": "string - role in book story"
        }}
    ],
    "level_design": "string - description of level layout",
    "visual_style": "string - art style",
    "scoring": {{"item_collected": 10, "level_complete": 100}}
}}

Make sure collectibles and obstacles arrays have at least one item each based on the book's story."""

        try:
            # Ask the LLM to create structured design
            response = self.llm.invoke([HumanMessage(content=summary_prompt)])
            
            # Extract JSON from response (handle markdown code blocks and extra text)
            import json
            import re
            
            content = response.content
            
            # Try to extract JSON from markdown code block first
            json_match = re.search(r'```(?:json)?\s*(\{{.*?\}})\s*```', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find JSON object directly
                json_match = re.search(r'\{{.*\}}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    json_str = content
            
            design_data = json.loads(json_str)
            
            # Validate with Pydantic
            game_design = GameDesign(**design_data)
            
            return {
                "success": True,
                "design": game_design.dict()
            }
        
        except Exception as e:
            # Log the error for debugging
            print(f"ERROR in create_game_design: {str(e)}")
            if 'response' in locals():
                print(f"LLM Response: {response.content[:500]}...")
            
            # Improved fallback with actual collectibles and obstacles
            # Extract useful info from book analysis
            character_name = book_analysis.characters[0].name if book_analysis.characters else "Hero"
            theme = book_analysis.themes[0] if book_analysis.themes else "adventure"
            
            # Try to find collectibles and obstacles from game_elements
            collectible_items = []
            obstacle_items = []
            
            for element in book_analysis.game_elements[:5]:
                if any(word in element.description.lower() for word in ['collect', 'find', 'get', 'treasure', 'food', 'item']):
                    collectible_items.append(element)
                elif any(word in element.description.lower() for word in ['danger', 'avoid', 'enemy', 'bad', 'scary']):
                    obstacle_items.append(element)
            
            # Build fallback collectibles
            fallback_collectibles = []
            if collectible_items:
                for item in collectible_items[:2]:
                    fallback_collectibles.append({
                        "name": item.name,
                        "type": "collectible",
                        "appearance": f"Golden {item.name.lower()}",
                        "behavior": "Give points when collected",
                        "story_connection": item.description
                    })
            else:
                fallback_collectibles.append({
                    "name": "Story Items",
                    "type": "collectible",
                    "appearance": "Glowing golden objects",
                    "behavior": "Give points when collected",
                    "story_connection": f"Important items from {book_analysis.book.title}"
                })
            
            # Build fallback obstacles
            fallback_obstacles = []
            if obstacle_items:
                for item in obstacle_items[:2]:
                    fallback_obstacles.append({
                        "name": item.name,
                        "type": "obstacle",
                        "appearance": f"Red {item.name.lower()}",
                        "behavior": "End game on contact",
                        "story_connection": item.description
                    })
            else:
                fallback_obstacles.append({
                    "name": "Hazards",
                    "type": "obstacle",
                    "appearance": "Red dangerous objects",
                    "behavior": "End game on contact",
                    "story_connection": f"Challenges from {book_analysis.book.title}"
                })
            
            return {
                "success": True,
                "design": {
                    "game_title": f"{book_analysis.book.title} Adventure",
                    "game_type": "platformer",
                    "book_title": book_analysis.book.title,
                    "theme": f"{theme.capitalize()} themed adventure",
                    "story_premise": f"Help {character_name} collect items and avoid obstacles in this {theme} adventure!",
                    "mechanics": {
                        "player_movement": "Arrow keys to move left/right, UP to jump",
                        "primary_action": "Jump and collect items",
                        "win_condition": "Collect all items without hitting obstacles",
                        "difficulty": "medium"
                    },
                    "player_character": {
                        "name": character_name,
                        "type": "player",
                        "appearance": f"Friendly {character_name}",
                        "behavior": "Runs and jumps through the level",
                        "story_connection": f"The main character from {book_analysis.book.title}"
                    },
                    "collectibles": fallback_collectibles,
                    "obstacles": fallback_obstacles,
                    "level_design": "Multi-level platforms with items scattered throughout",
                    "visual_style": "Colorful and playful",
                    "scoring": {"item": 10, "complete": 100}
                }
            }
    
    def _summarize_conversation(self, history: List[Any]) -> str:
        """Create a summary of the design conversation."""
        messages = []
        for msg in history[-10:]:  # Last 10 messages
            if isinstance(msg, HumanMessage):
                messages.append(f"User: {msg.content}")
            elif isinstance(msg, AIMessage):
                messages.append(f"Designer: {msg.content}")
        
        return "\n".join(messages)


# Singleton instance
_game_designer_instance = None


def get_game_designer() -> GameDesignerAgent:
    """
    Get or create the singleton Game Designer agent.
    
    Returns:
        GameDesignerAgent: The initialized agent
    """
    global _game_designer_instance
    
    if _game_designer_instance is None:
        _game_designer_instance = GameDesignerAgent()
    
    return _game_designer_instance

