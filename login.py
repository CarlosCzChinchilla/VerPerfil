from flask import request, jsonify, Blueprint
from app.models.Usuario import Usuario
from app import db
from werkzeug.exceptions import HTTPException

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/registro', methods=['POST'])
def registro():
    try:
        data = request.get_json()  # Recibe los datos en formato JSON
        print(f"Datos recibidos: {data}")  # Verifica qué datos estás recibiendo

        # Extraer los campos que el usuario ingresa
        id = data.get('id')
        nombres = data.get('nombres')
        apellidos = data.get('apellidos')
        password = data.get('password')
        email = data.get('email')

        # Validar que todos los campos obligatorios están presentes
        if not id or not nombres or not apellidos or not password or not email:
            return jsonify({'error': 'Faltan campos obligatorios'}), 400

        # Verificar si el ID o el email ya están registrados
        usuario_existente = Usuario.query.filter((Usuario.id == id) | (Usuario.email == email)).first()
        if usuario_existente:
            return jsonify({'error': 'El ID o el email ya están en uso'}), 400

        # Crear un nuevo usuario
        nuevo_usuario = Usuario(id=id, nombres=nombres, apellidos=apellidos, password=password, email=email)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({'message': 'Usuario creado exitosamente'}), 201

    except Exception as e:
        print(f"Error específico: {e}")  # Muestra el error en la consola
        db.session.rollback()  # Revertir si hay un error
        return jsonify({'error': f'Error en el registro: {str(e)}'}), 400

    
    
@login_blueprint.route('/login', methods=['POST'])
def login():
    try:
        id = request.json.get('id')
        password = request.json.get('password')

        if not id or not password:
            return jsonify({'error': 'Datos de entrada incompletos'}), 400

        # Obtener el usuario de la base de datos
        usuario = Usuario.query.filter_by(id=id).first()
        if usuario is None:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        # Comparar contraseñas en texto plano
        if usuario.password != password:
            return jsonify({'error': 'Contraseña incorrecta'}), 401

        return jsonify({'message': 'Bienvenido!'}), 200

    except HTTPException as e:
        return jsonify({'error': f'HTTP Exception: {str(e.description)}'}), e.code
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500


# Ruta para verificar datos del usuario para restablecimiento de contraseña
@login_blueprint.route('/verificar', methods=['POST'])
def verificar():
    try:
        data = request.get_json()
        print(f"Datos recibidos: {data}")  # Verifica qué datos estás recibiendo
        email = data.get('email')
        id = data.get('id')

        # Verificar si el usuario existe con el email y el registro académico proporcionados
        usuario = Usuario.query.filter_by(email=email, id=id).first()
        if usuario is None:
            return jsonify({'error': 'Correo electrónico o registro académico incorrectos'}), 404
        
        return jsonify({'message': 'Datos verificados, puede restablecer la contraseña'}), 200
    except HTTPException as e:
        return jsonify({'error': str(e.description)}), e.code
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500
    

# BUSCAR USUARIOS POR MEDIO DE ID--------------------------------------------------------------------------------------------------------------------
@login_blueprint.route('/buscar_usuario', methods=['GET'])
def buscar_usuario():
    try:
        # Obtener el ID de la solicitud y imprimirlo
        id = request.args.get('id')
        print(f"ID recibido: {id}")  # Imprimir el ID recibido

        if id is None:
            print("No se proporcionó un ID en la solicitud")
            return jsonify({'error': 'ID no proporcionado'}), 400

        # Buscar el usuario en la base de datos usando el ID proporcionado
        usuario = Usuario.query.filter_by(id=id).first()

        if usuario is None:
            # Imprimir cuando el usuario no se encuentra
            print(f"Usuario no encontrado con ID = {id}")
            return jsonify({'error': 'Usuario no encontrado'}), 404

        # Verificar que los campos nombres y apellidos no sean None
        if usuario.nombres is None or usuario.apellidos is None:
            print(f"El usuario con ID = {id} no tiene un nombre o apellido asignado")
            return jsonify({'error': 'El usuario no tiene un nombre o apellido asignado'}), 404

        # Si se encuentra el usuario, imprimir el ID, nombre y apellido del usuario
        print(f"Usuario encontrado: ID = {usuario.id}, Nombres = {usuario.nombres}, Apellidos = {usuario.apellidos}")

        # Devolver los detalles del usuario en la respuesta
        return jsonify({
            'id': usuario.id,
            'nombres': usuario.nombres,
            'apellidos': usuario.apellidos
        }), 200
    except HTTPException as e:
        # Imprimir cualquier excepción específica de HTTP
        print(f"Error HTTP: {e.description}")
        return jsonify({'error': str(e.description)}), e.code
    except Exception as e:
        # Imprimir cualquier excepción inesperada
        print(f"Error inesperado: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# Ruta para actualizar la contraseña del usuario
@login_blueprint.route('/restablecer', methods=['PUT'])
def actualizar_contrasena():
    try:
        data = request.get_json()
        id = data.get('id')
        nueva_contrasena = data.get('nueva_contrasena')

        # Verificar si el usuario existe con el email y el registro académico proporcionados
        usuario = Usuario.query.filter_by(id=id).first()
        if usuario is None:
            return jsonify({'error': 'Registro académico incorrecto'}), 404

        # Actualizar la contraseña del usuario
        usuario.password = nueva_contrasena
        db.session.commit()

        return jsonify({'message': 'Contraseña actualizada exitosamente'}), 200
    except HTTPException as e:
        return jsonify({'error': str(e.description)}), e.code
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500