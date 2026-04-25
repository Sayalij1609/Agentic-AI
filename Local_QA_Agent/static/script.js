async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const historyList = document.getElementById("history");

    const query = input.value;

    if (!query) return;

    // Show user message
    chatBox.innerHTML += `<div class="message user">${query}</div>`;
    input.value = "";

    // Show loading
    chatBox.innerHTML += `<div class="message bot" id="loading">Typing...</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    const response = await fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: query })
    });

    const data = await response.json();

    // Remove loading
    document.getElementById("loading").remove();

    // Show bot response
    chatBox.innerHTML += `<div class="message bot">${data.answer}</div>`;

    // Update history sidebar
    historyList.innerHTML = "";
    data.history.forEach(item => {
        historyList.innerHTML += `<li>${item.user}</li>`;
    });

    chatBox.scrollTop = chatBox.scrollHeight;
}