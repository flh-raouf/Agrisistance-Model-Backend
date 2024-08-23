async function sendMessageToChatbot(message) {
    const response = await fetch('http://localhost:8000/chat', {  // Adjust the URL if needed
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: 'gpt-4-turbo',
            messages: [{ role: 'user', content: message }],
            max_token: 100,
            temperature: 0.7,
            response_format: 'text/plain',
            user_id: 'user123'  // Optional
        })
    });

    const data = await response.json();
    return data;
}

// Usage example:
sendMessageToChatbot('What crops should I plant in my region?').then(response => {
    console.log(response);
});
