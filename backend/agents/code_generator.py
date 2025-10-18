"""
Code Generator Agent - The final agent in the game creation workflow.

This agent:
1. Receives game design from Game Designer
2. Selects appropriate Phaser.js template
3. Customizes the template with story elements
4. Generates complete, playable HTML game
5. Returns ready-to-play game code

This demonstrates:
- Code generation from specifications
- Template customization
- Final product assembly
"""
import os
from typing import Dict, Any
from templates.phaser_templates import get_template, generate_game_html
from schemas.game_schema import GameDesign


class CodeGeneratorAgent:
    """
    Code Generator Agent - Creates playable Phaser.js games.
    
    This agent takes a game design and generates complete, working
    game code that can be played immediately in a browser.
    """
    
    def __init__(self):
        """Initialize the Code Generator agent."""
        pass
    
    def generate_game(self, game_design: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete game from the design specification.
        
        Args:
            game_design: Complete game design from Game Designer
        
        Returns:
            dict: Generated game code and HTML
        """
        try:
            # Extract design details
            game_title = game_design.get('game_title', 'My Game')
            game_type = game_design.get('game_type', 'platformer')
            book_title = game_design.get('book_title', 'Story')
            
            # Get player, collectibles, obstacles
            player = game_design.get('player_character', {})
            collectibles = game_design.get('collectibles', [])
            obstacles = game_design.get('obstacles', [])
            
            # Get template
            template = get_template(game_type)
            
            # Customize based on game type
            if game_type == 'platformer':
                customized_code = self._customize_platformer(
                    template, game_title, player, collectibles, obstacles, game_design
                )
            elif game_type == 'top-down':
                customized_code = self._customize_top_down(
                    template, game_title, player, collectibles, obstacles, game_design
                )
            elif game_type == 'obstacle-avoider':
                customized_code = self._customize_avoider(
                    template, game_title, player, collectibles, obstacles, game_design
                )
            else:
                # Default to platformer
                customized_code = self._customize_platformer(
                    template, game_title, player, collectibles, obstacles, game_design
                )
            
            # Generate complete HTML
            game_html = generate_game_html(game_title, customized_code)
            
            return {
                "success": True,
                "code": customized_code,
                "html": game_html,
                "game_title": game_title
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _customize_platformer(self, template: str, game_title: str, 
                            player: Dict, collectibles: list, obstacles: list,
                            game_design: Dict) -> str:
        """Customize platformer template with story elements."""
        
        # Extract names
        player_name = player.get('name', 'Hero') if player else 'Hero'
        collectible_name = collectibles[0].get('name', 'Items') if collectibles else 'Items'
        obstacle_name = obstacles[0].get('name', 'Danger') if obstacles else 'Obstacles'
        
        # Customize template
        customized = template.format(
            game_title=game_title,
            player_name=player_name,
            collectible_name=collectible_name,
            obstacle_name=obstacle_name,
            collectible_count=8,
            obstacle_count=3,
            # Colors (using hex without 0x prefix for format string)
            bg_color='0x87CEEB',  # Sky blue
            platform_color='0x8B4513',  # Brown
            player_color='0x00FF00',  # Green
            collectible_color='0xFFD700',  # Gold
            obstacle_color='0xFF0000'  # Red
        )
        
        return customized
    
    def _customize_top_down(self, template: str, game_title: str,
                          player: Dict, collectibles: list, obstacles: list,
                          game_design: Dict) -> str:
        """Customize top-down template with story elements."""
        
        player_name = player.get('name', 'Hero') if player else 'Hero'
        collectible_name = collectibles[0].get('name', 'Items') if collectibles else 'Items'
        obstacle_name = obstacles[0].get('name', 'Danger') if obstacles else 'Obstacles'
        
        customized = template.format(
            game_title=game_title,
            player_name=player_name,
            collectible_name=collectible_name,
            obstacle_name=obstacle_name,
            collectible_count=15,
            obstacle_count=5,
            game_time=60,
            # Colors
            bg_color='0x228B22',  # Forest green
            player_color='0x00FF00',  # Green
            collectible_color='0xFFD700',  # Gold
            obstacle_color='0x800080'  # Purple
        )
        
        return customized
    
    def _customize_avoider(self, template: str, game_title: str,
                         player: Dict, collectibles: list, obstacles: list,
                         game_design: Dict) -> str:
        """Customize obstacle avoider template with story elements."""
        
        player_name = player.get('name', 'Hero') if player else 'Hero'
        collectible_name = collectibles[0].get('name', 'Items') if collectibles else 'Items'
        obstacle_name = obstacles[0].get('name', 'Danger') if obstacles else 'Obstacles'
        
        customized = template.format(
            game_title=game_title,
            player_name=player_name,
            collectible_name=collectible_name,
            obstacle_name=obstacle_name,
            initial_speed=200,
            # Colors
            bg_color='0x1E90FF',  # Dodger blue
            player_color='0x00FF00',  # Green
            collectible_color='0xFFD700',  # Gold
            obstacle_color='0xFF0000'  # Red
        )
        
        return customized


# Singleton instance
_code_generator_instance = None


def get_code_generator() -> CodeGeneratorAgent:
    """
    Get or create the singleton Code Generator agent.
    
    Returns:
        CodeGeneratorAgent: The initialized agent
    """
    global _code_generator_instance
    
    if _code_generator_instance is None:
        _code_generator_instance = CodeGeneratorAgent()
    
    return _code_generator_instance

