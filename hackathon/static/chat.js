// document.getElementById("sendBtn").addEventListener("click", function() {
//     let userMessage = document.getElementById("userInput").value;
    
//     fetch("https://vnit-ai-hackathon-production.up.railway.app/chatbot_response/", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify({ message: userMessage })
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.getElementById("chatbox").innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;
//     });
// });

function sendMessage() {
    let userMessage = document.getElementById("user-input").value;
    console.log("Sending message:", userMessage);  // Debugging

    let encodedMessage = encodeURIComponent(userMessage);

    fetch("https://vnit-ai-hackathon-production.up.railway.app/chatbot_response?message=" + encodedMessage, {
        method: "GET",
        credentials: "include",
        mode: "cors",  // Ensures cookies are sent
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
