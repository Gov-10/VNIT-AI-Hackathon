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

    // let encodedMessage = encodeURIComponent(userMessage);

    let apiUrl = `https://vnit-ai-hackathon-production.up.railway.app/chatbot_response/?message=${encodeURIComponent(userMessage)}`;
console.log("API URL:", apiUrl); // Debugging

fetch(apiUrl, {
    method: "GET",
    mode: "cors",
    headers: {
        "Content-Type": "application/json",
    }
})
.then(response => {
    console.log("Response received:", response);
    if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.status} - ${response.statusText}`);
    }
    return response.json();
})
.then(data => {
    console.log("Response data:", data);
    document.getElementById("chat-output").innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;
})
.catch(error => console.error("Fetch error:", error));

    document.getElementById("user-input").value = "";
}
