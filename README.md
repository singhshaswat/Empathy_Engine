# 🎭 Empathy Engine – Emotion-Aware Text-to-Speech

**Give your AI a human voice.**  
The Empathy Engine dynamically adjusts speech rate, volume, and vocal tone based on the emotional content of input text. It detects sentiment (happy, frustrated, surprised, neutral) and modulates TTS parameters to produce more natural, expressive speech.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

- **Sentiment Analysis**: Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) to classify text into `happy`, `frustrated`, `surprised`, or `neutral`.
- **Intensity Scaling**: Exclamation marks and question marks amplify the intensity, making modulation more pronounced.
- **Voice Modulation**:
  - **Rate** (words per minute) – faster for excited/surprised, slower for frustrated.
  - **Volume** – louder for happy/surprised, softer for frustrated.
  - **Voice Index** – switches between available system voices to add tonal variety.
- **Web Interface**: Simple, responsive UI for instant testing.
- **Automatic Cleanup**: Keeps only the 10 most recent audio files to manage disk space.
- **Offline TTS**: Uses `pyttsx3` – no API keys required.

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

---

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/singhshaswat/empathy-engine.git
   cd empathy-engine