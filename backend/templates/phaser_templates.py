"""
Phaser.js Game Templates

These templates are ported from the React Native mobile version.
Each template is a complete playable game that can be customized
based on the book's story elements.
"""

# HTML wrapper used by all game templates
HTML_WRAPPER = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{game_title}</title>
  <script src="https://cdn.jsdelivr.net/npm/phaser@3.70.0/dist/phaser.min.js"></script>
  <style>
    body {{
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
    #game-container {{
      max-width: 100%;
      max-height: 100vh;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      border-radius: 10px;
      overflow: hidden;
    }}
  </style>
</head>
<body>
  <div id="game-container"></div>
  <script>
    {game_code}
  </script>
</body>
</html>
"""

# Platformer Template - Jump and collect items
PLATFORMER_TEMPLATE = """
// Phaser 3 Platformer Game - {game_title}
const config = {{
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: 'game-container',
  physics: {{
    default: 'arcade',
    arcade: {{
      gravity: {{ y: 300 }},
      debug: false
    }}
  }},
  scene: {{
    preload: preload,
    create: create,
    update: update
  }}
}};

const game = new Phaser.Game(config);

let player;
let platforms;
let collectibles;
let obstacles;
let score = 0;
let scoreText;
let gameOver = false;
let cursors;

function preload() {{
  // Using simple shapes - no assets needed for MVP
}}

function create() {{
  // Create textures for game objects
  const graphics = this.add.graphics();
  
  // Platform texture
  graphics.fillStyle({platform_color}, 1);
  graphics.fillRect(0, 0, 32, 32);
  graphics.generateTexture('platform', 32, 32);
  graphics.clear();
  
  // Player texture
  graphics.fillStyle({player_color}, 1);
  graphics.fillRect(0, 0, 32, 32);
  graphics.generateTexture('player', 32, 32);
  graphics.clear();
  
  // Collectible texture
  graphics.fillStyle({collectible_color}, 1);
  graphics.fillCircle(10, 10, 10);
  graphics.generateTexture('collectible', 20, 20);
  graphics.clear();
  
  // Obstacle texture
  graphics.fillStyle({obstacle_color}, 1);
  graphics.fillRect(0, 0, 30, 30);
  graphics.generateTexture('obstacle', 30, 30);
  graphics.destroy();
  
  // Background color
  this.add.rectangle(400, 300, 800, 600, {bg_color});
  
  // Platforms
  platforms = this.physics.add.staticGroup();
  platforms.create(400, 568, 'platform').setDisplaySize(800, 32);
  platforms.create(600, 400, 'platform').setDisplaySize(200, 32);
  platforms.create(50, 250, 'platform').setDisplaySize(200, 32);
  platforms.create(750, 220, 'platform').setDisplaySize(200, 32);
  
  // Player - {player_name}
  player = this.physics.add.sprite(100, 450, 'player');
  player.setSize(32, 32);
  player.setBounce(0.2);
  player.setCollideWorldBounds(true);
  
  // Collectibles - {collectible_name}
  collectibles = this.physics.add.group();
  for (let i = 0; i < {collectible_count}; i++) {{
    const x = Phaser.Math.Between(50, 750);
    const collectible = collectibles.create(x, 0, 'collectible');
    collectible.setBounceY(Phaser.Math.FloatBetween(0.4, 0.8));
  }}
  
  // Obstacles - {obstacle_name}
  obstacles = this.physics.add.group();
  for (let i = 0; i < {obstacle_count}; i++) {{
    const x = Phaser.Math.Between(200, 700);
    const obstacle = obstacles.create(x, 500, 'obstacle');
    obstacle.setVelocityX(Phaser.Math.Between(-100, 100));
    obstacle.setBounce(1);
    obstacle.setCollideWorldBounds(true);
  }}
  
  // UI
  scoreText = this.add.text(16, 16, '{collectible_name}: 0 / {collectible_count}', {{ fontSize: '24px', fill: '#fff', backgroundColor: '#000', padding: {{ x: 10, y: 5 }} }});
  const instructions = this.add.text(400, 30, 'Arrow Keys to Move, UP to Jump', {{ fontSize: '16px', fill: '#fff', backgroundColor: '#000', padding: {{ x: 10, y: 5 }} }});
  instructions.setOrigin(0.5, 0);
  
  // Collisions
  this.physics.add.collider(player, platforms);
  this.physics.add.collider(collectibles, platforms);
  this.physics.add.collider(obstacles, platforms);
  this.physics.add.overlap(player, collectibles, collectItem, null, this);
  this.physics.add.overlap(player, obstacles, hitObstacle, null, this);
  
  // Controls
  cursors = this.input.keyboard.createCursorKeys();
}}

function update() {{
  if (gameOver) {{
    return;
  }}
  
  // Player movement
  if (cursors.left.isDown) {{
    player.setVelocityX(-160);
  }} else if (cursors.right.isDown) {{
    player.setVelocityX(160);
  }} else {{
    player.setVelocityX(0);
  }}
  
  // Jump
  if (cursors.up.isDown && player.body.touching.down) {{
    player.setVelocityY(-330);
  }}
}}

function collectItem(player, collectible) {{
  collectible.disableBody(true, true);
  score += 1;
  scoreText.setText('{collectible_name}: ' + score + ' / {collectible_count}');
  
  if (collectibles.countActive(true) === 0) {{
    showGameOver('🎉 You Win! 🎉\\n\\nYou collected all the {collectible_name}!', this);
  }}
}}

function hitObstacle(player, obstacle) {{
  this.physics.pause();
  player.setTint(0xff0000);
  gameOver = true;
  showGameOver('Game Over!\\n\\nYou hit a {obstacle_name}!', this);
}}

function showGameOver(message, scene) {{
  const bg = scene.add.rectangle(400, 300, 600, 300, 0x000000, 0.8);
  
  const text = scene.add.text(400, 260, message, {{ fontSize: '32px', fill: '#fff', align: 'center' }});
  text.setOrigin(0.5);
  
  const playAgainBtn = scene.add.text(400, 360, '🔄 Play Again', {{ fontSize: '28px', fill: '#0f0', backgroundColor: '#003300', padding: {{ x: 20, y: 10 }} }});
  playAgainBtn.setOrigin(0.5);
  playAgainBtn.setInteractive();
  playAgainBtn.on('pointerdown', () => {{
    window.location.reload();
  }});
  
  playAgainBtn.on('pointerover', () => {{
    playAgainBtn.setStyle({{ backgroundColor: '#00ff00', fill: '#000' }});
  }});
  playAgainBtn.on('pointerout', () => {{
    playAgainBtn.setStyle({{ backgroundColor: '#003300', fill: '#0f0' }});
  }});
}}
"""

# Top-Down Template - Explore and collect
TOP_DOWN_TEMPLATE = """
// Phaser 3 Top-Down Game - {game_title}
const config = {{
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: 'game-container',
  physics: {{
    default: 'arcade',
    arcade: {{
      gravity: {{ y: 0 }},
      debug: false
    }}
  }},
  scene: {{
    preload: preload,
    create: create,
    update: update
  }}
}};

const game = new Phaser.Game(config);

let player;
let collectibles;
let obstacles;
let score = 0;
let scoreText;
let timeText;
let gameTime = {game_time};
let gameOver = false;

function preload() {{
  // Using simple shapes
}}

function create() {{
  // Create textures for game objects
  const graphics = this.add.graphics();
  
  // Player texture
  graphics.fillStyle({player_color}, 1);
  graphics.fillCircle(20, 20, 20);
  graphics.generateTexture('player', 40, 40);
  graphics.clear();
  
  // Collectible texture
  graphics.fillStyle({collectible_color}, 1);
  graphics.fillCircle(10, 10, 10);
  graphics.generateTexture('collectible', 20, 20);
  graphics.clear();
  
  // Obstacle texture
  graphics.fillStyle({obstacle_color}, 1);
  graphics.fillRect(0, 0, 30, 30);
  graphics.generateTexture('obstacle', 30, 30);
  graphics.destroy();
  
  // Background
  this.add.rectangle(400, 300, 800, 600, {bg_color});
  
  // Player - {player_name}
  player = this.physics.add.sprite(400, 300, 'player');
  player.setCollideWorldBounds(true);
  
  // Collectibles - {collectible_name}
  collectibles = this.physics.add.group();
  for (let i = 0; i < {collectible_count}; i++) {{
    const x = Phaser.Math.Between(50, 750);
    const y = Phaser.Math.Between(50, 550);
    collectibles.create(x, y, 'collectible');
  }}
  
  // Obstacles - {obstacle_name}
  obstacles = this.physics.add.group();
  for (let i = 0; i < {obstacle_count}; i++) {{
    const x = Phaser.Math.Between(100, 700);
    const y = Phaser.Math.Between(100, 500);
    const obstacle = obstacles.create(x, y, 'obstacle');
    obstacle.setVelocity(Phaser.Math.Between(-50, 50), Phaser.Math.Between(-50, 50));
    obstacle.setBounce(1);
    obstacle.setCollideWorldBounds(true);
  }}
  
  // UI
  scoreText = this.add.text(16, 16, '{collectible_name}: 0', {{ fontSize: '24px', fill: '#fff', backgroundColor: '#000', padding: {{ x: 10, y: 5 }} }});
  timeText = this.add.text(16, 50, 'Time: ' + gameTime, {{ fontSize: '24px', fill: '#fff', backgroundColor: '#000', padding: {{ x: 10, y: 5 }} }});
  const instructions = this.add.text(400, 16, 'Arrow Keys to Move', {{ fontSize: '16px', fill: '#fff', backgroundColor: '#000', padding: {{ x: 10, y: 5 }} }});
  instructions.setOrigin(0.5, 0);
  
  // Collisions
  this.physics.add.overlap(player, collectibles, collectItem, null, this);
  this.physics.add.overlap(player, obstacles, hitObstacle, null, this);
  this.physics.add.collider(obstacles, obstacles);
  
  // Timer
  this.time.addEvent({{
    delay: 1000,
    callback: updateTimer,
    callbackScope: this,
    loop: true
  }});
  
  // Controls
  cursors = this.input.keyboard.createCursorKeys();
}}

function update() {{
  if (gameOver) {{
    return;
  }}
  
  // Player movement
  player.setVelocity(0);
  
  if (cursors.left.isDown) {{
    player.setVelocityX(-200);
  }} else if (cursors.right.isDown) {{
    player.setVelocityX(200);
  }}
  
  if (cursors.up.isDown) {{
    player.setVelocityY(-200);
  }} else if (cursors.down.isDown) {{
    player.setVelocityY(200);
  }}
}}

function collectItem(player, collectible) {{
  collectible.disableBody(true, true);
  score += 1;
  scoreText.setText('{collectible_name}: ' + score);
  
  if (collectibles.countActive(true) === 0) {{
    showGameOver('🎉 You Win! 🎉\\n\\nYou collected all {collectible_count} {collectible_name}!', this);
  }}
}}

function hitObstacle(player, obstacle) {{
  score = Math.max(0, score - 1);
  scoreText.setText('{collectible_name}: ' + score);
  player.setTint(0xff0000);
  this.time.delayedCall(200, () => player.clearTint());
}}

function updateTimer() {{
  if (!gameOver) {{
    gameTime--;
    timeText.setText('Time: ' + gameTime);
    
    if (gameTime <= 0) {{
      gameOver = true;
      this.physics.pause();
      showGameOver('⏰ Time Up!\\n\\nFinal Score: ' + score + ' {collectible_name}', this);
    }}
  }}
}}

function showGameOver(message, scene) {{
  const bg = scene.add.rectangle(400, 300, 600, 300, 0x000000, 0.8);
  
  const text = scene.add.text(400, 260, message, {{ fontSize: '28px', fill: '#fff', align: 'center' }});
  text.setOrigin(0.5);
  
  const playAgainBtn = scene.add.text(400, 360, '🔄 Play Again', {{ fontSize: '28px', fill: '#0f0', backgroundColor: '#003300', padding: {{ x: 20, y: 10 }} }});
  playAgainBtn.setOrigin(0.5);
  playAgainBtn.setInteractive();
  playAgainBtn.on('pointerdown', () => {{
    window.location.reload();
  }});
  
  playAgainBtn.on('pointerover', () => {{
    playAgainBtn.setStyle({{ backgroundColor: '#00ff00', fill: '#000' }});
  }});
  playAgainBtn.on('pointerout', () => {{
    playAgainBtn.setStyle({{ backgroundColor: '#003300', fill: '#0f0' }});
  }});
}}

let cursors;
"""

# Obstacle Avoider Template - Fast-paced dodging
OBSTACLE_AVOIDER_TEMPLATE = """
// Phaser 3 Obstacle Avoider - {game_title}
const config = {{
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: 'game-container',
  physics: {{
    default: 'arcade',
    arcade: {{
      gravity: {{ y: 0 }},
      debug: false
    }}
  }},
  scene: {{
    preload: preload,
    create: create,
    update: update
  }}
}};

const game = new Phaser.Game(config);

let player;
let obstacles;
let collectibles;
let score = 0;
let scoreText;
let gameOver = false;
let speed = {initial_speed};

function preload() {{
  // Using simple shapes
}}

function create() {{
  // Create textures for game objects
  const graphics = this.add.graphics();
  
  // Player texture
  graphics.fillStyle({player_color}, 1);
  graphics.fillCircle(20, 20, 20);
  graphics.generateTexture('player', 40, 40);
  graphics.clear();
  
  // Collectible texture
  graphics.fillStyle({collectible_color}, 1);
  graphics.fillCircle(12, 12, 12);
  graphics.generateTexture('collectible', 25, 25);
  graphics.clear();
  
  // Obstacle texture - will be created dynamically for different sizes
  graphics.fillStyle({obstacle_color}, 1);
  graphics.fillRect(0, 0, 30, 30);
  graphics.generateTexture('obstacle', 30, 30);
  graphics.destroy();
  
  // Background
  this.add.rectangle(400, 300, 800, 600, {bg_color});
  
  // Player - {player_name}
  player = this.physics.add.sprite(100, 300, 'player');
  player.setCollideWorldBounds(true);
  
  // Obstacles group - {obstacle_name}
  obstacles = this.physics.add.group();
  
  // Collectibles group - {collectible_name}
  collectibles = this.physics.add.group();
  
  // Score
  scoreText = this.add.text(16, 16, 'Score: 0', {{ fontSize: '32px', fill: '#fff', backgroundColor: '#000', padding: {{ x: 10, y: 5 }} }});
  const instructions = this.add.text(400, 16, 'UP/DOWN to Move', {{ fontSize: '16px', fill: '#fff', backgroundColor: '#000', padding: {{ x: 10, y: 5 }} }});
  instructions.setOrigin(0.5, 0);
  
  // Spawn obstacles
  this.time.addEvent({{
    delay: 1500,
    callback: spawnObstacle,
    callbackScope: this,
    loop: true
  }});
  
  // Spawn collectibles occasionally
  this.time.addEvent({{
    delay: 3000,
    callback: spawnCollectible,
    callbackScope: this,
    loop: true
  }});
  
  // Update score
  this.time.addEvent({{
    delay: 100,
    callback: () => {{
      if (!gameOver) {{
        score += 1;
        scoreText.setText('Score: ' + score);
        
        // Increase difficulty
        if (score % 200 === 0 && speed < 400) {{
          speed += 20;
        }}
      }}
    }},
    callbackScope: this,
    loop: true
  }});
  
  // Collisions
  this.physics.add.overlap(player, obstacles, hitObstacle, null, this);
  this.physics.add.overlap(player, collectibles, collectItem, null, this);
  
  // Controls
  cursors = this.input.keyboard.createCursorKeys();
}}

function update() {{
  if (gameOver) {{
    return;
  }}
  
  // Player movement
  if (cursors.up.isDown) {{
    player.setVelocityY(-300);
  }} else if (cursors.down.isDown) {{
    player.setVelocityY(300);
  }} else {{
    player.setVelocityY(0);
  }}
  
  // Remove off-screen objects
  obstacles.children.entries.forEach(obstacle => {{
    if (obstacle.x < -50) {{
      obstacle.destroy();
    }}
  }});
  
  collectibles.children.entries.forEach(collectible => {{
    if (collectible.x < -50) {{
      collectible.destroy();
    }}
  }});
}}

function spawnObstacle() {{
  if (gameOver) return;
  
  const y = Phaser.Math.Between(50, 550);
  const height = Phaser.Math.Between(30, 80);
  const obstacle = obstacles.create(850, y, 'obstacle').setDisplaySize(30, height);
  obstacle.setVelocityX(-speed);
}}

function spawnCollectible() {{
  if (gameOver) return;
  
  const y = Phaser.Math.Between(100, 500);
  const collectible = collectibles.create(850, y, 'collectible');
  collectible.setVelocityX(-speed);
}}

function collectItem(player, collectible) {{
  collectible.disableBody(true, true);
  score += 50;
  scoreText.setText('Score: ' + score);
  
  // Flash player green
  player.setTint(0x00ff00);
  this.time.delayedCall(200, () => player.clearTint());
}}

function hitObstacle() {{
  gameOver = true;
  this.physics.pause();
  player.setTint(0xff0000);
  
  showGameOver('Game Over!\\n\\nYou hit a {obstacle_name}!\\n\\nFinal Score: ' + score, this);
}}

function showGameOver(message, scene) {{
  const bg = scene.add.rectangle(400, 300, 600, 350, 0x000000, 0.8);
  
  const text = scene.add.text(400, 280, message, {{ fontSize: '28px', fill: '#fff', align: 'center' }});
  text.setOrigin(0.5);
  
  const playAgainBtn = scene.add.text(400, 380, '🔄 Play Again', {{ fontSize: '28px', fill: '#0f0', backgroundColor: '#003300', padding: {{ x: 20, y: 10 }} }});
  playAgainBtn.setOrigin(0.5);
  playAgainBtn.setInteractive();
  playAgainBtn.on('pointerdown', () => {{
    window.location.reload();
  }});
  
  playAgainBtn.on('pointerover', () => {{
    playAgainBtn.setStyle({{ backgroundColor: '#00ff00', fill: '#000' }});
  }});
  playAgainBtn.on('pointerout', () => {{
    playAgainBtn.setStyle({{ backgroundColor: '#003300', fill: '#0f0' }});
  }});
}}

let cursors;
"""


def get_template(game_type: str) -> str:
    """
    Get the Phaser.js template for a specific game type.
    
    Args:
        game_type: Type of game (platformer, top-down, obstacle-avoider)
    
    Returns:
        str: The game template code
    """
    templates = {
        'platformer': PLATFORMER_TEMPLATE,
        'top-down': TOP_DOWN_TEMPLATE,
        'obstacle-avoider': OBSTACLE_AVOIDER_TEMPLATE
    }
    
    return templates.get(game_type, PLATFORMER_TEMPLATE)


def generate_game_html(game_title: str, game_code: str) -> str:
    """
    Generate complete HTML with embedded game code.
    
    Args:
        game_title: Title of the game
        game_code: Complete Phaser.js game code
    
    Returns:
        str: Complete HTML document ready to play
    """
    return HTML_WRAPPER.format(
        game_title=game_title,
        game_code=game_code
    )

