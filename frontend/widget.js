const API_URL = "http://127.0.0.1:8890/ask"; // change to your backend URL

const bubble = document.getElementById("chatbot-bubble");
const container = document.getElementById("chatbot-container");
const closeBtn = document.getElementById("close-btn");
const sendBtn = document.getElementById("send-btn");
const input = document.getElementById("chat-input");
const messages = document.getElementById("chat-messages");

bubble.addEventListener("click", () => {
  container.classList.remove("hidden");
  bubble.style.display = "none";
});

closeBtn.addEventListener("click", () => {
  container.classList.add("hidden");
  bubble.style.display = "flex";
});

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", e => {
  if (e.key === "Enter") sendMessage();
});

function appendMessage(text, cls) {
  const div = document.createElement("div");
  div.className = "msg " + cls;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;
  appendMessage(text, "user");
  input.value = "";

  try {
    const resp = await fetch(API_URL, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question: text})
    });
    const data = await resp.json();
    appendMessage(data.answer, "bot");
  } catch (err) {
    appendMessage("⚠️ Error connecting to server.", "bot");
  }
}
