"""
The Game Maker - Flask Backend
A web application that transforms children's books into playable arcade games using AI agents.
"""
import os
from datetime import timedelta
from flask import Flask, jsonify, request, session, render_template
from flask_cors import CORS
from flask_session import Session
from dotenv import load_dotenv

# Load environment variables
# Load from project root (parent directory of backend/)
import pathlib
env_path = pathlib.Path(__file__).parent.parent / '.env'
load_dotenv(env_path)
# Also try loading from current directory as fallback
load_dotenv()

# Initialize Flask app
app = Flask(__name__,
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# Configuration
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# Initialize extensions
CORS(app)
Session(app)

# Store active sessions (in production, use Redis or database)
active_sessions = {}


@app.route('/')
def index():
    """Serve the main application page."""
    return render_template('index.html')


@app.route('/game')
def game():
    """Serve the game player page."""
    return render_template('game.html')


@app.route('/api/start_session', methods=['POST'])
def start_session():
    """
    Initialize a new game creation session.
    
    Returns:
        dict: Session ID and initial agent greeting
    """
    from agents.orchestrator import GameOrchestrator
    
    # Create new session
    session_id = os.urandom(16).hex()
    
    # Initialize orchestrator
    orchestrator = GameOrchestrator()
    active_sessions[session_id] = orchestrator
    
    # Get initial greeting
    greeting = orchestrator.get_initial_greeting()
    
    # Store session ID
    session['session_id'] = session_id
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': greeting['message'],
        'phase': greeting['phase']
    })


@app.route('/api/message', methods=['POST'])
def send_message():
    """
    Send a message to the agent and get a response.
    
    Expected JSON body:
        {
            "message": "user message text",
            "session_id": "optional session id"
        }
    
    Returns:
        dict: Agent response, current phase, and conversation state
    """
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({
            'success': False,
            'error': 'Message is required'
        }), 400
    
    # Get session
    session_id = data.get('session_id') or session.get('session_id')
    
    if not session_id or session_id not in active_sessions:
        return jsonify({
            'success': False,
            'error': 'Invalid or expired session. Please start a new session.'
        }), 400
    
    orchestrator = active_sessions[session_id]
    
    try:
        # Process message through orchestrator
        response = orchestrator.process_message(data['message'])
        
        # Log any errors from the agent
        if response.get('error'):
            app.logger.error(f"Agent error: {response.get('error')}")
            print(f"Agent error: {response.get('error')}")  # Also print to console
        
        return jsonify({
            'success': True,
            'message': response['message'],
            'phase': response['phase'],
            'agent': response.get('agent'),
            'is_complete': response.get('is_complete', False),
            'game_data': response.get('game_data'),
            'error': response.get('error')  # Include error in response for debugging
        })
    
    except Exception as e:
        app.logger.error(f"Error processing message: {str(e)}")
        import traceback
        traceback.print_exc()  # Print full traceback
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500


@app.route('/api/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """
    Get current session state.
    
    Args:
        session_id: The session identifier
    
    Returns:
        dict: Current session state including phase, conversation history, etc.
    """
    if session_id not in active_sessions:
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404
    
    orchestrator = active_sessions[session_id]
    state = orchestrator.get_state()
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'phase': state['phase'],
        'book_info': state.get('book_info'),
        'conversation_count': len(state.get('conversation_history', []))
    })


@app.route('/api/game/<session_id>', methods=['GET'])
def get_game(session_id):
    """
    Get the generated game HTML for a session.
    
    Args:
        session_id: The session identifier
    
    Returns:
        HTML string of the complete game
    """
    if session_id not in active_sessions:
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404
    
    orchestrator = active_sessions[session_id]
    state = orchestrator.get_state()
    
    if not state.get('game_html'):
        return jsonify({
            'success': False,
            'error': 'Game not yet generated'
        }), 400
    
    return state['game_html'], 200, {'Content-Type': 'text/html'}


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring and deployment platforms.
    
    Returns:
        JSON response with status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'the-game-maker',
        'version': '2.0'
    }), 200


if __name__ == '__main__':
    # Development server
    app.run(host='0.0.0.0', port=5001, debug=True)

