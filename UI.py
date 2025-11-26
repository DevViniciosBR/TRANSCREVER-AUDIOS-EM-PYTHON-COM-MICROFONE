import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import speech_recognition as sr
from TTS import TextToSpeech
# pip install -r requirements.txt
class ZippyVoiceApp:
    def __init__(self, master):
        self.master = master
        master.title("Zippy Voice - Sistema de Transcrição")
        master.geometry("700x600")
        master.configure(bg='#2c3e50')
        
        self.tts = TextToSpeech()
        
        self.configurar_estilos()
        
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.frame_instrucoes = ttk.Frame(self.notebook, style='Color.TFrame')
        self.notebook.add(self.frame_instrucoes, text="Instruções")
        
        self.frame_principal = ttk.Frame(self.notebook, style='Color.TFrame')
        self.notebook.add(self.frame_principal, text="Transcrição de Voz")
        
        self.frame_futuro = ttk.Frame(self.notebook, style='Color.TFrame')
        self.notebook.add(self.frame_futuro, text="Text-to-Speech")
        
        self.criar_aba_instrucoes()
        self.criar_aba_principal()
        self.criar_aba_tts()
        
        self.status_var = tk.StringVar()
        self.status_var.set("Sistema pronto - Conectado")
        self.status_bar = ttk.Label(master, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, style='Status.TLabel')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def configurar_estilos(self):
        self.style = ttk.Style()
        
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('Color.TFrame', background='#ecf0f1')
        self.style.configure('TLabel', font=('Arial', 10), background='#ecf0f1')
        self.style.configure('Title.TLabel', font=('Arial', 14, 'bold'), 
                           background='#ecf0f1', foreground='#2c3e50')
        self.style.configure('Header.TLabel', font=('Arial', 11, 'bold'),
                           background='#ecf0f1', foreground='#34495e')
        self.style.configure('Status.TLabel', font=('Arial', 9), 
                           background='#bdc3c7', foreground='#2c3e50')
        
        self.style.configure('TLabelframe', background='#ecf0f1')
        self.style.configure('TLabelframe.Label', background='#ecf0f1', 
                           foreground='#2c3e50', font=('Arial', 10, 'bold'))

    def criar_aba_instrucoes(self):
        titulo = ttk.Label(self.frame_instrucoes, 
                          text="Zippy Voice - Sistema de Transcrição", 
                          style='Title.TLabel')
        titulo.pack(pady=15)
        
        instrucoes_text = """
                            RECURSOS DISPONÍVEIS:
                            Transcrição em tempo real
                            Sistema Text-to-Speech (TTS)
                            Tratamento de erros robusto

                            💡 DICAS:
                            • Fale claramente e em ambiente silencioso
                            • Verifique as permissões do microfone
                            • Use fones de ouvido para melhor experiência TTS
                            """
        
        text_area = scrolledtext.ScrolledText(
            self.frame_instrucoes, 
            wrap=tk.WORD, 
            width=70, 
            height=25,
            font=('Arial', 10),
            bg='#ffffff',
            fg='#2c3e50',
            relief='solid',
            bd=1
        )
        text_area.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)
        text_area.insert(tk.INSERT, instrucoes_text)
        text_area.config(state=tk.DISABLED)

    def criar_aba_principal(self):
        content_frame = ttk.Frame(self.frame_principal, style='Color.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
        titulo = ttk.Label(content_frame, 
                          text="Sistema de Transcrição de Voz", 
                          style='Title.TLabel')
        titulo.pack(pady=(0, 20))
        
        self.mic_status_frame = ttk.LabelFrame(content_frame, 
                                              text="🎤 Status do Microfone",
                                              style='TLabelframe')
        self.mic_status_frame.pack(fill=tk.X, pady=8)

        self.mic_status_label = ttk.Label(self.mic_status_frame, 
                                         text="Verificando status do microfone...",
                                         style='Header.TLabel')
        self.mic_status_label.pack(pady=8)
        
        ttk.Button(
            self.mic_status_frame, 
            text="Verificar Microfone", 
            command=self.verificar_microfone
        ).pack(pady=5)
        control_frame = ttk.LabelFrame(content_frame, 
                                      text="Controles de Gravação",
                                      style='TLabelframe')
        control_frame.pack(fill=tk.X, pady=12)
        
        self.record_button = ttk.Button(
            control_frame, 
            text="🎤 Iniciar Gravação", 
            command=self.iniciar_gravacao,
            style='TButton'
        )
        self.record_button.pack(pady=12)
        
        self.status_label = ttk.Label(control_frame, 
                                     text="Pronto para gravar",
                                     style='Header.TLabel')
        self.status_label.pack(pady=5)
        
        result_frame = ttk.LabelFrame(content_frame, 
                                     text="Resultado da Transcrição",
                                     style='TLabelframe')
        result_frame.pack(fill=tk.BOTH, expand=True, pady=8)
        
        self.result_text = scrolledtext.ScrolledText(
            result_frame, 
            wrap=tk.WORD, 
            height=10,
            font=('Arial', 10),
            bg='#ffffff',
            fg='#2c3e50',
            relief='solid',
            bd=1
        )
        self.result_text.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)
        
        self.master.after(100, self.verificar_microfone)

    def criar_aba_tts(self):
        content_frame = ttk.Frame(self.frame_futuro, style='Color.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        titulo = ttk.Label(content_frame, 
                          text="Sistema Text-to-Speech", 
                          style='Title.TLabel')
        titulo.pack(pady=20)
        
        descricao = ttk.Label(
            content_frame, 
            text="Digite o texto abaixo e clique em 'Falar Texto' para ouvir a síntese de voz:",
            style='Header.TLabel',
            justify=tk.CENTER
        )
        descricao.pack(pady=10)
        
        tts_frame = ttk.LabelFrame(content_frame, 
                                  text="📝 Texto para Conversão",
                                  style='TLabelframe')
        tts_frame.pack(fill=tk.BOTH, expand=True, pady=12)
        
        self.tts_text = scrolledtext.ScrolledText(
            tts_frame, 
            wrap=tk.WORD,
            height=12,
            font=('Arial', 11),
            bg='#ffffff',
            fg='#2c3e50',
            relief='solid',
            bd=1
        )
        self.tts_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        button_frame = ttk.Frame(tts_frame, style='Color.TFrame')
        button_frame.pack(fill=tk.X, pady=5)
        ttk.Button(
            button_frame,
            text="Falar Texto",
            command=self.executar_tts
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame,
            text="Limpar",
            command=self.limpar_tts
        ).pack(side=tk.LEFT, padx=5)
        
        texto_exemplo = """Olá! Este é o sistema Zippy Voice. 
Digite seu texto aqui e clique em 'Falar Texto' para ouvir a síntese de voz.

Exemplo: Bem-vindo ao sistema de transcrição e síntese de voz mais moderno!"""
        self.tts_text.insert(tk.INSERT, texto_exemplo)

    def executar_tts(self):
        texto = self.tts_text.get(1.0, tk.END).strip()
        if texto:
            try:
                self.status_var.set("Sintetizando voz...")
                self.tts.falar(texto)
                self.status_var.set("Síntese de voz concluída")
            except Exception as e:
                messagebox.showerror("Erro TTS", f"Erro ao sintetizar voz: {str(e)}")
                self.status_var.set("Erro na síntese de voz")
        else:
            messagebox.showwarning("Texto Vazio", "Digite algum texto para sintetizar.")

    def limpar_tts(self):
        self.tts_text.delete(1.0, tk.END)

    def verificar_microfone(self):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                self.mic_status_label.config(text="Microfone detectado e funcionando")
                self.status_var.set("Microfone: Conectado")
                return True
        except OSError as e:
            if "No default input device available" in str(e):
                self.mic_status_label.config(text="Microfone não detectado")
                self.status_var.set("Microfone: Não detectado")
                messagebox.showwarning(
                    "Microfone Não Detectado", 
                    """Nenhum microfone foi encontrado.

Soluções:
• Verifique se o microfone está conectado
• Conceda permissão de áudio
• Configure um dispositivo padrão

O sistema continuará funcionando, mas a gravação não estará disponível."""
                )
                return False
            else:
                self.mic_status_label.config(text="⚠️ Erro na verificação do microfone")
                self.status_var.set("Microfone: Erro na verificação")
                return False

    def transcrever_audio(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                self.status_label.config(text="Ouvindo")
                self.status_var.set(" Gravando áudio")
                self.master.update()
                
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=10, phrase_time_limit=15)

            self.status_label.config(text="Processando áudio")
            self.status_var.set("Processando áudio")
            self.master.update()

            texto = r.recognize_google(audio, language='pt-BR')
            return texto

        except sr.WaitTimeoutError:
            return "Tempo de gravação excedido. Clique em 'Iniciar Gravação' para tentar novamente."
        except sr.UnknownValueError:
            return "Não foi possível entender o áudio. Tente falar mais claramente."
        except sr.RequestError as e:
            return f"Erro de conexão: {str(e)}"
        except OSError as e:
            if "No default input device available" in str(e):
                return "❌ ERRO: Microfone não detectado. Verifique as conexões e permissões."
            return f"Erro de hardware: {str(e)}"
        finally:
            self.status_var.set("✅ Processamento concluído")

    def iniciar_gravacao(self):
        if not self.verificar_microfone():
            messagebox.showerror(
                "Microfone Indisponível", 
                "Não é possível iniciar a gravação. Microfone não detectado."
            )
            return
            
        self.record_button.config(state=tk.DISABLED)
        self.result_text.delete(1.0, tk.END)
        self.master.update()

        try:
            resultado = self.transcrever_audio()

            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.result_text.insert(tk.END, f"[{timestamp}] {resultado}")
            self.result_text.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro inesperado:\n{str(e)}")
        finally:
            self.record_button.config(state=tk.NORMAL)
            self.status_label.config(text="✅ Pronto para gravar")
            self.status_var.set("✅ Sistema pronto")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZippyVoiceApp(root)

    root.mainloop()
