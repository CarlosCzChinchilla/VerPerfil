from flask import Flask, request, jsonify
from models import XMLProcessor
import os

app = Flask(__name__)

@app.route('/procesar-mensajes', methods=['POST'])
def procesar_mensajes():
    archivo = request.files['archivo']
    if archivo:
        # Crear la carpeta 'data' si no existe
        if not os.path.exists('data'):
            os.makedirs('data')
        
        # Guarda el archivo en la carpeta 'data'
        ruta_archivo = os.path.join('data', archivo.filename)
        archivo.save(ruta_archivo)
        
        # Procesa el archivo usando XMLProcessor
        procesador = XMLProcessor()
        procesador.cargar_archivo(ruta_archivo)
        
        # Lee los mensajes
        mensajes = procesador.leer_mensajes()
        
        # Genera el archivo de respuesta XML
        respuesta_xml = procesador.generar_respuesta_xml(mensajes)
        
        # Devuelve el diccionario y los mensajes procesados
        return jsonify({
            "respuesta_xml": respuesta_xml,
            "mensajes": mensajes
        }), 200
    else:
        return jsonify({"error": "Archivo no proporcionado."}), 400

@app.route('/consultar-datos', methods=['GET'])
def consultar_datos():
    procesador = XMLProcessor()
    mensajes = procesador.leer_mensajes()
    return jsonify(mensajes), 200

@app.route('/resumen-por-fecha', methods=['POST'])
def resumen_por_fecha():
    fecha = request.json.get('fecha')
    if fecha:
        procesador = XMLProcessor()
        mensajes = procesador.leer_mensajes()
        mensajes_fecha = [mensaje for mensaje in mensajes if fecha in mensaje]
        respuesta_xml = procesador.generar_respuesta_xml(mensajes_fecha)
        return jsonify({"respuesta_xml": respuesta_xml, "mensajes": mensajes_fecha}), 200
    else:
        return jsonify({"error": "Fecha no proporcionada."}), 400

@app.route('/resumen-por-rango', methods=['POST'])
def resumen_por_rango():
    fecha_inicio = request.json.get('fecha_inicio')
    fecha_fin = request.json.get('fecha_fin')
    if fecha_inicio and fecha_fin:
        procesador = XMLProcessor()
        mensajes = procesador.leer_mensajes()
        mensajes_rango = [mensaje for mensaje in mensajes if fecha_inicio <= mensaje.split()[2] <= fecha_fin]
        respuesta_xml = procesador.generar_respuesta_xml(mensajes_rango)
        return jsonify({"respuesta_xml": respuesta_xml, "mensajes": mensajes_rango}), 200
    else:
        return jsonify({"error": "Fechas no proporcionadas."}), 400

if __name__ == '__main__':
    app.run(debug=True)