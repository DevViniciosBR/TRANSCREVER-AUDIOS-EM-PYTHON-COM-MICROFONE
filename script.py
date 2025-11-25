# pip install SpeechRecognition
# pip install pyaudio

import speech_recognition as sr

def transcrever_audio_mic():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Fala Comigo")

        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            texto = r.recognize_google(audio,Language='pt-BR')
            return texto
        except sr.UnknownValueError:
            return "Não entendi o que você disse."
        except sr.RequestError:
            print("Não foi possível conectar")
        
texto_transcrito = transcrever_audio_mic()
print(texto_transcrito)
        
