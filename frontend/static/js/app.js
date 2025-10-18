/**
 * The Game Maker - Main Application Logic
 * Handles chat interface, API communication, and UI updates
 */

// State
let sessionId = null;
let currentPhase = 'identifying';
let isProcessing = false;

// DOM Elements
const messagesContainer = document.getElementById('messages-container');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const phaseText = document.getElementById('phase-text');
const agentName = document.getElementById('agent-name');
const statusIndicator = document.getElementById('status-indicator');
const gameResult = document.getElementById('game-result');
const startOverButton = document.getElementById('start-over');

// Phase display names
const phaseNames = {
    'identifying': 'Finding Your Book 📖',
    'discussing': 'Talking About the Story 💭',
    'designing': 'Designing the Game 🎨',
    'generating': 'Building Your Game 🔨',
    'complete': 'Game Ready! 🎉'
};

// Agent display names
const agentNames = {
    'story_analyst': 'Story Expert',
    'game_designer': 'Game Designer',
    'code_generator': 'Code Builder'
};

/**
 * Initialize the application
 */
async function init() {
    console.log('🎮 Initializing The Game Maker...');
    
    // Add event listeners
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    startOverButton.addEventListener('click', startOver);
    
    // Start a new session
    await startSession();
}

/**
 * Start a new game creation session
 */
async function startSession() {
    try {
        const response = await fetch('/api/start_session', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        
        if (data.success) {
            sessionId = data.session_id;
            currentPhase = data.phase;
            
            // Display initial greeting
            addMessage(data.message, 'agent');
            updatePhase(data.phase);
            
            console.log('✅ Session started:', sessionId);
        } else {
            showError('Failed to start session. Please refresh the page.');
        }
    } catch (error) {
        console.error('Error starting session:', error);
        showError('Could not connect to the server. Please check your connection.');
    }
}

/**
 * Send a message to the agent
 */
async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message || isProcessing) return;
    
    // Add user message to UI
    addMessage(message, 'user');
    messageInput.value = '';
    
    // Show processing state
    isProcessing = true;
    setProcessingState(true);
    
    try {
        const response = await fetch('/api/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Add agent response
            addMessage(data.message, 'agent');
            
            // Update phase if changed
            if (data.phase !== currentPhase) {
                currentPhase = data.phase;
                updatePhase(data.phase, data.agent);
            }
            
            // Check if game is complete
            if (data.is_complete) {
                showGameResult(data.game_data);
            }
        } else {
            showError(data.error || 'Something went wrong. Please try again.');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        showError('Failed to send message. Please try again.');
    } finally {
        isProcessing = false;
        setProcessingState(false);
    }
}

/**
 * Add a message to the chat
 */
function addMessage(text, sender) {
    // Remove placeholder if it exists
    const placeholder = messagesContainer.querySelector('.text-center.text-gray-400');
    if (placeholder) {
        placeholder.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex ' + (sender === 'user' ? 'justify-end' : 'justify-start');
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble px-6 py-4 ' + 
        (sender === 'user' 
            ? 'message-bubble-user' 
            : 'message-bubble-agent');
    
    // Add sender label for agents
    if (sender === 'agent') {
        const label = document.createElement('div');
        label.className = 'text-xs font-semibold text-purple-600 mb-1 flex items-center gap-1';
        label.innerHTML = '🤖 <span>AI Assistant</span>';
        bubble.appendChild(label);
    }
    
    // Add message text
    const textEl = document.createElement('div');
    textEl.className = 'leading-relaxed';
    textEl.textContent = text;
    bubble.appendChild(textEl);
    
    // Add timestamp
    const timestamp = document.createElement('div');
    timestamp.className = 'text-xs mt-2 opacity-60';
    timestamp.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    bubble.appendChild(timestamp);
    
    messageDiv.appendChild(bubble);
    messagesContainer.appendChild(messageDiv);
    
    // Smooth scroll to bottom
    setTimeout(() => {
        messagesContainer.scrollTo({
            top: messagesContainer.scrollHeight,
            behavior: 'smooth'
        });
    }, 100);
}

/**
 * Update the phase indicator
 */
function updatePhase(phase, agent) {
    currentPhase = phase;
    phaseText.textContent = phaseNames[phase] || phase;
    
    if (agent) {
        agentName.textContent = agentNames[agent] || agent;
    }
    
    // Update status indicator color and animation
    if (phase === 'complete') {
        statusIndicator.className = 'w-4 h-4 rounded-full bg-gradient-to-r from-green-500 to-emerald-500';
    } else {
        statusIndicator.className = 'w-4 h-4 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 animate-pulse-glow';
    }
    
    // Update phase dots
    const phases = ['identifying', 'discussing', 'designing', 'generating', 'complete'];
    const currentIndex = phases.indexOf(phase);
    
    phases.forEach((p, index) => {
        const dot = document.getElementById(`phase-dot-${index + 1}`);
        if (dot) {
            if (index <= currentIndex) {
                dot.className = 'w-2 h-2 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500';
            } else {
                dot.className = 'w-2 h-2 rounded-full bg-purple-200 transition-all duration-500';
            }
        }
    });
}

/**
 * Set processing state
 */
function setProcessingState(processing) {
    sendButton.disabled = processing;
    messageInput.disabled = processing;
    
    if (processing) {
        sendButton.innerHTML = `
            <span class="flex items-center gap-2">
                <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Thinking...</span>
            </span>
        `;
        statusIndicator.className = 'w-4 h-4 rounded-full bg-gradient-to-r from-yellow-500 to-orange-500 animate-pulse-glow';
        
        // Add thinking indicator
        addThinkingIndicator();
    } else {
        sendButton.innerHTML = `
            <span class="flex items-center gap-2">
                Send
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                </svg>
            </span>
        `;
        statusIndicator.className = 'w-4 h-4 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 animate-pulse-glow';
        
        // Remove thinking indicator
        removeThinkingIndicator();
    }
}

/**
 * Add thinking indicator
 */
function addThinkingIndicator() {
    removeThinkingIndicator(); // Remove if exists
    
    const thinkingDiv = document.createElement('div');
    thinkingDiv.id = 'thinking-indicator';
    thinkingDiv.className = 'flex justify-start';
    thinkingDiv.innerHTML = `
        <div class="message-bubble message-bubble-agent px-6 py-4 typing-indicator">
            <div class="flex items-center gap-2">
                <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 0ms;"></div>
                <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 150ms;"></div>
                <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 300ms;"></div>
            </div>
        </div>
    `;
    messagesContainer.appendChild(thinkingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

/**
 * Remove thinking indicator
 */
function removeThinkingIndicator() {
    const indicator = document.getElementById('thinking-indicator');
    if (indicator) {
        indicator.remove();
    }
}

/**
 * Show error message
 */
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'flex justify-center my-4';
    errorDiv.innerHTML = `
        <div class="bg-gradient-to-r from-red-50 to-pink-50 border-2 border-red-300 text-red-700 px-6 py-4 rounded-2xl shadow-lg max-w-md animate-slide-up">
            <div class="flex items-center gap-3">
                <div class="text-2xl">⚠️</div>
                <div>
                    <div class="font-semibold mb-1">Oops!</div>
                    <div class="text-sm">${message}</div>
                </div>
            </div>
        </div>
    `;
    messagesContainer.appendChild(errorDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

/**
 * Show game result
 */
function showGameResult(gameData) {
    gameResult.classList.remove('hidden');
    
    // Update play link with session ID
    const playLink = gameResult.querySelector('a');
    if (playLink && sessionId) {
        playLink.href = `/api/game/${sessionId}`;
    }
    
    // Scroll to result
    gameResult.scrollIntoView({ behavior: 'smooth' });
    
    // Disable input
    messageInput.disabled = true;
    sendButton.disabled = true;
}

/**
 * Start over with a new game
 */
async function startOver() {
    // Reset UI
    messagesContainer.innerHTML = '';
    gameResult.classList.add('hidden');
    messageInput.disabled = false;
    sendButton.disabled = false;
    
    // Start new session
    await startSession();
}

/**
 * Handle voice input from voice.js
 */
window.handleVoiceInput = function(transcript) {
    messageInput.value = transcript;
    sendMessage();
};

// Initialize when page loads
document.addEventListener('DOMContentLoaded', init);

