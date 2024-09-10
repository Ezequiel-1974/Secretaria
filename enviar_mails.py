from tkinter import *
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo():
    remitente = entrada_remitente.get()
    destinatario = entrada_destinatario.get()
    asunto = entrada_asunto.get()
    mensaje = texto_mensaje.get("1.0", END)
    
    try:
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = destinatario
        msg['Subject'] = asunto
        msg.attach(MIMEText(mensaje, 'plain'))
        
        # Configura tu servidor SMTP (por ejemplo, Gmail)
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, entrada_contrasena.get())  # Usa aquí la contraseña de aplicación
        servidor.sendmail(remitente, destinatario, msg.as_string())
        servidor.quit()
        
        messagebox.showinfo("Éxito", "Correo enviado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo enviar el correo. Error: {e}")

# Crear la ventana raíz
raiz = Tk()
raiz.title("Enviar Correo")

# Etiquetas y entradas
Label(raiz, text="Remitente:").grid(row=0, column=0, padx=10, pady=5)
entrada_remitente = Entry(raiz, width=40)
entrada_remitente.grid(row=0, column=1, padx=10, pady=5)

Label(raiz, text="Contraseña: (Contraseña de Aplicación)").grid(row=1, column=0, padx=10, pady=5)
entrada_contrasena = Entry(raiz, show='*', width=40)
entrada_contrasena.grid(row=1, column=1, padx=10, pady=5)

Label(raiz, text="Destinatario:").grid(row=2, column=0, padx=10, pady=5)
entrada_destinatario = Entry(raiz, width=40)
entrada_destinatario.grid(row=2, column=1, padx=10, pady=5)

Label(raiz, text="Asunto:").grid(row=3, column=0, padx=10, pady=5)
entrada_asunto = Entry(raiz, width=40)
entrada_asunto.grid(row=3, column=1, padx=10, pady=5)

Label(raiz, text="Mensaje:").grid(row=4, column=0, padx=10, pady=5)
texto_mensaje = Text(raiz, width=50, height=10)
texto_mensaje.grid(row=4, column=1, padx=10, pady=5)

# Botón para enviar
boton_enviar = Button(raiz, text="Enviar", command=enviar_correo)
boton_enviar.grid(row=5, column=1, pady=10)

# Iniciar el bucle principal de la ventana
raiz.mainloop()
