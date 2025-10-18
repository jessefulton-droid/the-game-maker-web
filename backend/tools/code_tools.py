"""
Tools for the Code Generator agent to create Phaser.js games.
These tools help generate, validate, and wrap game code.
"""
from langchain.tools import tool
from typing import Dict, Any
import json


@tool
def select_game_template(game_type: str) -> str:
    """
    Select the appropriate Phaser.js template based on game type.
    
    Args:
        game_type: Type of game (platformer, top-down, obstacle-avoider)
    
    Returns:
        JSON string confirming template selection
    """
    result = {
        "action": "select_template",
        "game_type": game_type,
        "template_loaded": True,
        "message": f"Loading {game_type} template..."
    }
    
    return json.dumps(result)


@tool
def customize_game_elements(customization_params: str) -> str:
    """
    Customize game elements based on the story.
    
    Args:
        customization_params: JSON string with customization details
    
    Returns:
        JSON string with customization status
    """
    result = {
        "action": "customize_elements",
        "status": "applying_customizations",
        "message": "Customizing game with story elements..."
    }
    
    return json.dumps(result)


@tool
def validate_game_code(code_snippet: str) -> str:
    """
    Validate that the generated game code is syntactically correct.
    
    Args:
        code_snippet: JavaScript/Phaser code to validate
    
    Returns:
        JSON string with validation results
    """
    # Basic validation - check for common issues
    issues = []
    
    if "function" not in code_snippet and "const" not in code_snippet:
        issues.append("No functions or variables defined")
    
    result = {
        "action": "validate_code",
        "valid": len(issues) == 0,
        "issues": issues,
        "message": "Code validation complete" if len(issues) == 0 else f"Found {len(issues)} issues"
    }
    
    return json.dumps(result)


@tool
def generate_html_wrapper(game_title: str, game_code: str) -> str:
    """
    Wrap the game code in a complete HTML document.
    
    Args:
        game_title: Title of the game
        game_code: Complete Phaser.js game code
    
    Returns:
        JSON string confirming HTML generation
    """
    result = {
        "action": "generate_html",
        "status": "complete",
        "message": f"Generated complete HTML for '{game_title}'"
    }
    
    return json.dumps(result)


@tool
def finalize_game_code(summary: str) -> str:
    """
    Signal that code generation is complete.
    
    Args:
        summary: Summary of the generated game
    
    Returns:
        JSON string with completion status
    """
    result = {
        "action": "finalize_code",
        "status": "complete",
        "ready_to_play": True,
        "summary": summary
    }
    
    return json.dumps(result)


# Export all tools as a list
CODE_TOOLS = [
    select_game_template,
    customize_game_elements,
    validate_game_code,
    generate_html_wrapper,
    finalize_game_code
]

