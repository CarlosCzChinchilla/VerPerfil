import xml.etree.ElementTree as ET
from xml.dom import minidom
import unicodedata

# Diccionario de sentimientos
positive_words = ["bueno", "excelente", "cool", "satisfecho"]
negative_words = ["malo", "pésimo", "triste", "molesto", "decepcionado", "enojo"]

class Nodo:
    def __init__(self, nombre, atributos=None, texto=None):
        self.nombre = nombre
        self.atributos = atributos if atributos else {}
        self.texto = texto
        self.hijos = []

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

    def a_elemento(self):
        elemento = ET.Element(self.nombre, self.atributos)
        if self.texto:
            elemento.text = self.texto
        for hijo in self.hijos:
            elemento.append(hijo.a_elemento())
        return elemento

    @staticmethod
    def desde_elemento(elemento):
        nodo = Nodo(elemento.tag, elemento.attrib, elemento.text)
        for hijo in elemento:
            nodo.agregar_hijo(Nodo.desde_elemento(hijo))
        return nodo

    def a_xml(self):
        elemento = self.a_elemento()
        rough_string = ET.tostring(elemento, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    @staticmethod
    def desde_xml(xml_str):
        elemento = ET.fromstring(xml_str)
        return Nodo.desde_elemento(elemento)
    
class XMLSerializer:
    def __init__(self, archivo):
        self.archivo = archivo

    def guardar(self, nodo):
        """Guarda el nodo en un archivo XML."""
        xml_str = nodo.a_xml()
        with open(self.archivo, 'w', encoding='utf-8') as f:
            f.write(xml_str)

    def cargar(self):
        """Carga el nodo desde un archivo XML."""
        with open(self.archivo, 'r', encoding='utf-8') as f:
            xml_str = f.read()
        return Nodo.desde_xml(xml_str)    

class XMLProcessor:
    def __init__(self, xml_file=None):
        """Constructor de la clase XMLProcessor"""
        self.xml_file = xml_file
        self.message_processor = MessageProcessor(xml_file)
        self.sentiment_analyzer = SentimentAnalyzer(positive_words, negative_words)
        self.response_generator = XMLResponseGenerator(self.sentiment_analyzer, self.message_processor.diccionario)

    def cargar_archivo(self, archivo):
        """Carga el archivo XML y lo convierte en un árbol DOM."""
        self.message_processor.cargar_archivo(archivo)

    def leer_mensajes(self):
        """Lee los mensajes de usuarios desde el archivo XML cargado."""
        return self.message_processor.leer_mensajes()

    def generar_respuesta_xml(self, mensajes):
        """Genera un archivo XML con los resultados del análisis."""
        return self.response_generator.generar_respuesta_xml(mensajes)

class SentimentAnalyzer:
    def __init__(self, positive_words, negative_words):
        self.positive_words = positive_words
        self.negative_words = negative_words

    def normalizar_texto(self, texto):
        """Normaliza el texto eliminando tildes y convirtiendo a minúsculas."""
        texto = texto.lower()
        texto = ''.join(
            (c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
        )
        return texto

    def analizar_sentimiento(self, mensaje):
        """Analiza el sentimiento de un mensaje."""
        mensaje = self.normalizar_texto(mensaje)
        positivo = sum(palabra in mensaje for palabra in self.positive_words)
        negativo = sum(palabra in mensaje for palabra in self.negative_words)
        
        if positivo > negativo:
            return "positivo"
        elif negativo > positivo:
            return "negativo"
        else:
            return "neutro"
        

class MessageProcessor:
    def __init__(self, xml_file=None):
        self.xml_file = xml_file
        self.tree = None
        self.diccionario = {
            "empresas": {}
        }
        if xml_file:
            self.cargar_archivo(xml_file)

    def cargar_archivo(self, archivo):
        """Carga el archivo XML y lo convierte en un árbol DOM."""
        try:
            self.tree = ET.parse(archivo)
            print(f"Archivo {archivo} cargado correctamente.")
            self.cargar_empresas()
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            self.tree = None

    def cargar_empresas(self):
        """Lee las empresas y sus servicios desde el XML cargado."""
        if not self.tree:
            raise ValueError("No se ha cargado ningún archivo XML.")
        
        # Leer las empresas y sus servicios
        empresas = {}
        empresas_xml = self.tree.findall('.//empresa')
        for empresa in empresas_xml:
            nombre_empresa = empresa.find('nombre').text
            servicios = empresa.findall('servicio')
            servicios_dict = {}
            for servicio in servicios:
                nombre_servicio = servicio.attrib['nombre']
                aliases = [alias.text for alias in servicio.findall('alias')]
                servicios_dict[nombre_servicio] = aliases
            empresas[nombre_empresa] = servicios_dict

        # Almacenar las empresas en el diccionario
        self.diccionario['empresas'] = empresas

    def leer_mensajes(self):
        """Lee los mensajes de usuarios desde el archivo XML cargado."""
        if not self.tree:
            raise ValueError("No se ha cargado ningún archivo XML.")

        mensajes = []
        mensajes_xml = self.tree.findall('.//mensaje')
        for mensaje in mensajes_xml:
            mensajes.append(mensaje.text)
        return mensajes
    
class XMLResponseGenerator:
    def __init__(self, sentiment_analyzer, diccionario):
        self.sentiment_analyzer = sentiment_analyzer
        self.diccionario = diccionario

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element."""
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="   ")

    def generar_respuesta_xml(self, mensajes):
        """Genera un archivo XML con los resultados del análisis."""
        root = ET.Element("lista_respuestas")
        respuesta = ET.SubElement(root, "respuesta")
        fecha = ET.SubElement(respuesta, "fecha")
        fecha.text = "01/04/2022"  # Ejemplo de fecha, puedes cambiarlo según sea necesario
        
        mensajes_element = ET.SubElement(respuesta, "mensajes")
        total = ET.SubElement(mensajes_element, "total")
        total.text = str(len(mensajes))
        
        positivos = sum(1 for mensaje in mensajes if self.sentiment_analyzer.analizar_sentimiento(mensaje) == "positivo")
        negativos = sum(1 for mensaje in mensajes if self.sentiment_analyzer.analizar_sentimiento(mensaje) == "negativo")
        neutros = len(mensajes) - positivos - negativos
        
        ET.SubElement(mensajes_element, "positivos").text = str(positivos)
        ET.SubElement(mensajes_element, "negativos").text = str(negativos)
        ET.SubElement(mensajes_element, "neutros").text = str(neutros)
        
        analisis = ET.SubElement(respuesta, "analisis")
        for empresa, servicios in self.diccionario['empresas'].items():
            empresa_element = ET.SubElement(analisis, "empresa", nombre=empresa)
            empresa_mensajes = [mensaje for mensaje in mensajes if empresa.lower() in self.sentiment_analyzer.normalizar_texto(mensaje)]
            empresa_total = len(empresa_mensajes)
            empresa_positivos = sum(1 for mensaje in empresa_mensajes if self.sentiment_analyzer.analizar_sentimiento(mensaje) == "positivo")
            empresa_negativos = sum(1 for mensaje in empresa_mensajes if self.sentiment_analyzer.analizar_sentimiento(mensaje) == "negativo")
            empresa_neutros = empresa_total - empresa_positivos - empresa_negativos
            
            empresa_mensajes_element = ET.SubElement(empresa_element, "mensajes")
            ET.SubElement(empresa_mensajes_element, "total").text = str(empresa_total)
            ET.SubElement(empresa_mensajes_element, "positivos").text = str(empresa_positivos)
            ET.SubElement(empresa_mensajes_element, "negativos").text = str(empresa_negativos)
            ET.SubElement(empresa_mensajes_element, "neutros").text = str(empresa_neutros)
            
            servicios_element = ET.SubElement(empresa_element, "servicios")
            for servicio, aliases in servicios.items():
                servicio_element = ET.SubElement(servicios_element, "servicio", nombre=servicio)
                servicio_mensajes = [mensaje for mensaje in empresa_mensajes if any(alias.lower() in self.sentiment_analyzer.normalizar_texto(mensaje) for alias in aliases)]
                servicio_total = len(servicio_mensajes)
                servicio_positivos = sum(1 for mensaje in servicio_mensajes if self.sentiment_analyzer.analizar_sentimiento(mensaje) == "positivo")
                servicio_negativos = sum(1 for mensaje in servicio_mensajes if self.sentiment_analyzer.analizar_sentimiento(mensaje) == "negativo")
                servicio_neutros = servicio_total - servicio_positivos - servicio_negativos
                
                servicio_mensajes_element = ET.SubElement(servicio_element, "mensajes")
                ET.SubElement(servicio_mensajes_element, "total").text = str(servicio_total)
                ET.SubElement(servicio_mensajes_element, "positivos").text = str(servicio_positivos)
                ET.SubElement(servicio_mensajes_element, "negativos").text = str(servicio_negativos)
                ET.SubElement(servicio_mensajes_element, "neutros").text = str(servicio_neutros)
        
        # Prettify the XML output
        pretty_xml = self.prettify(root)
        
        # Save the prettified XML to a file
        with open("data/response.xml", "w", encoding="utf-8") as f:
            f.write(pretty_xml)

        return pretty_xml