/**
 * Voice Input Handler - Web Speech API Integration
 * Enables voice input for hands-free interaction
 */

// Check for browser support
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let isListening = false;
let silenceTimer = null;
let currentTranscript = '';

// Configuration
const SILENCE_DELAY = 2500; // Wait 2.5 seconds of silence before submitting

// DOM Elements
const voiceButton = document.getElementById('voice-button');
const voiceStatus = document.getElementById('voice-status');

/**
 * Initialize voice recognition
 */
function initVoice() {
    if (!SpeechRecognition) {
        console.warn('Speech Recognition not supported in this browser');
        voiceButton.disabled = true;
        voiceButton.title = 'Voice input not supported in this browser';
        return;
    }
    
    // Create recognition instance
    recognition = new SpeechRecognition();
    recognition.continuous = true;  // Keep listening for pauses
    recognition.interimResults = true;  // Show interim results
    recognition.lang = 'en-US';  // Language
    recognition.maxAlternatives = 1;
    
    // Event: Recognition starts
    recognition.onstart = function() {
        console.log('🎤 Voice recognition started');
        isListening = true;
        currentTranscript = '';
        voiceButton.classList.add('bg-red-600', 'hover:bg-red-700');
        voiceButton.classList.remove('bg-purple-600', 'hover:bg-purple-700');
        voiceButton.textContent = '⏹️';
        voiceStatus.classList.remove('hidden');
        voiceStatus.textContent = '🎤 Listening... (click again or wait to finish)';
    };
    
    // Event: Recognition ends
    recognition.onend = function() {
        console.log('🎤 Voice recognition ended');
        isListening = false;
        
        // Clear any pending timers
        if (silenceTimer) {
            clearTimeout(silenceTimer);
            silenceTimer = null;
        }
        
        // Submit final transcript if there is one
        if (currentTranscript.trim()) {
            submitTranscript(currentTranscript);
            currentTranscript = '';
        }
        
        voiceButton.classList.remove('bg-red-600', 'hover:bg-red-700');
        voiceButton.classList.add('bg-purple-600', 'hover:bg-purple-700');
        voiceButton.textContent = '🎤';
        voiceStatus.classList.add('hidden');
    };
    
    // Event: Result received
    recognition.onresult = function(event) {
        // Clear existing silence timer
        if (silenceTimer) {
            clearTimeout(silenceTimer);
        }
        
        // Build full transcript from all results
        let interimTranscript = '';
        let finalTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }
        
        // Update current transcript with final results
        if (finalTranscript) {
            currentTranscript += finalTranscript;
            console.log('📝 Final transcript so far:', currentTranscript);
            
            // Show what we have so far
            voiceStatus.textContent = `🎤 "${currentTranscript.trim()}" (keep talking or wait to finish)`;
            
            // Start silence timer - will submit after SILENCE_DELAY ms of no speech
            silenceTimer = setTimeout(() => {
                if (currentTranscript.trim()) {
                    console.log('⏱️ Silence detected, submitting transcript');
                    recognition.stop(); // This will trigger onend which submits
                }
            }, SILENCE_DELAY);
        }
        
        // Show interim results
        if (interimTranscript) {
            voiceStatus.textContent = `🎤 "${currentTranscript}${interimTranscript}" (still listening...)`;
        }
    };
    
    // Event: Error occurred
    recognition.onerror = function(event) {
        console.error('❌ Speech recognition error:', event.error);
        
        let errorMessage = 'Voice input error';
        
        switch (event.error) {
            case 'no-speech':
                errorMessage = 'No speech detected. Please try again.';
                break;
            case 'audio-capture':
                errorMessage = 'Microphone not found. Please check your mic.';
                break;
            case 'not-allowed':
                errorMessage = 'Microphone permission denied. Please allow access.';
                break;
            default:
                errorMessage = `Voice error: ${event.error}`;
        }
        
        showVoiceError(errorMessage);
    };
    
    // Add click listener to voice button
    voiceButton.addEventListener('click', toggleVoice);
    
    // Add keyboard shortcut (V key)
    document.addEventListener('keydown', (e) => {
        if (e.key === 'v' && e.ctrlKey) {
            e.preventDefault();
            toggleVoice();
        }
    });
}

/**
 * Toggle voice recognition on/off
 */
function toggleVoice() {
    if (!recognition) return;
    
    if (isListening) {
        recognition.stop();
    } else {
        try {
            recognition.start();
        } catch (error) {
            console.error('Error starting recognition:', error);
            // Recognition might already be running
        }
    }
}

/**
 * Submit the transcript to the chat
 */
function submitTranscript(transcript) {
    console.log('📤 Submitting transcript:', transcript);
    
    // Call the handler from app.js
    if (window.handleVoiceInput) {
        window.handleVoiceInput(transcript.trim());
    }
}

/**
 * Show voice error message
 */
function showVoiceError(message) {
    voiceStatus.textContent = `❌ ${message}`;
    voiceStatus.classList.remove('hidden');
    voiceStatus.classList.add('text-red-600');
    
    setTimeout(() => {
        voiceStatus.classList.add('hidden');
        voiceStatus.classList.remove('text-red-600');
        voiceStatus.textContent = '🎤 Listening...';
    }, 3000);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initVoice);

