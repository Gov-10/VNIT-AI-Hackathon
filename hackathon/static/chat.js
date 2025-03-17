document.getElementById("sendBtn").addEventListener("click", function() {
    let userMessage = document.getElementById("userInput").value;
    
    fetch("/chatbot-response/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("chatbox").innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;
    });
});
