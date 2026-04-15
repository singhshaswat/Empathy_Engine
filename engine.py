"""Empathy Engine: emotion detection and voice modulation logic."""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

try:
    import pyttsx3
except ImportError as exc:
    raise SystemExit("pyttsx3 is required. Install it with: pip install pyttsx3") from exc

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except ImportError:
    SentimentIntensityAnalyzer = None

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

_analyzer = SentimentIntensityAnalyzer() if SentimentIntensityAnalyzer else None


@dataclass
class VoiceProfile:
    emotion: str
    rate: int
    volume: float
    voice_index: int
    label: str


EMOTION_PROFILES: Dict[str, VoiceProfile] = {
    "happy": VoiceProfile("happy", rate=190, volume=1.0, voice_index=0, label="bright"),
    "frustrated": VoiceProfile("frustrated", rate=150, volume=0.95, voice_index=1, label="firm"),
    "neutral": VoiceProfile("neutral", rate=170, volume=0.85, voice_index=0, label="steady"),
    "surprised": VoiceProfile("surprised", rate=205, volume=1.0, voice_index=0, label="energetic"),
}


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def detect_emotion(text: str) -> Tuple[str, float, Dict[str, float]]:
    """Return emotion label, intensity, and raw scores."""
    cleaned = _normalize_text(text)
    if not cleaned:
        return "neutral", 0.0, {"compound": 0.0, "pos": 0.0, "neg": 0.0, "neu": 1.0}

    if _analyzer is not None:
        scores = _analyzer.polarity_scores(cleaned)
        compound = scores["compound"]
        exclaim_boost = min(cleaned.count("!"), 4) * 0.04
        question_boost = min(cleaned.count("?"), 4) * 0.03
        intensity = min(1.0, abs(compound) + exclaim_boost + question_boost)

        if compound >= 0.35:
            if cleaned.count("!") >= 2 and compound >= 0.6:
                return "surprised", intensity, scores
            return "happy", intensity, scores
        if compound <= -0.35:
            return "frustrated", intensity, scores
        if cleaned.count("?") >= 2 and compound > -0.1:
            return "surprised", intensity, scores
        return "neutral", intensity, scores

    # Fallback keyword-based logic
    positive_words = {
        "great", "good", "awesome", "amazing", "happy", "love", "excellent", "nice", "wonderful"
    }
    negative_words = {
        "bad", "terrible", "awful", "angry", "frustrated", "hate", "poor", "annoyed", "sad"
    }
    words = re.findall(r"[a-z']+", cleaned.lower())
    pos = sum(w in positive_words for w in words)
    neg = sum(w in negative_words for w in words)
    exclaims = cleaned.count("!")
    questions = cleaned.count("?")
    score = pos - neg

    if score > 0:
        emotion = "happy"
    elif score < 0:
        emotion = "frustrated"
    elif questions >= 2:
        emotion = "surprised"
    else:
        emotion = "neutral"

    intensity = min(1.0, (abs(score) / max(1, len(words))) + exclaims * 0.05 + questions * 0.03)
    return emotion, intensity, {"compound": float(score), "pos": float(pos), "neg": float(neg), "neu": 0.0}


def build_profile(emotion: str, intensity: float) -> VoiceProfile:
    base = EMOTION_PROFILES.get(emotion, EMOTION_PROFILES["neutral"])

    if emotion == "happy":
        rate = int(base.rate + 20 * intensity)
        volume = min(1.0, base.volume + 0.05 * intensity)
    elif emotion == "frustrated":
        rate = int(base.rate - 20 * intensity)
        volume = max(0.6, base.volume - 0.10 * intensity)
    elif emotion == "surprised":
        rate = int(base.rate + 25 * intensity)
        volume = min(1.0, base.volume)
    else:
        rate = base.rate
        volume = base.volume

    voice_index = base.voice_index
    return VoiceProfile(base.emotion, rate=rate, volume=volume, voice_index=voice_index, label=base.label)


def cleanup_old_files(max_files: int = 10) -> None:
    """Keep only the `max_files` most recent .wav files in OUTPUT_DIR."""
    wav_files = list(OUTPUT_DIR.glob("*.wav"))
    if len(wav_files) <= max_files:
        return
    # Sort by modification time (newest first)
    wav_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    for old_file in wav_files[max_files:]:
        try:
            old_file.unlink()
        except OSError:
            pass  # ignore deletion errors


def synthesize_speech(text: str, profile: VoiceProfile) -> str:
    engine = pyttsx3.init()
    voices = engine.getProperty("voices") or []

    if voices:
        chosen_index = min(profile.voice_index, len(voices) - 1)
        engine.setProperty("voice", voices[chosen_index].id)

    engine.setProperty("rate", profile.rate)
    engine.setProperty("volume", profile.volume)

    filename = f"speech_{uuid.uuid4().hex}.wav"
    out_path = OUTPUT_DIR / filename
    engine.save_to_file(text, str(out_path))
    engine.runAndWait()
    engine.stop()

    # Auto‑cleanup: keep only the 10 most recent audio files
    cleanup_old_files(max_files=10)

    return filename