const inputField = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const chatWindow = document.getElementById("chat-window");

async function sendMessageToChatbot(message) {
    console.log("Sending message to chatbot:", message); // Debug log

    try {
        const response = await fetch(`${window.location.origin}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Parsed response data:", data); // Debug log
            return data.responses; // Return multiple responses
        } else {
            console.error("Error communicating with chatbot. Status:", response.status);
            return [];
        }
    } catch (error) {
        console.error("Fetch error:", error); // Debug log
        return [];
    }
}

async function displayResponsesSequentially(responses) {
    for (const response of responses) {
        await new Promise(resolve => {
            setTimeout(() => {
                addMessageToChat(response.ai, response.response);
                resolve();
            }, 1000); // Wait 1 second before showing the next response
        });
    }
}

sendButton.addEventListener("click", async () => {
    const userMessage = inputField.value.trim();
    if (!userMessage) return;

    // Add the user's message to the chat
    addMessageToChat("user", userMessage);
    inputField.value = "";

    // Get the chatbot's responses
    const chatbotResponses = await sendMessageToChatbot(userMessage);

    // Display responses one by one
    await displayResponsesSequentially(chatbotResponses);
});

function formatMessageAsHTML(role, message) {
    // Check if the message contains a code block (e.g., starts with ``` and ends with ```)
    if (message.includes("```")) {
        // Extract the code block
        const formattedMessage = message.replace(/```(.*?)```/gs, (match, code) => {
            return `<pre><code>${code.trim()}</code></pre>`;
        });
        return formattedMessage;
    }
    return `<span>${message}</span>`;
}

function addMessageToChat(role, message) {
    const messageContainer = document.createElement("div");
    messageContainer.classList.add("message-container");

    // if (!message.trim()) {
    //     return;
    // }

    if (role === "raccoon") {
        messageContainer.innerHTML = `
            <div class="chatbot-message">
                <img src="/static/donald.png" alt="Raccoon Icon">
                <span><strong>Donald Trump:</strong> ${message}</span>
            </div>
        `;
    } else if (role === "lion") {
        messageContainer.innerHTML = `
            <div class="chatbot-message">
                <img src="/static/joe_biden.png" alt="Lion Icon">
                <span><strong>Joe Biden:</strong> ${message}</span>
            </div>
        `;
    } else if (role === "user") {
        messageContainer.classList.add("user");
        messageContainer.innerHTML = `
            <div class="user-message">
                <strong>User:</strong> ${message}
            </div>
        `;
    }

    chatWindow.appendChild(messageContainer);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll
}
