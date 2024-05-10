function sendMessage() {
    var input = document.getElementById('chat-input');
    var message = input.value;
    input.value = '';

    fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({message: message})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('chat-output').textContent += 'You: ' + message + '\n';
        document.getElementById('chat-output').textContent += 'Bot: ' + data.response + '\n';
    })
    .catch(error => console.error('Error:', error));
}