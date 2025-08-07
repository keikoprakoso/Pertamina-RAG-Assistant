document.addEventListener('DOMContentLoaded', function() {
    const chatHistory = document.getElementById('chatHistory');
    const questionForm = document.getElementById('questionForm');
    const questionInput = document.getElementById('questionInput');
    const langToggle = document.getElementById('langToggle');
    const langToggleID = document.getElementById('langToggleID');
    
    // Set current language (default to English)
    let currentLanguage = 'en';
    
    // Language toggle functionality
    langToggle.addEventListener('click', function() {
        currentLanguage = 'en';
        langToggle.classList.add('active');
        langToggleID.classList.remove('active');
    });
    
    langToggleID.addEventListener('click', function() {
        currentLanguage = 'id';
        langToggleID.classList.add('active');
        langToggle.classList.remove('active');
    });
    
    // Form submission handler
    questionForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const question = questionInput.value.trim();
        if (!question) return;
        
        // Add user message to chat
        addMessageToChat(question, 'user');
        
        // Clear input
        questionInput.value = '';
        
        // Show loading indicator
        const loadingMsg = addLoadingMessage();
        
        try {
            // Send request to backend
            const response = await fetch('http://localhost:8000/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question })
            });
            
            // Remove loading message
            chatHistory.removeChild(loadingMsg);
            
            if (response.ok) {
                const data = await response.json();
                // Add bot response to chat
                addMessageToChat(data.answer, 'bot');
            } else {
                // Handle error
                addMessageToChat('Sorry, I encountered an error processing your request. Please try again.', 'bot');
            }
        } catch (error) {
            // Remove loading message
            chatHistory.removeChild(loadingMsg);
            
            // Handle network error
            addMessageToChat('Sorry, I couldn\'t connect to the server. Please make sure the backend is running.', 'bot');
            console.error('Error:', error);
        }
        
        // Scroll to bottom of chat
        chatHistory.scrollTop = chatHistory.scrollHeight;
    });
    
    // Function to add message to chat
    function addMessageToChat(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender + '-message');
        
        if (sender === 'bot') {
            // Add bot message header
            const headerDiv = document.createElement('div');
            headerDiv.classList.add('message-header');
            headerDiv.innerHTML = '<i class="fas fa-robot"></i><span class="sender-name">Knowledge Assistant</span>';
            messageDiv.appendChild(headerDiv);
            
            // For bot messages, we need to separate English and Indonesian content
            const contents = content.split('\n\n');
            if (contents.length >= 2) {
                // Check if we have both English and Indonesian versions
                const hasIndonesian = content.includes('**Indonesian:**') || content.includes('[Indonesian]') || content.includes('Untuk') || content.includes('untuk');
                
                if (hasIndonesian) {
                    // Format: English content \n\n Indonesian content
                    let englishContent = '';
                    let indonesianContent = '';
                    
                    if (content.includes('**Indonesian:**')) {
                        const parts = content.split('**Indonesian:**');
                        englishContent = parts[0].replace('**English:**', '').trim();
                        indonesianContent = parts[1].trim();
                    } else if (content.includes('[Indonesian]')) {
                        const parts = content.split('[Indonesian]');
                        englishContent = parts[0].trim();
                        indonesianContent = parts[1].trim();
                    } else {
                        // Try to separate based on content
                        let foundIndonesian = false;
                        for (let i = 0; i < contents.length; i++) {
                            if (contents[i].includes('Untuk') || contents[i].includes('untuk') || contents[i].includes('dan') || contents[i].includes('atau')) {
                                indonesianContent = contents[i];
                                foundIndonesian = true;
                            } else if (!foundIndonesian) {
                                englishContent += (englishContent ? '\n\n' : '') + contents[i];
                            } else {
                                indonesianContent += '\n\n' + contents[i];
                            }
                        }
                    }
                    
                    const englishDiv = document.createElement('div');
                    englishDiv.classList.add('message-content');
                    englishDiv.textContent = englishContent;
                    messageDiv.appendChild(englishDiv);
                    
                    const indonesianDiv = document.createElement('div');
                    indonesianDiv.classList.add('message-content', 'indonesian');
                    indonesianDiv.textContent = indonesianContent;
                    messageDiv.appendChild(indonesianDiv);
                } else {
                    // Single content, just display it
                    const contentDiv = document.createElement('div');
                    contentDiv.classList.add('message-content');
                    contentDiv.textContent = content;
                    messageDiv.appendChild(contentDiv);
                }
            } else {
                // Single content, just display it
                const contentDiv = document.createElement('div');
                contentDiv.classList.add('message-content');
                contentDiv.textContent = content;
                messageDiv.appendChild(contentDiv);
            }
        } else {
            // Add user message header
            const headerDiv = document.createElement('div');
            headerDiv.classList.add('message-header');
            headerDiv.innerHTML = '<i class="fas fa-user"></i><span class="sender-name">You</span>';
            messageDiv.appendChild(headerDiv);
            
            // User message
            const contentDiv = document.createElement('div');
            contentDiv.classList.add('message-content');
            contentDiv.textContent = content;
            messageDiv.appendChild(contentDiv);
        }
        
        chatHistory.appendChild(messageDiv);
        
        // Scroll to bottom of chat
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    
    // Function to add loading message
    function addLoadingMessage() {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'bot-message');
        messageDiv.id = 'loadingMessage';
        
        const headerDiv = document.createElement('div');
        headerDiv.classList.add('message-header');
        headerDiv.innerHTML = '<i class="fas fa-robot"></i><span class="sender-name">Knowledge Assistant</span>';
        messageDiv.appendChild(headerDiv);
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.innerHTML = '<div class="loading"></div> Processing your question...';
        messageDiv.appendChild(contentDiv);
        
        chatHistory.appendChild(messageDiv);
        
        // Scroll to bottom of chat
        chatHistory.scrollTop = chatHistory.scrollHeight;
        
        return messageDiv;
    }
});