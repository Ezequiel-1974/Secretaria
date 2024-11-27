from tkinter import *
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import threading

# Función para obtener docentes filtrados (simulación básica; idealmente debe consultarse en una base de datos)
import mysql.connector

def obtener_docentes_filtrados(carrera, ano, division, materia):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="escuela"
    )
    cursor = conexion.cursor()
    
    consulta = """
        SELECT d.email
        FROM docente d
        JOIN materia m ON m.nombre = d.escalafon
        WHERE d.carrera = %s
          AND d.ano = %s
          AND d.division = %s
          AND m.nombre = %s;
    """
    parametros = (carrera, ano, division, materia)
    cursor.execute(consulta, parametros)
    correos = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conexion.close()
    
    return correos


# Función para iniciar el temporizador
def iniciar_temporizador(duracion_horas, destinatario):
    tiempo_limite = datetime.datetime.now() + datetime.timedelta(hours=duracion_horas)
    threading.Thread(target=verificar_tiempo_respuesta, args=(tiempo_limite, destinatario)).start()

def verificar_tiempo_respuesta(tiempo_limite, destinatario):
    while datetime.datetime.now() < tiempo_limite:
        # Espera activa hasta que se cumple el tiempo límite
        pass
    # Notificación de tiempo vencido (en una versión avanzada, enviaría un aviso o actualizaría el estado)
    messagebox.showinfo("Tiempo Vencido", f"El tiempo de respuesta para {destinatario} ha expirado.")

def enviar_correo():
    # Obtener datos de los filtros
    carrera = entrada_carrera.get()
    ano = entrada_ano.get()
    division = entrada_division.get()
    materia = entrada_materia.get()
    docentes = obtener_docentes_filtrados(carrera, ano, division, materia)

    # Configuración de correo y envío a cada destinatario filtrado
    for destinatario in docentes:
        remitente = entrada_remitente.get()
        asunto = entrada_asunto.get()
        mensaje = texto_mensaje.get("1.0", END)
        
        try:
            msg = MIMEMultipart()
            msg['From'] = remitente
            msg['To'] = destinatario
            msg['Subject'] = asunto
            msg.attach(MIMEText(mensaje, 'plain'))

            # Configuración del servidor SMTP (e.g., Gmail)
            servidor = smtplib.SMTP('smtp.gmail.com', 587)
            servidor.starttls()
            servidor.login(remitente, entrada_contrasena.get())
            servidor.sendmail(remitente, destinatario, msg.as_string())
            servidor.quit()
            
            # Inicia el temporizador para seguimiento de la respuesta del destinatario
            iniciar_temporizador(24, destinatario)  # 24 horas para responder
            messagebox.showinfo("Éxito", f"Correo enviado a {destinatario}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el correo a {destinatario}. Error: {e}")

# Configuración de la ventana principal de Tkinter y la interfaz gráfica
raiz = Tk()
raiz.title("Enviar Correo")

# Campos de filtro: Carrera, Año, División, Materia
Label(raiz, text="Carrera:").grid(row=0, column=0, padx=10, pady=5)
entrada_carrera = Entry(raiz, width=40)
entrada_carrera.grid(row=0, column=1, padx=10, pady=5)

Label(raiz, text="Año:").grid(row=1, column=0, padx=10, pady=5)
entrada_ano = Entry(raiz, width=40)
entrada_ano.grid(row=1, column=1, padx=10, pady=5)

Label(raiz, text="División:").grid(row=2, column=0, padx=10, pady=5)
entrada_division = Entry(raiz, width=40)
entrada_division.grid(row=2, column=1, padx=10, pady=5)

Label(raiz, text="Materia:").grid(row=3, column=0, padx=10, pady=5)
entrada_materia = Entry(raiz, width=40)
entrada_materia.grid(row=3, column=1, padx=10, pady=5)

# Campos de remitente y destinatario
Label(raiz, text="Remitente:").grid(row=4, column=0, padx=10, pady=5)
entrada_remitente = Entry(raiz, width=40)
entrada_remitente.grid(row=4, column=1, padx=10, pady=5)

Label(raiz, text="Contraseña: (Contraseña de Aplicación)").grid(row=5, column=0, padx=10, pady=5)
entrada_contrasena = Entry(raiz, show='*', width=40)
entrada_contrasena.grid(row=5, column=1, padx=10, pady=5)

Label(raiz, text="Asunto:").grid(row=6, column=0, padx=10, pady=5)
entrada_asunto = Entry(raiz, width=40)
entrada_asunto.grid(row=6, column=1, padx=10, pady=5)

Label(raiz, text="Mensaje:").grid(row=7, column=0, padx=10, pady=5)
texto_mensaje = Text(raiz, width=50, height=10)
texto_mensaje.grid(row=7, column=1, padx=10, pady=5)

# Botón de envío de correo
boton_enviar = Button(raiz, text="Enviar", command=enviar_correo)
boton_enviar.grid(row=8, column=1, pady=10)

# Iniciar el bucle principal de la ventana
raiz.mainloop()