let isSending = false;
const ws = new WebSocket('ws://localhost:6789');
let ipAddress = '';

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    displayMessage(message.message, 'received', message);
    reloadSVG(); // Update the graph when a new message is received
};

function prepareAndSendMessage() {
    const hostInput = document.getElementById('hostInput');
    const portInput = document.getElementById('portInput');

    if (!hostInput.value) {
        alert('Host is required');
        hostInput.focus();
        return;
    }

    if (!portInput.value) {
        alert('Port is required');
        portInput.focus();
        return;
    }

    if (isSending) return;
    isSending = true;

    const message = document.getElementById('messageInput').value;
    const host = document.getElementById('hostInput').value;
    const port = document.getElementById('portInput').value;

    if (!message || !host || !port) {
        isSending = false;
        return;
    }

    pywebview.api.prepare_message(message).then(response => {
        displayMessage(message, 'sent', response);
        const preparedSignal = response.encoded_message;
        pywebview.api.send_signal(preparedSignal, host, port).then(sendResponse => {
            isSending = false;
        }).catch(() => {
            isSending = false;
        });
    }).catch(() => {
        isSending = false;
    });

    reloadSVG();
}

function displayMessage(message, type, details) {
    const chatMessages = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', type);

    const photo = document.createElement('img');
    photo.classList.add('photo');
    photo.src = 'square_wave.ico';

    const content = document.createElement('div');
    content.classList.add('content');

    content.innerHTML = `
        <p class="message-title">${type.charAt(0).toUpperCase() + type.slice(1)}</p>
        <p>${message}</p>
        <div class="details">
            <p>Raw Message: ${details.raw_message}</p>
            <p>Binary Message: ${details.binary_message}</p>
            <p>Encrypted Message: ${details.encrypted_message}</p>
            <p>2B1Q Encoded Message: ${details.encoded_message}</p>
        </div>
    `;

    messageElement.appendChild(photo);
    messageElement.appendChild(content);
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    if (type === 'received') {
        alert(`Received message: ${message}`);
    }
    reloadSVG(); // Update the graph when a new message is displayed
}

// pywebview.api.get_ip().then(response => {
//     ipAddress = response;
//     const chatMessages = document.getElementById('chatMessages');
//     const ipElement = document.createElement('div');
//     ipElement.classList.add('message', 'received');
//     ipElement.innerHTML = `
//         <p><strong>${response.hostname}</strong> (${response})</p>
//     `;
//     chatMessages.appendChild(ipElement);
// });

function reloadSVG() {
    setTimeout(() => {
        const graph = document.getElementById('graph_recv');
        const newGraph = document.createElement('img');
        newGraph.src = 'received_signal.svg?' + new Date().getTime(); // Add timestamp to force reload
        newGraph.alt = '2B1Q Received Signal Graph';
        newGraph.id = 'graph';
        graph.parentNode.replaceChild(newGraph, graph);
        const graph2 = document.getElementById('graph_sent');
        const newGraph2 = document.createElement('img');
        newGraph2.src = 'sent_signal.svg?' + new Date().getTime(); // Add timestamp to force reload
        newGraph2.alt = '2B1Q Sent Signal Graph';
        newGraph2.id = 'graph';
        graph2.parentNode.replaceChild(newGraph2, graph2);
    }, 1000); // Delay of 1 second
}

function pollReceivedMessage() {
    pywebview.api.get_received_message().then(response => {
        if (response.message) {
            displayMessage(response.message, 'received', response);
        }
    }).catch(error => {
        console.error('Error fetching received message:', error);
    }).finally(() => {
        setTimeout(pollReceivedMessage, 3000);
    });
}

pollReceivedMessage();