let isSending = false;

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
            alert(sendResponse);
            reloadSVG();
            isSending = false;
        }).catch(() => {
            isSending = false;
        });
    }).catch(() => {
        isSending = false;
    });
}

function receiveMessage() {
    const host = document.getElementById('hostInput').value;
    const port = document.getElementById('portInput').value;

    if (!host || !port) {
        return;
    }

    pywebview.api.receive_message(host, port).then(response => {
        displayMessage(response.message, 'received', response);
        plotGraph(response.encoded_message, 'Received Signal');
    });
}

function displayMessage(message, type, details) {
    const chatMessages = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', type);

    const photo = document.createElement('img');
    photo.classList.add('photo');
    photo.src = type === 'sent' ? 'path/to/os/logo.png' : 'path/to/other/os/logo.png';

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
    reloadSVG();
}

pywebview.api.get_ip().then(response => {
    const chatMessages = document.getElementById('chatMessages');
    const ipElement = document.createElement('div');
    ipElement.classList.add('message', 'received');
    ipElement.innerHTML = `
        <p><strong>${response.hostname}</strong> (${response.ip})</p>
    `;
    chatMessages.appendChild(ipElement);
});

function reloadSVG() {
    const graph = document.getElementById('graph');
    const newGraph = document.createElement('img');
    newGraph.src = '../graph/signal.svg?' + new Date().getTime(); // Add timestamp to force reload
    newGraph.alt = '2B1Q Signal Graph';
    newGraph.id = 'graph';
    graph.parentNode.replaceChild(newGraph, graph);
}