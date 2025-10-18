"""
Tools for the Game Designer agent to create game designs.
These tools help translate book elements into game mechanics.
"""
from langchain.tools import tool
from typing import Dict, Any
import json


@tool
def suggest_game_type(book_theme: str, story_elements: str) -> str:
    """
    Suggest appropriate game types based on the book's theme and elements.
    
    Args:
        book_theme: The main theme or tone of the book
        story_elements: Key story elements (characters, plot, setting)
    
    Returns:
        JSON string with suggested game types and reasoning
    """
    result = {
        "action": "suggest_game_types",
        "suggestions": [
            {
                "type": "platformer",
                "description": "Jump and collect items while avoiding obstacles",
                "good_for": "Adventure stories, journeys, overcoming challenges"
            },
            {
                "type": "top-down",
                "description": "Navigate from above, explore and collect",
                "good_for": "Exploration stories, quests, finding things"
            },
            {
                "type": "obstacle-avoider",
                "description": "Fast-paced dodging and collecting",
                "good_for": "Action stories, chase scenes, escape themes"
            }
        ],
        "recommendation": "Based on the theme, I'll help you choose!"
    }
    
    return json.dumps(result)


@tool
def brainstorm_collectibles(story_elements: str) -> str:
    """
    Generate ideas for collectible items based on story elements.
    
    Args:
        story_elements: Important items, themes, or objects from the story
    
    Returns:
        JSON string with collectible suggestions
    """
    result = {
        "action": "brainstorm_collectibles",
        "message": "Let's think about what the player should collect!",
        "awaiting_response": True
    }
    
    return json.dumps(result)


@tool
def design_obstacles(story_challenges: str) -> str:
    """
    Create obstacle ideas based on challenges in the story.
    
    Args:
        story_challenges: Conflicts, antagonists, or dangers from the story
    
    Returns:
        JSON string with obstacle suggestions
    """
    result = {
        "action": "design_obstacles",
        "message": "What should the player avoid or overcome?",
        "awaiting_response": True
    }
    
    return json.dumps(result)


@tool
def set_difficulty_level(target_age: str, user_preference: str) -> str:
    """
    Determine appropriate difficulty based on age and preference.
    
    Args:
        target_age: Age range of the player
        user_preference: User's stated difficulty preference (easy/medium/hard)
    
    Returns:
        JSON string with difficulty settings
    """
    result = {
        "action": "set_difficulty",
        "difficulty": user_preference or "medium",
        "message": f"Setting difficulty to {user_preference or 'medium'} for age {target_age}"
    }
    
    return json.dumps(result)


@tool
def define_win_condition(game_type: str, collectible: str, story_goal: str) -> str:
    """
    Define how the player wins the game.
    
    Args:
        game_type: Type of game (platformer, top-down, obstacle-avoider)
        collectible: What the player collects
        story_goal: The goal or resolution from the story
    
    Returns:
        JSON string with win condition
    """
    result = {
        "action": "define_win_condition",
        "win_condition": f"Collect enough {collectible} to achieve: {story_goal}",
        "message": "The player wins when they complete this goal!"
    }
    
    return json.dumps(result)


@tool
def finalize_game_design(design_summary: str) -> str:
    """
    Signal that game design is complete and ready for code generation.
    
    Args:
        design_summary: Complete summary of the game design
    
    Returns:
        JSON string with finalization status
    """
    result = {
        "action": "finalize_design",
        "status": "ready_for_code_generation",
        "summary": design_summary,
        "next_phase": "generating"
    }
    
    return json.dumps(result)


@tool
def ask_design_question(aspect: str, question_text: str) -> str:
    """
    Ask the user a specific question about game design.
    
    Args:
        aspect: What aspect of design (mechanics, visuals, difficulty, etc.)
        question_text: The specific question to ask
    
    Returns:
        JSON string indicating question was asked
    """
    result = {
        "action": "ask_question",
        "aspect": aspect,
        "question": question_text,
        "awaiting_response": True
    }
    
    return json.dumps(result)


# Export all tools as a list
GAME_TOOLS = [
    suggest_game_type,
    brainstorm_collectibles,
    design_obstacles,
    set_difficulty_level,
    define_win_condition,
    finalize_game_design,
    ask_design_question
]

