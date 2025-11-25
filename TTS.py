import pyttsx3
import threading
import tempfile
import os

class TextToSpeech:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 180)  
            self.engine.setProperty('volume', 0.9)  
            
            voices = self.engine.getProperty('voices')
            portuguese_voices = []
            
            for voice in voices:
                if 'portuguese' in voice.name.lower() or 'pt' in voice.id.lower():
                    portuguese_voices.append(voice)
                    print(f"Voz PT encontrada: {voice.name} - {voice.id}")
            
            if portuguese_voices:

                for voice in portuguese_voices:
                    if 'female' in voice.name.lower() or 'mulher' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        print(f"Voz selecionada: {voice.name}")
                        break
                else:
                    self.engine.setProperty('voice', portuguese_voices[0].id)
                    print(f"Voz selecionada: {portuguese_voices[0].name}")
            else:
                print("Nenhuma voz em português encontrada. Usando voz padrão.")
                
        except Exception as e:
            print(f"Erro ao inicializar TTS: {e}")

            self.engine = None

    def falar(self, texto):
        def falar_thread():
            try:
                if self.engine:
                    self.engine.say(texto)
                    self.engine.runAndWait()
                else:

                    self.falar_fallback(texto)
            except Exception as e:
                print(f"Erro no TTS: {e}")

                self.falar_fallback(texto)
        
        thread = threading.Thread(target=falar_thread)
        thread.daemon = True
        thread.start()

    def falar_fallback(self, texto):
        """Fallback usando comando de voz do sistema operacional"""
        try:
            texto_limpo = texto.replace('"', "'").replace('`', "'")
            
            if os.name == 'nt':  # Windows
                import win32com.client
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak(texto_limpo)
            else:  
                import subprocess

                for command in ['espeak', 'say', 'spd-say']:
                    try:
                        if command == 'espeak':
                            subprocess.run(['espeak', '-v', 'pt-br', texto_limpo], check=True)
                        elif command == 'say':
                            subprocess.run(['say', texto_limpo], check=True)
                        elif command == 'spd-say':
                            subprocess.run(['spd-say', texto_limpo], check=True)
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
                else:
                    print("Nenhum sintetizador de voz encontrado no sistema")
                    
        except Exception as e:
            print(f"Erro no fallback TTS: {e}")