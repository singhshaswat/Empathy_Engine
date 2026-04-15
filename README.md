# 🎭 Emppathy Engine – Emotion-Aware Text-to-Speech

Give your app a **human-like voice**.  
Empathy Engine analyzes input text and generates speech by adjusting **emotion, rate, and volume**.

---

## 🚀 Features

- 🧠 Emotion Detection (happy, frustrated, neutral, surprised)
- 🔊 Dynamic voice modulation (rate + volume)
- 🌐 Flask-based web interface
- 🎧 Offline Text-to-Speech using pyttsx3
- 🧹 Auto cleanup of old audio files

---

## 📂 Project Structure
```bash
Empathy_Engine/
├── .gitignore
├── app.py
├── engine.py
├── outputs/
├── templates/
│ └── index.html
├── static/
│ └── style.css
```
---

## ⚙️ Installation

```bash
git clone https://github.com/singhshaswat/Empathy_Engine.git
cd Empathy_Engine
pip install flask pyttsx3 vaderSentiment
```
---

## ▶️ Run the App

```bash
python app.py
```
## Then open:
http://127.0.0.1:5000

---

## 🧠 How It Works

User enters text in UI
Emotion is detected using sentiment analysis
A voice profile is built (rate, volume, tone)
Speech is generated using pyttsx3
Audio is played in browser

---

## 🎯 Emotion Mapping
| Emotion    | Behavior         |
| ---------- | ---------------- |
| Happy      | Faster + louder  |
| Frustrated | Slower + softer  |
| Neutral    | Balanced         |
| Surprised  | Fast + energetic |

---

## 🛠 Tech Stack
Python
Flask
pyttsx3
VADER Sentiment Analysis
HTML + CSS

---

## ⚠️ Notes
Works offline (no API needed)
Voice depends on system voices
Make sure pyttsx3 is installed correctly

---

## 💡 Future Improvements
ElevenLabs / API-based voices
Voice selection dropdown
Deployment (Render / AWS)

---

## 👨‍💻 Author
Shaswat Singh
CSE @ IIIT Nagpur
