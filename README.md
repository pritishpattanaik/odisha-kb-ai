# 🏝 Odisha Tourism AI Chatbot

A production-ready **AI-powered tourism chatbot** for Odisha.  
This project combines **Dialogflow (guided menus)** with a **FastAPI backend + Vector DB (Chroma + Sentence Transformers)** to provide both structured answers (menus & FAQs) and unstructured knowledge base responses.

---

## 🚀 Features
- Guided menu navigation using **Dialogflow Intents**
- Sub-menus for **Puri, Bhubaneswar, Chilika Lake, Hotels, Flights, Astrology**
- **Webhook integration** with FastAPI → answers questions from a **local vector DB**
- Knowledge base powered by **Sentence Transformers (`all-MiniLM-L6-v2`) + ChromaDB**
- Deployable widget for websites (floating chat window)
- Extensible: add more Odisha FAQs, RSS feeds, Wikipedia pages, or government advisories

---

## 📂 Project Structure

odisha-tourism-chatbot/
│── data/                # Knowledge base files (txt, RSS, wiki dumps)
│   ├── rss/             # Odisha news RSS feeds
│   ├── wiki/            # Wikipedia pages
│   ├── gov/             # Tourism advisories
│   └── faq/             # Odisha FAQs
│
│── vectorstore/         # Persisted ChromaDB embeddings
│── ingest.py            # Script to index data into Chroma
│── server.py            # FastAPI backend with /ask and webhook endpoint
│── requirements.txt     # Python dependencies
│── templates/index.html # (Optional) Web frontend
│── static/              # JS/CSS for frontend widget
│── dialogflow/          # OdishaTourismBot.zip (Dialogflow agent export)
│── README.md            # Documentation

---

## ⚙️ Setup

### 1️⃣ Clone repo & create venv
```bash
git clone https://github.com/your-org/odisha-tourism-chatbot.git
cd odisha-tourism-chatbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

2️⃣ Prepare vector DB

python ingest.py

This creates embeddings in ./vectorstore.

3️⃣ Run FastAPI server

uvicorn server:app --reload --port 8890

4️⃣ Test API

curl -X POST http://127.0.0.1:8890/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Tell me about Chilika Lake"}'


⸻

🤖 Dialogflow Setup
	1.	Go to Dialogflow Console.
	2.	Create new Agent → OdishaTourismBot.
	3.	Navigate → Settings → Export and Import → Restore from ZIP.
	4.	Upload dialogflow/OdishaTourismBot.zip.

This will import:
	•	Welcome Intent → “Namaskar! Welcome to Odisha Tourism. Choose an option:”
	•	Intents for Puri, Bhubaneswar, Chilika, Hotels, Flights, Astrology
	•	Fallback Intent → calls your FastAPI webhook

⸻

🔗 Webhook Integration
	1.	In Dialogflow → Fulfillment → Enable Webhook.
	2.	Set URL:

https://yourdomain.com/webhook

	3.	Deploy your FastAPI app with HTTPS (e.g., Nginx + Gunicorn + Certbot).

⸻

🌐 Website Integration
	1.	In Dialogflow → Integrations → Web Demo.
	2.	Copy iframe snippet.
	3.	Paste into your website <body> to show the chatbot widget.

Example:

<iframe
  allow="microphone;"
  width="350"
  height="430"
  src="https://console.dialogflow.com/api-client/demo/embedded/YOUR-AGENT-ID">
</iframe>


⸻

🛠 Technology Stack
	•	Dialogflow ES → Menus & guided flows
	•	FastAPI → Webhook + KB retrieval
	•	ChromaDB → Vector store
	•	SentenceTransformers → Local embeddings
	•	Python 3.11+
	•	Frontend Widget → Dialogflow iframe / custom React widget

⸻

📌 Next Steps
	•	Add Hindi & Odia language intents
	•	Expand KB with more FAQs
	•	Add voice support (WebRTC + TTS + STT)
	•	Deploy on GCP/AWS/Azure

⸻

👥 Authors
	•	Pritish Pattanaik – Lead Developer & Architect
	•	Odisha Tourism AI Team

⸻

📜 License

Apache 2.0
