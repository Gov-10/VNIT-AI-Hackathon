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
    console.log(userMessage);
    // Encode message for URL
    let encodedMessage = encodeURIComponent(userMessage);

    fetch(`https://vnit-ai-hackathon-production.up.railway.app/chatbot_response/?message=${encodedMessage}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById("chat-output").innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;
    })
    .catch(error => console.error("Error:", error));

    document.getElementById("user-input").value = "";
}
