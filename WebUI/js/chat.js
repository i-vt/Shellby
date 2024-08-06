// chat.js

// Object to store chat messages for each node
const chatMessages = {};

// Initialize the chat interface
function initializeChat() {
    // Handle Enter key for sending messages
    const chatInput = document.getElementById('chat-input');
    chatInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevent newline
            sendMessage(); // Send message
        }
    });
}

// Function to send a chat message
function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (message !== '') {
        const activeTab = document.querySelector('.chat-tab.active');
        const nodeId = activeTab.getAttribute('data-node-id');
        const chatWindow = document.getElementById('chat-window');

        // Append user's message to chat window and store it
        const userMessage = {
            type: 'user',
            text: message,
            timestamp: new Date().toISOString()
        };
        
        chatMessages[nodeId].push(userMessage);
        appendMessageToChatWindow(userMessage);

        // Auto-scroll to the bottom
        chatWindow.scrollTop = chatWindow.scrollHeight;

        // Clear the input
        input.value = '';

        // Simulate a bot response
        setTimeout(() => {
            const botMessage = {
                type: 'bot',
                text: 'This is a bot response.',
                timestamp: new Date().toISOString()
            };
            chatMessages[nodeId].push(botMessage);
            appendMessageToChatWindow(botMessage);

            // Auto-scroll to the bottom
            chatWindow.scrollTop = chatWindow.scrollHeight;

            // Save updated chat to file
            saveChatToFile(nodeId);
        }, 1000);
    }
}

// Function to append a message to the chat window
function appendMessageToChatWindow(message) {
    const chatWindow = document.getElementById('chat-window');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${message.type}`;
    messageDiv.textContent = message.text;
    chatWindow.appendChild(messageDiv);
}

// Function to create chat tab for each node
function createChatTab(nodeId) {
    const chatTabs = document.getElementById('chat-tabs');
    const tab = document.createElement('div');
    tab.className = 'chat-tab';
    tab.textContent = nodeId;
    tab.setAttribute('data-node-id', nodeId);

    tab.addEventListener('click', function() {
        // Set active tab
        const activeTab = document.querySelector('.chat-tab.active');
        if (activeTab) activeTab.classList.remove('active');
        tab.classList.add('active');

        // Load messages for this node
        loadChatMessages(nodeId);
    });

    chatTabs.appendChild(tab);

    // Set the first tab as active by default
    if (chatTabs.childElementCount === 1) {
        tab.classList.add('active');
        loadChatMessages(nodeId);
    }
}

// Function to load chat messages for the selected node
function loadChatMessages(nodeId) {
    const chatWindow = document.getElementById('chat-window');
    chatWindow.innerHTML = ''; // Clear current messages

    // Fetch stored messages from the JSON file
    fetch(`data/${nodeId}.json`)
        .then(response => response.json())
        .then(data => {
            chatMessages[nodeId] = data.messages;

            // Append each message to the chat window
            chatMessages[nodeId].forEach(message => {
                appendMessageToChatWindow(message);
            });

            // Auto-scroll to the bottom
            chatWindow.scrollTop = chatWindow.scrollHeight;
        })
        .catch(error => {
            console.error(`Error loading chat messages for ${nodeId}:`, error);
        });
}

// Function to save chat messages to a JSON file
function saveChatToFile(nodeId) {
    // Prepare data for saving
    const data = {
        messages: chatMessages[nodeId]
    };

    // Perform a POST request to save the data
    fetch(`data/${nodeId}.json`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        console.log(`Chat for ${nodeId} saved successfully.`);
    })
    .catch(error => {
        console.error(`Error saving chat for ${nodeId}:`, error);
    });
}
