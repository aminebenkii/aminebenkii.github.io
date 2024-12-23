// Open and close chat popup
const chatbotButton = document.getElementById("chatbot-button");
const chatPopup = document.getElementById("chat-popup");
const closeChat = document.getElementById("close-chat");

chatbotButton.addEventListener("click", () => {
  chatPopup.style.display = "block";
});

closeChat.addEventListener("click", () => {
  chatPopup.style.display = "none";
});

// Send user query to Flask backend
const sendChat = document.getElementById("send-chat");
const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");

sendChat.addEventListener("click", async () => {
  const userMessage = chatInput.value.trim();
  if (userMessage) {
    // Display user's message
    chatMessages.innerHTML += `<div><strong>You:</strong> ${userMessage}</div>`;
    chatInput.value = "";

    // Send message to backend
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: userMessage }),
    });

    const result = await response.json();

    if (result.response) {
      // Display bot's response
      chatMessages.innerHTML += `<div><strong>Bot:</strong> ${result.response}</div>`;
    } else {
      chatMessages.innerHTML += `<div><strong>Bot:</strong> Sorry, I couldn't process that.</div>`;
    }

    // Scroll to the bottom of the chat
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});
