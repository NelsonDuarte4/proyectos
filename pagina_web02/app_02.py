from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message    # importaciones para la funcionalidad de correo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_02 import SolicitudPuntos, User, Empleado
from werkzeug.security import check_password_hash
from datetime import datetime

DB_URL = "sqlite:///usuarios.db"

app = Flask(__name__)
app.secret_key = "cambia_esto_por_una_clave_segura"

# Configuración del correo del administrador que enviará los correos a los empleados
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'carlos.gomez.fidelix@gmail.com'    # correo de donde se envían los demás mails
app.config['MAIL_PASSWORD'] = 'yfvk ulzt yndn qfyh'  # contraseña de aplicación generada del correo del administrador
app.config['MAIL_DEFAULT_SENDER'] = 'carlos.gomez.fidelix@gmail.com'

mail = Mail(app)

engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)

def obtener_usuario_por_username(username):
    db = Session()
    user = db.query(User).filter_by(username=username).first()
    db.close()
    return user

def obtener_empleado_por_id(empleado_id):
    db = Session()
    empleado = db.query(Empleado).filter_by(id=empleado_id).first()
    db.close()
    return empleado

def actualizar_puntos_empleado(empleado_id, puntos_a_descontar):
    db = Session()
    empleado = db.query(Empleado).filter_by(id=empleado_id).first()
    
    if not empleado:
        db.close()
        return False
    
    if empleado.puntos_acumulados >= puntos_a_descontar:
        empleado.puntos_acumulados -= puntos_a_descontar
        db.commit()
        db.close()
        return True
    else:
        db.close()
        return False

def enviar_correo_recompensa(empleado):
    """Envía correo simple al empleado"""
    try:
        msg = Message(
            subject="Tu recompensa está siendo procesada",
            recipients=[empleado.correo]
        )
        
        msg.body = f"""
Hola {empleado.nombre} {empleado.apellido},

Tu solicitud de recompensa está siendo procesada exitosamente.

Detalles:
- Puntos actuales: {empleado.puntos_acumulados}
- Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}

Tu recompensa será procesada en las próximas 24-48 horas.

Saludos,
Sistema de Recompensas
        """
        
        mail.send(msg)
        print(f"✓ Correo enviado a: {empleado.correo}")
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("home_02"))
    return redirect(url_for("login_02"))

@app.route("/login_02", methods=["GET", "POST"])
def login_02():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = obtener_usuario_por_username(username)

        if not user:
            flash("Usuario no existe", "error")
            return render_template("login_02.html")

        if not check_password_hash(user.password_hash, password):
            flash("Contraseña incorrecta", "error")
            return render_template("login_02.html")

        session["user_id"] = user.id
        session["username"] = user.username
        flash(f"¡Bienvenido {user.username}!", "success")
        if user.rol == "admin":
            return redirect(url_for("admin_dashboard"))  # Va a página de admin
        else:
            return redirect(url_for("home_02"))  # Va a página de empleado
            

    return render_template("login_02.html")

@app.route("/admin")
def admin_dashboard():
    # Verificamos que sea admin
    if not session.get("user_id") or session.get("rol") != "admin":
        flash("No tienes permisos para acceder", "error")
        return redirect(url_for("admin_02"))
    
    # Obtenemos todos los empleados
    db = Session()
    empleados = db.query(Empleado).all()
    db.close()
    
    return render_template("admin_02.html", 
                         username=session["username"],
                         empleados=empleados)

@app.route("/home_02")
def home_02():
    if not session.get("user_id"):
        return redirect(url_for("login_02"))
    
    user_id = session.get("user_id")
    db = Session()
    user = db.query(User).filter_by(id=user_id).first()
    
    if not user:
        db.close()
        flash("Error al cargar usuario", "error")
        return redirect(url_for("login_02"))
    
    empleado = None
    if hasattr(user, 'empleado_id') and user.empleado_id:
        empleado = db.query(Empleado).filter_by(id=user.empleado_id).first()
    
    db.close()
    
    if not empleado:
        flash("No se encontró información del empleado", "error")
        return render_template("home_02.html", username=session["username"], empleado=None)
    
    return render_template("home_02.html", 
                         username=session["username"],
                         empleado=empleado)

@app.route("/canjear", methods=["POST"])
def canjear():
    if not session.get("user_id"):
        return redirect(url_for("login_02"))
    
    user_id = session.get("user_id")
    db = Session()
    user = db.query(User).filter_by(id=user_id).first()
    
    if not user:
        db.close()
        flash("Error al cargar usuario", "error")
        return redirect(url_for("login_02"))
    
    empleado = None
    if hasattr(user, 'empleado_id') and user.empleado_id:
        empleado = db.query(Empleado).filter_by(id=user.empleado_id).first()
    
    db.close()
    
    if not empleado:
        flash("No se encontró información del empleado", "error")
        return redirect(url_for("home_02"))
    
    recompensa = request.form.get("recompensa")
    
    if recompensa:
        try:
            costo = int(recompensa)
            
            if actualizar_puntos_empleado(empleado.id, costo):
                empleado_actualizado = obtener_empleado_por_id(empleado.id)
                
                correo_enviado = enviar_correo_recompensa(empleado_actualizado)
                
                if correo_enviado:
                    flash(f"¡Recompensa canjeada! Se descontaron {costo} puntos. Correo enviado a {empleado_actualizado.correo}", "success")
                else:
                    flash(f"¡Recompensa canjeada! Se descontaron {costo} puntos. No se pudo enviar el correo.", "warning")
            else:
                flash("No tienes suficientes puntos para esta recompensa.", "error")
        except ValueError:
            flash("Valor de recompensa inválido.", "error")
    else:
        flash("Por favor, selecciona una recompensa.", "warning")
    
    return redirect(url_for("home_02"))

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    flash("Has cerrado sesión correctamente", "info")
    return redirect(url_for("login_02"))

######################################
# SECCIÓN DE SOLICITAR PUNTOS
######################################

# Definición de valores para solicitud de puntos
valores_cuadros = {
    'cuadro1': {'puntos': 800, 'descripcion': 'Llegué a tiempo durante tres meses consecutivos'},
    'cuadro2': {'puntos': 1500, 'descripcion': 'Completé el curso de atención al cliente'},
    'cuadro3': {'puntos': 2000, 'descripcion': 'Alcancé el 100% de mis objetivos del mes'},
    'cuadro4': {'puntos': 2500, 'descripcion': 'Presenté una idea que mejoró la experiencia del cliente'}
}

@app.route('/reclamar', methods=['POST'])
def reclamar():
    """Procesa el formulario, guarda la solicitud y notifica al empleado"""
    if not session.get("user_id"):
        return redirect(url_for("login_02"))
    
    cuadro_seleccionado = request.form.get('cuadro')
    empleado_id = request.form.get('empleado_id')

    if not cuadro_seleccionado:
        flash("Por favor, selecciona una opción", "warning")
        return redirect(url_for("home_02"))

    if cuadro_seleccionado not in valores_cuadros:
        flash("Selección inválida", "error")
        return redirect(url_for("home_02"))

    datos = valores_cuadros[cuadro_seleccionado]
    puntos = datos['puntos']
    descripcion = datos['descripcion']

    db = Session()

    # Verificamos si el empleado existe
    empleado = db.query(Empleado).filter_by(id=empleado_id).first()
    if not empleado:
        db.close()
        flash("Empleado no encontrado", "error")
        return redirect(url_for("home_02"))

    # Extraer datos del empleado ANTES de cerrar la sesión
    datos_empleado = {
        'correo': empleado.correo,
        'nombre': empleado.nombre,
        'apellido': empleado.apellido,
        'puntos_acumulados': empleado.puntos_acumulados
    }

    # Crear solicitud (pendiente de aprobación)
    nueva_solicitud = SolicitudPuntos(
        empleado_id=empleado.id,
        descripcion=descripcion,
        fecha_solicitud=datetime.now().date()
    )

    db.add(nueva_solicitud)
    db.commit()
    db.close()

    # Enviar correo de notificación usando los datos extraídos
    correo_enviado = enviar_correo_solicitud_puntos(datos_empleado, puntos, descripcion)
    
    if correo_enviado:
        flash(f"✓ Solicitud de {puntos} puntos registrada exitosamente. Se te notificará por correo cuando sea aprobada.", "success")
    else:
        flash(f"Solicitud registrada, pero hubo un error al enviar el correo de notificación.", "warning")

    return redirect(url_for("home_02"))




def enviar_correo_solicitud_puntos(datos_empleado, puntos, descripcion):
    """Envía correo al empleado notificando que su solicitud está pendiente"""
    try:
        msg = Message(
            subject="Solicitud de puntos recibida - Pendiente de aprobación",
            recipients=[datos_empleado['correo']]
        )
        
        msg.body = f"""
Hola {datos_empleado['nombre']} {datos_empleado['apellido']},

Tu solicitud de puntos ha sido registrada correctamente y se encuentra pendiente de autorización por parte del administrador.

Detalles de la solicitud:
- Descripción: {descripcion}
- Puntos solicitados: {puntos}
- Fecha de solicitud: {datetime.now().strftime('%d/%m/%Y %H:%M')}
- Puntos actuales: {datos_empleado['puntos_acumulados']}

Recibirás una notificación por correo cuando el administrador apruebe tu solicitud.

Saludos,
Sistema de Recompensas Fidelix
        """
        
        mail.send(msg)
        print(f"✓ Correo de solicitud enviado a: {datos_empleado['correo']}")
        return True

    except Exception as e:
        print(f"✗ Error al enviar correo: {str(e)}")
        return False
    

######################################
# SECCIÓN ADMIN EN DONDE SE MUESTRA 
#LOS DATOS Y ESTA LA SECCION APROBAR Y RECHAZAR 
######################################

def obtener_solicitudes_empleado(empleado_id, Session):
    """
    Trae todas las solicitudes de puntos de un empleado específico
    VERSIÓN PARA SQLALCHEMY PURO
    """
    db = Session()  # Crear sesión
    
    try:
        # Consulta con JOIN entre empleado y solicitud_puntos
        solicitudes = db.query(
            Empleado.nombre,
            Empleado.apellido,
            Empleado.cedula,
            SolicitudPuntos.fecha_solicitud,
            SolicitudPuntos.descripcion,
            SolicitudPuntos.puntos,
            SolicitudPuntos.id
        ).join(
            SolicitudPuntos, Empleado.id == SolicitudPuntos.empleado_id
        ).filter(
            Empleado.id == empleado_id
        ).all()
        
        if not solicitudes:
            print(f"No se encontraron solicitudes para el empleado ID: {empleado_id}")
            return []
        
        # Formatear resultados
        resultados = []
        for sol in solicitudes:
            resultados.append({
                'nombre': sol.nombre,
                'apellido': sol.apellido,
                'cedula': sol.cedula,
                'fecha': sol.fecha_solicitud.strftime('%d/%m/%Y'),
                'descripcion': sol.descripcion,
                'puntos': sol.puntos,
                'solicitud_id': sol.id
            })
        
        return resultados
        
    except Exception as e:
        print(f"Error al obtener solicitudes: {str(e)}")
        return []
    finally:
        db.close()  # IMPORTANTE: Cerrar la sesión


def obtener_todas_solicitudes_pendientes(Session):
    """
    Trae TODAS las solicitudes pendientes de TODOS los empleados
    VERSIÓN PARA SQLALCHEMY PURO
    """
    db = Session()  # Crear sesión
    
    try:
        solicitudes = db.query(
            Empleado.nombre,
            Empleado.apellido,
            Empleado.cedula,
            SolicitudPuntos.fecha_solicitud,
            SolicitudPuntos.descripcion,
            SolicitudPuntos.puntos,
            SolicitudPuntos.id,
            SolicitudPuntos.estado
        ).join(
            SolicitudPuntos, Empleado.id == SolicitudPuntos.empleado_id
        ).filter(
            SolicitudPuntos.estado == 'pendiente'
        ).order_by(
            SolicitudPuntos.fecha_solicitud.desc()
        ).all()
        
        if not solicitudes:
            print("No se encontraron solicitudes pendientes")
            return []
        
        # Formatear resultados
        resultados = []
        for sol in solicitudes:
            resultados.append({
                'nombre': sol.nombre,
                'apellido': sol.apellido,
                'cedula': sol.cedula,
                'fecha': sol.fecha_solicitud.strftime('%d/%m/%Y'),
                'descripcion': sol.descripcion,
                'puntos': sol.puntos,
                'solicitud_id': sol.id
            })
        
        return resultados
        
    except Exception as e:
        print(f"Error al obtener solicitudes: {str(e)}")
        return []
    finally:
        db.close()  # IMPORTANTE: Cerrar la sesión


@app.route('/admin_02')
def panel_admin():
    """
    Panel de administración - VERSIÓN SQLALCHEMY PURO
    """
    solicitudes = obtener_todas_solicitudes_pendientes(Session)
    admin_nombre = session.get('nombre_admin', 'Carlos Gomez')
    
    return render_template('admin.html', 
                         solicitudes=solicitudes,
                         admin_nombre=admin_nombre)


@app.route('/aprobar_solicitud/<int:solicitud_id>', methods=['POST'])
def aprobar_solicitud(solicitud_id):
    """
    Permite al admin aprobar una solicitud de puntos
    VERSIÓN PARA SQLALCHEMY PURO
    """
    db = Session()  # Crear sesión
    
    try:
        solicitud = db.query(SolicitudPuntos).filter_by(id=solicitud_id).first()
        if not solicitud:
            db.close()
            flash("Solicitud no encontrada", "error")
            return redirect(url_for('panel_admin'))

        empleado = db.query(Empleado).filter_by(id=solicitud.empleado_id).first()
        if not empleado:
            db.close()
            flash("Empleado no encontrado", "error")
            return redirect(url_for('admin_02'))

        # Obtener puntos
        puntos = solicitud.puntos

        # Sumar puntos al empleado
        empleado.puntos_acumulados += puntos
        
        # Cambiar estado de la solicitud
        solicitud.estado = "aprobada"

        # Extraer datos del empleado ANTES de cerrar la sesión
        datos_empleado = {
            'correo': empleado.correo,
            'nombre': empleado.nombre,
            'apellido': empleado.apellido,
            'cedula': empleado.cedula,
            'puntos_acumulados': empleado.puntos_acumulados
        }
        
        descripcion = solicitud.descripcion

        # Guardar cambios
        db.commit()
        db.close()

        # Enviar correo de aprobación
        enviar_correo_aprobacion(datos_empleado, puntos, descripcion)

        flash(f"✓ Solicitud #{solicitud_id} aprobada. {datos_empleado['nombre']} recibió {puntos} puntos.", "success")
        return redirect(url_for('admin_02'))
    
    except Exception as e:
        db.rollback()
        db.close()
        print(f"Error al aprobar solicitud: {str(e)}")
        flash(f"Error al aprobar la solicitud: {str(e)}", "error")
        return redirect(url_for('admin_02'))


@app.route('/rechazar_solicitud/<int:solicitud_id>', methods=['POST'])
def rechazar_solicitud(solicitud_id):
    """
    Permite al admin rechazar una solicitud
    VERSIÓN PARA SQLALCHEMY PURO
    """
    db = Session()  # Crear sesión
    
    try:
        motivo = request.form.get('motivo', 'No especificado')
        
        solicitud = db.query(SolicitudPuntos).filter_by(id=solicitud_id).first()
        if not solicitud:
            db.close()
            flash("Solicitud no encontrada", "error")
            return redirect(url_for('admin_02'))

        empleado = db.query(Empleado).filter_by(id=solicitud.empleado_id).first()
        if not empleado:
            db.close()
            flash("Empleado no encontrado", "error")
            return redirect(url_for('admin_02'))

        # Cambiar estado de la solicitud
        solicitud.estado = "rechazada"

        datos_empleado = {
            'correo': empleado.correo,
            'nombre': empleado.nombre,
            'apellido': empleado.apellido,
            'cedula': empleado.cedula,
            'puntos_acumulados': empleado.puntos_acumulados
        }
        
        puntos = solicitud.puntos
        descripcion = solicitud.descripcion

        # Guardar cambios
        db.commit()
        db.close()

        # Enviar correo
        enviar_correo_rechazo(datos_empleado, puntos, descripcion, motivo)
        
        flash(f"Solicitud #{solicitud_id} rechazada correctamente.", "warning")
        return redirect(url_for('admin_02'))
    
    except Exception as e:
        db.rollback()
        db.close()
        print(f"Error al rechazar solicitud: {str(e)}")
        flash(f"Error al rechazar la solicitud: {str(e)}", "error")
        return redirect(url_for('admin_02'))


def enviar_correo_aprobacion(datos_empleado, puntos, descripcion):
    """Envía correo al empleado notificando que su solicitud fue aprobada"""
    try:
        msg = Message(
            subject="¡Solicitud de puntos APROBADA! ✓",
            recipients=[datos_empleado['correo']]
        )
        
        msg.body = f"""
¡Hola {datos_empleado['nombre']} {datos_empleado['apellido']}!

¡Excelentes noticias! Tu solicitud de puntos ha sido APROBADA por el administrador.

Detalles:
- Descripción: {descripcion}
- Puntos otorgados: {puntos}
- Puntos totales actuales: {datos_empleado['puntos_acumulados']}
- Fecha de aprobación: {datetime.now().strftime('%d/%m/%Y %H:%M')}

¡Felicitaciones! Ya puedes usar tus puntos para canjear recompensas.

Saludos,
Sistema de Recompensas Fidelix
        """
        
        mail.send(msg)
        print(f"✓ Correo de aprobación enviado a: {datos_empleado['correo']}")
        return True

    except Exception as e:
        print(f"✗ Error al enviar correo: {str(e)}")
        return False


def enviar_correo_rechazo(datos_empleado, puntos, descripcion, motivo_rechazo=""):
    """Envía correo al empleado notificando que su solicitud fue rechazada"""
    try:
        msg = Message(
            subject="Solicitud de puntos rechazada",
            recipients=[datos_empleado['correo']]
        )
        
        msg.body = f"""
Hola {datos_empleado['nombre']} {datos_empleado['apellido']},

Lamentamos informarte que tu solicitud de puntos ha sido rechazada por el administrador.

Detalles:
- Descripción: {descripcion}
- Puntos solicitados: {puntos}
- Fecha de rechazo: {datetime.now().strftime('%d/%m/%Y %H:%M')}
{f'- Motivo del rechazo: {motivo_rechazo}' if motivo_rechazo else ''}

Si tienes dudas sobre esta decisión, puedes contactar con el administrador para más información.

Puntos actuales: {datos_empleado['puntos_acumulados']}

Saludos,
Sistema de Recompensas Fidelix
        """
        
        mail.send(msg)
        print(f"✓ Correo de rechazo enviado a: {datos_empleado['correo']}")
        return True

    except Exception as e:
        print(f"✗ Error al enviar correo: {str(e)}")
        return False

if __name__ == "__main__":
    app.run(debug=True)