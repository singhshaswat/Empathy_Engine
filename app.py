"""Flask web interface for Empathy Engine."""

from pathlib import Path

from flask import Flask, render_template, request, send_from_directory, url_for

from engine import OUTPUT_DIR, build_profile, detect_emotion, synthesize_speech

app = Flask(__name__)


@app.route("/audio/<path:filename>")
def audio(filename: str):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=False)


@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    emotion = None
    intensity_display = None
    rate = None
    volume = None
    label = None
    audio_url = None
    error = None

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        if not text:
            error = "Please enter some text."
        else:
            emotion, intensity, _scores = detect_emotion(text)
            profile = build_profile(emotion, intensity)
            filename = synthesize_speech(text, profile)
            audio_url = url_for("audio", filename=filename)
            intensity_display = f"{intensity:.2f}"
            rate = profile.rate
            volume = f"{profile.volume:.2f}"
            label = profile.label

    return render_template(
        "index.html",
        text=text,
        emotion=emotion,
        intensity_display=intensity_display,
        rate=rate,
        volume=volume,
        label=label,
        audio_url=audio_url,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)