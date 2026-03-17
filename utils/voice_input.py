def transcribe_from_microphone() -> str:
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            audio = recognizer.listen(mic, timeout=5)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            return f"Speech API error: {e}"
    except ImportError:
        return "Voice input unavailable: pyaudio not installed."
    except Exception as e:
        return f"Microphone error: {e}"
