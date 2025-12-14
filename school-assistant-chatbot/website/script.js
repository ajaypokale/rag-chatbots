/**
 * YOUR_API_GATEWAY_ENDPOINT - Replace this with your actual API endpoint URL.
 * Example: 'https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/myfunction'
 */
const API_ENDPOINT = 'YOUR_API_GATEWAY_ENDPOINT'; 

// Get elements for the chat toggle
const chatToggleButton = document.getElementById('chat-toggle-button');
const chatWidget = document.getElementById('chat-widget');
const questionInput = document.getElementById('question-input');

// Event listener for the toggle button
chatToggleButton.addEventListener('click', toggleChat);

/**
 * Toggles the visibility of the chat widget.
 */
function toggleChat() {
    chatWidget.classList.toggle('visible');
    chatWidget.classList.toggle('hidden');
    if (chatWidget.classList.contains('visible')) {
        questionInput.focus(); // Focus on input when chat opens
    }
}

/**
 * Inserts a new message bubble into the chat box.
 * @param {string} text - The message content.
 * @param {string} sender - 'user' or 'assistant'.
 */
function insertMessage(text, sender) {
    const chatBox = document.getElementById('chat-box');
    
    // Create the main message container div
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(sender + '-message');
    
    // Create the paragraph for the text
    const p = document.createElement('p');
    p.textContent = text;
    
    messageDiv.appendChild(p);
    chatBox.appendChild(messageDiv);
    
    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;
}


/**
 * Main function invoked by the Send button.
 * It reads the question, updates the UI, calls the API, and renders the response.
 */
async function sendMessage() {
    const inputField = document.getElementById('question-input');
    const sendButton = document.getElementById('send-button');
    const statusMessage = document.getElementById('status-message');
    
    const userQuestion = inputField.value.trim();
    
    if (userQuestion === "") {
        statusMessage.textContent = "Please type a question.";
        setTimeout(() => statusMessage.textContent = "", 2000);
        return;
    }

    // 1. UI Update: Disable input, show user message, show loading status
    inputField.value = ''; // Clear the input field
    sendButton.disabled = true; // Prevent multiple clicks
    statusMessage.textContent = "Assistant is typing...";
    
    insertMessage(userQuestion, 'user');
    
    try {
		console.log(userQuestion);
        // 2. API Call Logic
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: userQuestion }) // Pass the question in the body
        });
		if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
       
        const data = await response.json();
		console.log(data);
        
        // Assuming your API returns an object like { answer: "..." }
        const assistantResponse = data.answer || "Sorry, I received an unknown response format.";
		console.log(assistantResponse);

        // 3. UI Update: Show assistant response
        insertMessage(assistantResponse, 'assistant');

    } catch (error) {
        console.error('API Call Error:', error);
        insertMessage(`Error: Could not connect to the assistant. Please check the console or the API endpoint.`, 'assistant');
        statusMessage.textContent = "Connection error occurred.";

    } finally {
        // 4. UI Update: Re-enable input and clear status
        sendButton.disabled = false;
        statusMessage.textContent = "";
        inputField.focus(); // Set focus back to the input field
    }
}