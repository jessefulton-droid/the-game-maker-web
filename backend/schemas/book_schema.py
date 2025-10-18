"""
Book-related Pydantic schemas for data validation.
These schemas ensure type safety when passing data between agents.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class BookInfo(BaseModel):
    """Basic information about a book."""
    title: str = Field(..., description="The title of the book")
    author: str = Field(..., description="The author of the book")
    summary: Optional[str] = Field(None, description="Brief summary of the book")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Dragons Love Tacos",
                "author": "Adam Rubin",
                "summary": "Dragons love tacos but hate spicy salsa"
            }
        }


class Character(BaseModel):
    """A character from the book."""
    name: str = Field(..., description="Character name")
    description: str = Field(..., description="Brief character description")
    role: str = Field(..., description="Role in the story (protagonist, antagonist, supporting)")
    traits: List[str] = Field(default_factory=list, description="Character traits and qualities")


class GameElement(BaseModel):
    """Story element that could become a game mechanic."""
    element_type: str = Field(..., description="Type: collectible, obstacle, power-up, character")
    name: str = Field(..., description="Name of the element")
    description: str = Field(..., description="How it appears in the story")
    game_potential: str = Field(..., description="How this could work in a game")


class BookAnalysis(BaseModel):
    """Complete analysis of a book for game creation."""
    book: BookInfo
    plot_summary: str = Field(..., description="Summary of the main plot")
    setting: str = Field(..., description="Where the story takes place")
    themes: List[str] = Field(..., description="Main themes of the story")
    characters: List[Character] = Field(..., description="Key characters")
    game_elements: List[GameElement] = Field(..., description="Elements that could become game mechanics")
    tone: str = Field(..., description="Overall tone: funny, adventurous, mysterious, etc.")
    target_age: str = Field(default="5-10", description="Target age range")
    
    class Config:
        json_schema_extra = {
            "example": {
                "book": {
                    "title": "Dragons Love Tacos",
                    "author": "Adam Rubin",
                    "summary": "Dragons love tacos but hate spicy salsa"
                },
                "plot_summary": "Dragons love all kinds of tacos, but spicy salsa gives them the worst tummy troubles.",
                "setting": "A whimsical world with dragons and taco parties",
                "themes": ["friendship", "food", "humor", "consequences"],
                "characters": [
                    {
                        "name": "Dragons",
                        "description": "Taco-loving creatures",
                        "role": "protagonist",
                        "traits": ["friendly", "food-loving", "sensitive to spice"]
                    }
                ],
                "game_elements": [
                    {
                        "element_type": "collectible",
                        "name": "Tacos",
                        "description": "Dragons' favorite food",
                        "game_potential": "Collect tacos to score points"
                    },
                    {
                        "element_type": "obstacle",
                        "name": "Spicy Salsa",
                        "description": "Makes dragons sick",
                        "game_potential": "Avoid spicy salsa or lose health"
                    }
                ],
                "tone": "funny and lighthearted",
                "target_age": "4-8"
            }
        }

