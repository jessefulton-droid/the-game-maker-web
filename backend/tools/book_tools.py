"""
Tools for the Story Analyst agent to identify and analyze books.
These tools are callable by the LangChain agent during conversation.
"""
from langchain.tools import tool
from typing import Dict, Any
import json


@tool
def identify_book_from_description(description: str) -> str:
    """
    Extract book title and author from user's description.
    
    This tool analyzes what the user says about a book and tries to identify
    the specific title and author. It returns structured data that can be
    confirmed with the user.
    
    Args:
        description: What the user said about the book (e.g., "Dragons Love Tacos")
    
    Returns:
        JSON string with title, author, and confidence level
    """
    # In a real implementation, this could query a book database or API
    # For now, we'll use the LLM's knowledge to identify books
    
    # The LLM will populate this based on its knowledge
    result = {
        "identified": True,
        "needs_confirmation": True,
        "message": f"Based on '{description}', I need to identify the specific book."
    }
    
    return json.dumps(result)


@tool
def confirm_book_identification(title: str, author: str, user_confirmed: bool) -> str:
    """
    Record user's confirmation of book identification.
    
    Args:
        title: The book title we identified
        author: The author we identified
        user_confirmed: Whether the user confirmed this is correct
    
    Returns:
        JSON string with confirmation status
    """
    result = {
        "confirmed": user_confirmed,
        "book": {
            "title": title,
            "author": author
        }
    }
    
    if user_confirmed:
        result["message"] = f"Great! I've confirmed we're talking about '{title}' by {author}."
        result["next_step"] = "begin_discussion"
    else:
        result["message"] = "Let me try again. Can you tell me more about the book?"
        result["next_step"] = "retry_identification"
    
    return json.dumps(result)


@tool
def extract_story_themes(discussion_text: str) -> str:
    """
    Extract themes from the book discussion.
    
    Analyzes the conversation to identify key themes like friendship, adventure,
    courage, etc. that could inform game design.
    
    Args:
        discussion_text: Summary of what's been discussed about the book
    
    Returns:
        JSON string with identified themes
    """
    # The LLM will analyze the discussion and extract themes
    result = {
        "action": "analyze_themes",
        "input": discussion_text
    }
    
    return json.dumps(result)


@tool
def extract_characters(discussion_text: str) -> str:
    """
    Extract main characters from the book discussion.
    
    Identifies key characters, their traits, and roles in the story.
    This helps create appropriate player characters and NPCs for the game.
    
    Args:
        discussion_text: Summary of what's been discussed about characters
    
    Returns:
        JSON string with character information
    """
    result = {
        "action": "analyze_characters",
        "input": discussion_text
    }
    
    return json.dumps(result)


@tool
def extract_game_elements(discussion_text: str) -> str:
    """
    Identify story elements that could become game mechanics.
    
    Looks for things in the story that could be collectibles, obstacles,
    power-ups, or other game elements.
    
    Args:
        discussion_text: Summary of the book discussion
    
    Returns:
        JSON string with potential game elements
    """
    result = {
        "action": "identify_game_elements",
        "input": discussion_text
    }
    
    return json.dumps(result)


@tool
def ask_follow_up_question(topic: str, question_text: str) -> str:
    """
    Ask the user a follow-up question to deepen understanding.
    
    Used by the agent to ask specific questions about the story to gather
    more information for game design.
    
    Args:
        topic: What aspect of the story (plot, characters, setting, etc.)
        question_text: The specific question to ask
    
    Returns:
        JSON string indicating the question was asked
    """
    result = {
        "action": "ask_question",
        "topic": topic,
        "question": question_text,
        "awaiting_response": True
    }
    
    return json.dumps(result)


@tool
def complete_book_analysis(analysis_summary: str) -> str:
    """
    Signal that book discussion is complete and analysis is ready.
    
    Called when the agent has gathered enough information to move to
    game design phase.
    
    Args:
        analysis_summary: Summary of the book analysis
    
    Returns:
        JSON string with completion status
    """
    result = {
        "action": "complete_analysis",
        "status": "ready_for_game_design",
        "summary": analysis_summary
    }
    
    return json.dumps(result)


# Export all tools as a list for easy registration
BOOK_TOOLS = [
    identify_book_from_description,
    confirm_book_identification,
    extract_story_themes,
    extract_characters,
    extract_game_elements,
    ask_follow_up_question,
    complete_book_analysis
]

