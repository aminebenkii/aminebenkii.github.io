const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");
const sendButton = document.getElementById("send-chat");

sendButton.addEventListener("click", () => {
    const userMessage = chatInput.value;

    if (!userMessage) return;

    // Display user's message in the chat
    chatMessages.innerHTML += `<div>You: ${userMessage}</div>`;
    chatInput.value = "";

    // Send the message to your backend
    fetch("https://aminebenkii-github-io.onrender.com/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: userMessage }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.response) {
                // Display the bot's response
                chatMessages.innerHTML += `<div>Bot: ${data.response}</div>`;
            } else {
                chatMessages.innerHTML += `<div>Bot: Sorry, something went wrong.</div>`;
            }
        })
        .catch(() => {
            chatMessages.innerHTML += `<div>Bot: Failed to connect to the server.</div>`;
        });
});
