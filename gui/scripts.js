/**
 * @file scripts.js
 * @brief Arquivo de scripts da interface gráfica do usuário.
 */
let isSending = false
let ws

/**
 * @brief Obtém o endereço do servidor WebSocket e inicia a conexão.
 */
pywebview.api.get_websocket_url().then(url => {
    ws = new WebSocket(url);

    ws.onopen = function(event) {
        console.log('WebSocket connection opened:', event);
    };

    ws.onerror = function(event) {
        console.error('WebSocket error:', event);
    };

    ws.onclose = function(event) {
        console.log('WebSocket connection closed:', event);
    };

    ws.onmessage = function(event) {
        const message = JSON.parse(event.data);
        displayMessage(message.message, 'received', message);
        reloadSVG();
    };
});

/**
 * @brief Escutador de eventos de erro de conexão com o servidor WebSocket.
 */
function prepareAndSendMessage() {
    const hostInput = document.getElementById('hostInput')
    const portInput = document.getElementById('portInput')

    if (!hostInput.value) {
        alert('Host is required')
        hostInput.focus()
        return
    }

    if (!portInput.value) {
        alert('Port is required')
        portInput.focus()
        return
    }

    if (isSending) return
    isSending = true

    const message = document.getElementById('messageInput').value
    const host = document.getElementById('hostInput').value
    const port = document.getElementById('portInput').value

    if (!message || !host || !port) {
        isSending = false
        return
    }

    pywebview.api.prepare_message(message).then(response => {
        displayMessage(message, 'sent', response)
        const preparedSignal = response.encoded_message
        pywebview.api.send_signal(preparedSignal, host, port).then(sendResponse => {
            isSending = false
        }).catch(() => {
            isSending = false
        })
    }).catch(() => {
        isSending = false
    })

    reloadSVG()
}

/**
 * @brief Exibe uma mensagem na tela.
 * @param message Mensagem a ser exibida.
 * @param type Tipo da mensagem (enviada ou recebida).
 * @param details Detalhes da mensagem (mensagem bruta, mensagem binária, mensagem criptografada e mensagem codificada).
 */
function displayMessage(message, type, details) {
    const chatMessages = document.getElementById('chatMessages')
    const messageElement = document.createElement('div')
    messageElement.classList.add('message', type)

    const photo = document.createElement('img')
    photo.classList.add('photo')
    photo.src = 'square_wave.ico'

    const content = document.createElement('div')
    content.classList.add('content')

    content.innerHTML = `
        <p class="message-title">${type.charAt(0).toUpperCase() + type.slice(1)}</p>
        <p>${message}</p>
        <div class="details">
            <p>Raw Message: ${details.raw_message}</p>
            <p>Binary Message: ${details.binary_message}</p>
            <p>Encrypted Message: ${details.encrypted_message}</p>
            <p>2B1Q Encoded Message: ${details.encoded_message}</p>
        </div>
    `

    messageElement.appendChild(photo)
    messageElement.appendChild(content)
    chatMessages.appendChild(messageElement)
    chatMessages.scrollTop = chatMessages.scrollHeight
    if (type === 'received') {
        alert(`Received message: ${message}`)
    }
    reloadSVG()
}

/**
 * @brief Recarrega os gráficos SVG.
 */
function reloadSVG() {
    const graphRecv = document.getElementById('graph_recv')
    const newGraphRecv = document.createElement('img')
    newGraphRecv.src = 'received_signal.svg?' + new Date().getTime() // Add timestamp to force reload
    newGraphRecv.alt = '2B1Q Received Signal Graph'
    newGraphRecv.id = 'graph_recv'
    graphRecv.parentNode.replaceChild(newGraphRecv, graphRecv)

    const graphSent = document.getElementById('graph_sent')
    const newGraphSent = document.createElement('img')
    newGraphSent.src = 'sent_signal.svg?' + new Date().getTime() // Add timestamp to force reload
    newGraphSent.alt = '2B1Q Sent Signal Graph'
    newGraphSent.id = 'graph_sent'
    graphSent.parentNode.replaceChild(newGraphSent, graphSent)
}

/**
 * @brief Task que verifica se há mensagens recebidas.
 */
function pollReceivedMessage() {
    pywebview.api.get_received_message().then(response => {
        pywebview.api.log_message('Received response: ' + JSON.stringify(response));
        if (response.message) {
            displayMessage(response.message, 'received', response);
            pywebview.api.log_message('Message displayed: ' + response.message);
        } else {
            pywebview.api.log_message('No message received');
        }
    }).catch(error => {
        pywebview.api.log_message('Error fetching received message: ' + error);
    }).finally(() => {
        setTimeout(pollReceivedMessage, 3000);
    });
}


/**
 * @brief Task que verifica se há arquivos de gráficos a serem atualizados.
 */
function pollGraphFiles() {
    reloadSVG()
    setTimeout(pollGraphFiles, 3000) // Poll every 3 seconds
}

pollReceivedMessage()
pollGraphFiles()
