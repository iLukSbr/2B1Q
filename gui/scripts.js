let isSending = false;

function prepareAndSendMessage() {
    if (isSending) return; // Prevent multiple submissions
    isSending = true;

    const message = document.getElementById('messageInput').value;
    if (!message) {
        isSending = false;
        return;
    }

    pywebview.api.send_message(message).then(response => {
        const senderDetails = document.getElementById('senderDetails');
        if (senderDetails) {
            senderDetails.innerHTML = `
                <p>Raw Message: ${response.raw_message}</p>
                <p>Binary Message: ${response.binary_message}</p>
                <p>Encrypted Message: ${response.encrypted_message}</p>
                <p>2B1Q Encoded Message: ${response.encoded_message}</p>
            `;
        }
        const preparedSignal = response.encoded_message;
        pywebview.api.send_signal(preparedSignal).then(sendResponse => {
            alert(sendResponse);
            isSending = false; // Reset the flag after sending
        }).catch(() => {
            isSending = false; // Reset the flag in case of error
        });
    }).catch(() => {
        isSending = false; // Reset the flag in case of error
    });
}

function receiveMessage() {
    pywebview.api.receive_message().then(response => {
        const receivedMessages = document.getElementById('receivedMessages');
        if (receivedMessages) {
            const messageElement = document.createElement('p');
            messageElement.textContent = response.message;
            receivedMessages.appendChild(messageElement);
        }

        const receiverDetails = document.getElementById('receiverDetails');
        if (receiverDetails) {
            receiverDetails.innerHTML = `
                <p>Raw Message: ${response.raw_message}</p>
                <p>Binary Message: ${response.binary_message}</p>
                <p>Encrypted Message: ${response.encrypted_message}</p>
                <p>2B1Q Encoded Message: ${response.encoded_message}</p>
            `;
        }
    });
}

function plotGraph() {
    const trace1 = {
        x: [1, 2, 3, 4, 5],
        y: [10, 15, 13, 17, 21],
        type: 'scatter'
    };
    const data = [trace1];
    Plotly.newPlot('graph', data); // Render the graph in the div with id="graph"
}

plotGraph();