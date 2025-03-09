document.getElementById("sendBtn").addEventListener("click", async () => {
    const userMessage = document.getElementById("userInput").value;
    
    const response = await fetch("/chatbot/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `message=${encodeURIComponent(userMessage)}`,
    });

    const data = await response.json();
    document.getElementById("chatOutput").innerText = data.choices[0].message.content;
});
