"""
Story Analyst Agent - The first agent in the game creation workflow.

This agent:
1. Asks what book the user read
2. Identifies the book title and author through conversation
3. Discusses the book to understand plot, characters, themes
4. Extracts elements that could become game mechanics
5. Prepares a complete book analysis for the Game Designer agent

This demonstrates key LangChain patterns:
- Agent creation with system prompts
- Tool registration and usage
- Conversation history management
- Structured output with Pydantic schemas
"""
import os
from typing import List, Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from tools.book_tools import BOOK_TOOLS
from schemas.book_schema import BookAnalysis, BookInfo


class StoryAnalystAgent:
    """
    Story Analyst Agent - Identifies and discusses children's books.
    
    This agent is friendly, encouraging, and asks thoughtful questions
    to understand the book deeply enough to create a great game.
    """
    
    def __init__(self):
        """Initialize the Story Analyst agent with Claude and tools."""
        
        # Get API key and verify it's loaded
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        # Debug: Log key info (first/last chars only for security)
        print(f"[StoryAnalyst] Initializing with API key: {api_key[:15]}...{api_key[-10:]} (length: {len(api_key)})")
        
        # Initialize Claude model
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            anthropic_api_key=api_key,
            temperature=0.7,  # Slightly creative but focused
            max_tokens=4096
        )
        
        # Define the agent's personality and instructions
        self.system_prompt = """You are a friendly and enthusiastic Story Analyst AI who loves children's books!

Your job is to:
1. Ask the user what book they read (be warm and excited!)
2. When they tell you, identify the specific title and author
3. Confirm the book with them CLEARLY: "Is that '[EXACT TITLE]' by [AUTHOR NAME]?" - Use this exact format!
4. Once confirmed, have a fun conversation about the book
5. Ask questions to understand: plot, characters, setting, themes, and exciting moments
6. Think about what elements could become fun game mechanics
7. After 5-7 exchanges, you'll have enough info to move to game design

IMPORTANT - BOOK CONFIRMATION FORMAT:
When confirming a book, ALWAYS use this format:
"Is that '[BOOK TITLE]' by [AUTHOR NAME]?"
Example: "Is that 'Where the Wild Things Are' by Maurice Sendak?"

IMPORTANT VOICE AND TONE:
- Be enthusiastic and encouraging, like talking to a friend
- Use simple language appropriate for kids
- Ask one question at a time (don't overwhelm)
- Show genuine interest in what they say
- Celebrate their answers: example - "That's so cool!" "I love that part too!"
- Make them feel proud of their reading
- Keep your conversation turns friendly and engaging, but not too chatty. Kids don't want to read your long responses
- Break up your responses into short, concise sentences. Kids don't want to read your long responses
- Don't respond with long paragraphs. Kids don't want to read your long responses
- Use emojis to make your responses more engaging. Kids love emojis!

CONVERSATION FLOW:
1. Start: "Hi! I'm so excited to help you create a game! What book did you just read?"
2. Identify: When they respond, identify the book and confirm using the format above
3. Discuss: Ask about favorite parts, characters, what happens, themes
4. Extract: Think about collectibles (items from the story), obstacles (challenges), character traits
5. Complete: When you have enough, thank them and signal you're ready to design

Remember: You're setting the stage for creating an amazing game based on their book!"""
        
        # Create the prompt template with message placeholders
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent with tools
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=BOOK_TOOLS,
            prompt=self.prompt
        )
        
        # Create the executor that will run the agent
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=BOOK_TOOLS,
            verbose=True,  # Helpful for debugging
            max_iterations=15,  # Increased to allow more conversation
            handle_parsing_errors=True
        )
    
    def get_initial_greeting(self) -> str:
        """
        Get the initial greeting message.
        
        Returns:
            str: Warm greeting asking about the book
        """
        return "Hi! I'm so excited to help you create a game! What book did you just read?"
    
    def process_message(self, user_message: str, chat_history: List[Any] = None) -> Dict[str, Any]:
        """
        Process a user message and return the agent's response.
        
        Args:
            user_message: What the user said
            chat_history: Previous conversation messages
        
        Returns:
            dict: Agent response with message and any extracted data
        """
        if chat_history is None:
            chat_history = []
        
        try:
            # Invoke the agent
            result = self.agent_executor.invoke({
                "input": user_message,
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
            
            # Check if we've identified a book
            book_identified = self._check_for_book_identification(response_text, chat_history)
            
            # Check if analysis is complete
            is_complete = self._check_if_complete(response_text, chat_history)
            
            return {
                "success": True,
                "message": response_text,
                "book_identified": book_identified,
                "is_complete": is_complete,
                "agent": "story_analyst"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "I had a little trouble there. Could you say that again?"
            }
    
    def _check_for_book_identification(self, response: str, history: List[Any]) -> bool:
        """Check if a book has been identified and confirmed."""
        # Look for confirmation language
        confirmation_phrases = [
            "is that",
            "by",
            "that's the book",
            "confirmed"
        ]
        
        response_lower = response.lower()
        return any(phrase in response_lower for phrase in confirmation_phrases)
    
    def _check_if_complete(self, response: str, history: List[Any]) -> bool:
        """Check if the book analysis is complete."""
        # After 5-7 exchanges, or if agent signals completion
        if len(history) >= 12:  # 6 exchanges (user + agent)
            return True
        
        completion_phrases = [
            "enough information",
            "ready to design",
            "let's design",
            "create the game",
            "game design"
        ]
        
        response_lower = response.lower()
        return any(phrase in response_lower for phrase in completion_phrases)
    
    def create_book_analysis(self, conversation_history: List[Any], book_info: BookInfo) -> Dict[str, Any]:
        """
        Create a structured book analysis from the conversation.
        
        This uses the LLM to analyze the entire conversation and extract
        structured information according to the BookAnalysis schema.
        
        Args:
            conversation_history: All messages exchanged
            book_info: Basic book information (title, author)
        
        Returns:
            dict: Structured book analysis
        """
        # Create a summary prompt
        summary_prompt = f"""Based on our conversation about "{book_info.title}" by {book_info.author}, 
please create a structured analysis for game design.

Extract and format the following (in JSON):
- plot_summary: Brief plot summary (2-3 sentences)
- setting: Where the story takes place
- themes: List of main themes (friendship, courage, etc.)
- characters: List of main characters with names, descriptions, roles, and traits
- game_elements: Story elements that could become game mechanics (collectibles, obstacles, etc.)
- tone: Overall tone (funny, adventurous, etc.)
- target_age: Age range this book is for

Conversation summary:
{self._summarize_conversation(conversation_history)}

Return ONLY valid JSON matching this structure, no other text."""

        try:
            # Ask the LLM to create structured analysis
            response = self.llm.invoke([HumanMessage(content=summary_prompt)])
            
            # Parse the response
            import json
            analysis_data = json.loads(response.content)
            
            # Add book info
            analysis_data['book'] = book_info.dict()
            
            # Validate with Pydantic
            book_analysis = BookAnalysis(**analysis_data)
            
            return {
                "success": True,
                "analysis": book_analysis.dict()
            }
        
        except Exception as e:
            # Fallback to a basic analysis
            return {
                "success": True,
                "analysis": {
                    "book": book_info.dict(),
                    "plot_summary": "A wonderful story to turn into a game!",
                    "setting": "A magical world",
                    "themes": ["adventure", "friendship"],
                    "characters": [],
                    "game_elements": [],
                    "tone": "fun and engaging",
                    "target_age": "5-10"
                }
            }
    
    def _summarize_conversation(self, history: List[Any]) -> str:
        """Create a summary of the conversation for analysis."""
        messages = []
        for msg in history:
            if isinstance(msg, HumanMessage):
                messages.append(f"User: {msg.content}")
            elif isinstance(msg, AIMessage):
                messages.append(f"Agent: {msg.content}")
        
        return "\n".join(messages)


# Singleton instance
_story_analyst_instance = None


def get_story_analyst() -> StoryAnalystAgent:
    """
    Get or create the singleton Story Analyst agent.
    
    Returns:
        StoryAnalystAgent: The initialized agent
    """
    global _story_analyst_instance
    
    if _story_analyst_instance is None:
        _story_analyst_instance = StoryAnalystAgent()
    
    return _story_analyst_instance

