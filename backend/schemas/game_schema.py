"""
Game design Pydantic schemas for data validation.
These schemas define the structure of game designs passed between agents.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class GameMechanics(BaseModel):
    """Core game mechanics and rules."""
    player_movement: str = Field(..., description="How the player moves: keyboard, mouse, touch")
    primary_action: str = Field(..., description="Main player action: jump, shoot, collect, avoid")
    win_condition: str = Field(..., description="How to win the game")
    lose_condition: Optional[str] = Field(None, description="How to lose (if applicable)")
    difficulty: str = Field(default="medium", description="easy, medium, or hard")


class GameObject(BaseModel):
    """An object in the game world."""
    name: str = Field(..., description="Object name")
    type: str = Field(..., description="collectible, obstacle, enemy, platform, power-up")
    appearance: str = Field(..., description="Visual description")
    behavior: str = Field(..., description="How it behaves or affects gameplay")
    story_connection: str = Field(..., description="Connection to the original book")


class GameDesign(BaseModel):
    """Complete game design specification."""
    game_title: str = Field(..., description="Title of the game")
    game_type: str = Field(..., description="platformer, top-down, obstacle-avoider")
    book_title: str = Field(..., description="Source book title")
    
    theme: str = Field(..., description="Visual and narrative theme")
    story_premise: str = Field(..., description="Game story in 1-2 sentences")
    
    mechanics: GameMechanics
    
    player_character: GameObject = Field(..., description="The player character")
    collectibles: List[GameObject] = Field(..., description="Things to collect")
    obstacles: List[GameObject] = Field(..., description="Things to avoid")
    enemies: Optional[List[GameObject]] = Field(default_factory=list, description="Enemy characters")
    power_ups: Optional[List[GameObject]] = Field(default_factory=list, description="Power-ups")
    
    level_design: str = Field(..., description="Description of the level layout")
    visual_style: str = Field(..., description="Art style: colorful, retro, minimalist, etc.")
    
    scoring: Dict[str, int] = Field(..., description="Points for different actions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "game_title": "Dragon Taco Adventure",
                "game_type": "platformer",
                "book_title": "Dragons Love Tacos",
                "theme": "Colorful taco party with friendly dragons",
                "story_premise": "Help the dragon collect tacos for the big party while avoiding spicy salsa!",
                "mechanics": {
                    "player_movement": "Arrow keys to move left/right, spacebar to jump",
                    "primary_action": "jump and collect",
                    "win_condition": "Collect 50 tacos",
                    "lose_condition": "Touch 3 spicy salsas",
                    "difficulty": "medium"
                },
                "player_character": {
                    "name": "Friendly Dragon",
                    "type": "player",
                    "appearance": "Green dragon with big smile",
                    "behavior": "Runs and jumps",
                    "story_connection": "The taco-loving dragon from the book"
                },
                "collectibles": [
                    {
                        "name": "Tacos",
                        "type": "collectible",
                        "appearance": "Golden tacos",
                        "behavior": "Give points when collected",
                        "story_connection": "Dragons' favorite food"
                    }
                ],
                "obstacles": [
                    {
                        "name": "Spicy Salsa",
                        "type": "obstacle",
                        "appearance": "Red hot sauce bottles",
                        "behavior": "Hurt player on contact",
                        "story_connection": "What dragons must avoid"
                    }
                ],
                "enemies": [],
                "power_ups": [],
                "level_design": "Platforms at different heights with tacos scattered throughout",
                "visual_style": "Bright, colorful, cartoon style",
                "scoring": {
                    "taco": 10,
                    "complete_level": 100
                }
            }
        }


class GameCode(BaseModel):
    """Generated game code and assets."""
    game_design_id: str = Field(..., description="Reference to the game design")
    phaser_code: str = Field(..., description="Complete Phaser.js game code")
    html_wrapper: str = Field(..., description="HTML file wrapping the game")
    css_styles: Optional[str] = Field(None, description="Additional CSS if needed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "game_design_id": "dragon-taco-adventure-001",
                "phaser_code": "// Phaser.js game code here",
                "html_wrapper": "<!DOCTYPE html><html>...</html>",
                "css_styles": "body { margin: 0; }"
            }
        }

