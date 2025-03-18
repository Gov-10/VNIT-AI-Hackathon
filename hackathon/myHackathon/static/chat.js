

function sendMessage() {
    let userMessage = document.getElementById("user-input").value;
    console.log("Sending message:", userMessage);  // Debugging

    let encodedMessage = encodeURIComponent(userMessage);

    fetch("https://vnit-ai-hackathon-production.up.railway.app/chatbot_response/?message=" + encodedMessage, {
        method: "GET",
        credentials: "include",  // Ensures cookies are sent
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok: " + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("chat-output").innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;
    })
    .catch(error => console.error("Error:", error));

    document.getElementById("user-input").value = "";
}

