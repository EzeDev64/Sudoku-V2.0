import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox

class EnvioCorreo:
    def __init__(self,codigo,correo):
        # 1. Configuración de credenciales y servidor (Ejemplo con Gmail)
        self.remitente = "ezeprocb2005@gmail.com"
        # ¡OJO! Esta contraseña debe ser una "Contraseña de aplicación" generada en tu cuenta de Google
        self.password = "brsk mjjv lual xekg" 
        
        self.destinatario = correo
        self.smtp_server = "smtp.gmail.com"
        self.port = 587  # Puerto estándar para TLS
        
        # 2. Ejecutar el envío de forma inmediata al iniciar la clase
        self.enviar_hello_world(codigo)

    def enviar_hello_world(self,codigo):
        try:
            # 3. Crear la estructura del mensaje
            msg = MIMEMultipart()
            msg['From'] = self.remitente
            msg['To'] = self.destinatario
            msg['Subject'] = "Código de Acceso - Sudoku 2026"
            
            # Cuerpo del mensaje
            cuerpo_mensaje = f"Codigo de acceso para iniciar sesión: {codigo}"
            msg.attach(MIMEText(cuerpo_mensaje, 'plain'))
            
            # 4. Conectarse de forma segura al servidor SMTP
            print(f"Conectando al servidor de correo para {self.destinatario}...")
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.starttls()  # Cifrado seguro
            
            # Iniciar sesión y enviar
            server.login(self.remitente, self.password)
            server.sendmail(self.remitente, self.destinatario, msg.as_string())
            
            # Cerrar conexión
            server.quit()
            print("Correo enviado exitosamente de manera automatizada.")
            
        except Exception as e:
            messagebox.showinfo("Sudoku","Error al enviar el correo")
            print(f"Error crítico al intentar enviar el correo: {e}")

# --- Cómo ejecutarla en tu programa ---
if __name__ == "__main__":
    # Solo con instanciar la clase, el constructor __init__ se encarga de todo el flujo
    correo_sistema = EnvioCorreo()