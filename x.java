package com.mycompany.proyecto2;

import java.util.ArrayList;              // Importa ArrayList para almacenar listas dinámicas
import java.util.List;                   // Importa la interfaz List para tipar colecciones

public class AnalizadorSintacticos {
    private List<Token> tokens;           // Lista de tokens resultante del análisis léxico
    private List<Error> errores;          // Lista donde guardamos los errores sintácticos
    private StringBuilder descripcionMapa; // Acumula el texto que luego se convertirá en un gráfico
    private String mundoActual;           // Guarda el nombre del mundo que estamos procesando

    // Constructor: recibe la lista de tokens y prepara las estructuras internas
    public AnalizadorSintacticos(List<Token> tokens) {
        this.tokens = tokens;             // Asigna la lista de tokens recibida
        this.errores = new ArrayList<>(); // Inicializa la lista de errores vacía
        this.descripcionMapa = new StringBuilder(); // StringBuilder vacío para la descripción
        this.mundoActual = "";          // Nombre de mundo vacío inicialmente
    }

    // Método auxiliar para registrar un error sintáctico
    public void agregarError(Token token, String mensaje) {
        int linea = token != null ? token.getLinea() : 0;    // Línea donde ocurrió (o 0)
        int columna = token != null ? token.getColumna() : 0; // Columna donde ocurrió (o 0)
        String caracter = token != null ? token.getLexema() : "EOF"; // Lexema o EOF
        errores.add(new Error(caracter, mensaje, linea, columna, "Sintáctico")); // Añade el Error
    }

    // Devuelve la lista de errores encontrados
    public List<Error> getErrores() {
        return errores;
    }

    // Método principal: arranca el análisis sintáctico y genera el mapa si no hay errores
    public void analizar(String rutaDot, String rutaPng) {
        this.INICIO();                    // Inicia la llamada a la primera regla
        if (!errores.isEmpty()) {         // Si hubo errores
            System.out.println("Errores encontrados durante el análisis sintáctico.");
        } else {
            System.out.println("Análisis sintáctico completado sin errores.");
            try {
                // Genera el archivo DOT y el PNG a partir de la descripción
                GeneradorMapaa.generarMapaConGraphviz(descripcionMapa.toString(), rutaDot, rutaPng);
            } catch (Exception e) {
                System.err.println("Error al generar el mapa: " + e.getMessage());
            }
        }
    }

    // Retorna el token actual (primero de la lista) o null si no quedan
    private Token obtenerTokenActual() {
        return tokens.isEmpty() ? null : tokens.get(0);
    }

    // Consume el token actual eliminándolo de la lista
    private void consumirToken() {
        if (!tokens.isEmpty()) {
            tokens.remove(0);
        }
    }

    // Regla inicial de la gramática
    private void INICIO() {
        System.out.println("INICIO");  // Log para depuración
        MUNDOS();                        // Llama a la regla MUNDOS
    }

    // Regla: uno o más mundos separados por comas
    private void MUNDOS() {
        System.out.println("MUNDOS");
        MUNDO();                         // Procesa un mundo
        MUNDOSP();                       // Y luego las repeticiones
    }

    // Parte repetitiva de MUNDOS: si hay coma, consume y procesa otro mundo
    private void MUNDOSP() {
        System.out.println("MUNDOSP");
        Token actual = obtenerTokenActual();
        if (actual != null && actual.getTipo().equals("coma")) {
            consumirToken();            // Consume la coma
            MUNDO();                    // Otro mundo
            MUNDOSP();                  // Posibles más repeticiones
        }
    }

    // Regla para un único mundo
    private void MUNDO() {
        System.out.println("MUNDO");
        Token actual = obtenerTokenActual();
        if (actual != null && actual.getTipo().equals("pr_world")) { // "world"
            consumirToken();            // Consume "world"
            actual = obtenerTokenActual();
            if (actual != null && actual.getTipo().equals("cadena")) { // Nombre entre comillas
                mundoActual = actual.getLexema(); // Guarda el nombre del mundo
                descripcionMapa.append("// Mundo: ").append(mundoActual).append("\n");
                consumirToken();        // Consume el nombre
                actual = obtenerTokenActual();
                if (actual != null && actual.getTipo().equals("llave_abre")) { // "{"
                    consumirToken();    // Consume "{"
                    LOCACIONES();       // Procesa locaciones
                    CONEXIONES();       // Procesa conexiones
                    OBJETOS();          // Procesa objetos
                    actual = obtenerTokenActual();
                    if (actual != null && actual.getTipo().equals("llave_cierra")) { // "}"
                        consumirToken(); // Consume "}"
                        return;         // Mundo completo
                    } else {
                        agregarError(actual, "Se esperaba '}' al final del mundo.");
                    }
                } else {
                    agregarError(actual, "Se esperaba '{' después del nombre del mundo.");
                }
            } else {
                agregarError(actual, "Se esperaba un nombre de mundo entre comillas.");
            }
        } else {
            agregarError(actual, "Se esperaba la palabra reservada 'world'.");
        }
    }

    // Regla: una o más locaciones
    private void LOCACIONES() {
        System.out.println("LOCACIONES");
        LOCACION();                      // Al menos una locación
        LOCACIONESP();                   // Cero o más adicionales
    }

    // Parte repetitiva de LOCACIONES: mientras aparezca "place", procesa más locaciones
    private void LOCACIONESP() {
        System.out.println("LOCACIONESP");
        Token actual = obtenerTokenActual();
        if (actual != null && actual.getTipo().equals("pr_place")) {
            LOCACION();                  // Nueva locación
            LOCACIONESP();               // Recurre para más
        }
    }

    // Regla para una locación individual
    private void LOCACION() {
        System.out.println("LOCACION");
        Token actual = obtenerTokenActual();
        if (actual != null && actual.getTipo().equals("pr_place")) { // "place"
            consumirToken();            // Consume "place"
            actual = obtenerTokenActual();
            if (actual != null && actual.getTipo().equals("identificador")) {
                String identificador = actual.getLexema(); // Nombre de la locación
                consumirToken();        // Consume identificador
                actual = obtenerTokenActual();
                if (actual != null && actual.getTipo().equals("dos_puntos")) { // ":"
                    consumirToken();    // Consume ":"
                    actual = obtenerTokenActual();
                    if (actual != null && actual.getTipo().equals("pr_locacion")) { // Tipo (forest, etc.)
                        String tipo = actual.getLexema();
                        consumirToken();
                        actual = obtenerTokenActual();
                        if (actual != null && actual.getTipo().equals("pr_at")) { // "at"
                            consumirToken();
                            actual = obtenerTokenActual();
                            if (actual != null && actual.getTipo().equals("parentesis_abre")) { // "("
                                consumirToken();
                                actual = obtenerTokenActual();
                                if (actual != null && actual.getTipo().equals("numero")) {
                                    String x = actual.getLexema(); // Coordenada X
                                    consumirToken();
                                    actual = obtenerTokenActual();
                                    if (actual != null && actual.getTipo().equals("coma")) { // ","
                                        consumirToken();
                                        actual = obtenerTokenActual();
                                        if (actual != null && actual.getTipo().equals("numero")) {
                                            String y = actual.getLexema(); // Coordenada Y
                                            consumirToken();
                                            actual = obtenerTokenActual();
                                            if (actual != null && actual.getTipo().equals("parentesis_cierra")) { // ")"
                                                consumirToken();
                                                // Añade la línea al mapa
                                                descripcionMapa.append(
                                                  String.format("place %s : %s at (%s,%s)\n",
                                                    identificador, tipo, x, y));
                                                return;
                                            } else {
                                                agregarError(actual, "Se esperaba ')' para cerrar las coordenadas.");
                                            }
                                        } else {
                                            agregarError(actual, "Se esperaba un número para la coordenada Y.");
                                        }
                                    } else {
                                        agregarError(actual, "Se esperaba ',' entre las coordenadas.");
                                    }
                                } else {
                                    agregarError(actual, "Se esperaba un número para la coordenada X.");
                                }
                            } else {
                                agregarError(actual, "Se esperaba '(' para las coordenadas.");
                            }
                        } else {
                            agregarError(actual, "Se esperaba 'at' para especificar la posición.");
                        }
                    } else {
                        agregarError(actual, "Se esperaba un tipo de locación.");
                    }
                } else {
                    agregarError(actual, "Se esperaba ':' después del identificador de la locación.");
                }
            } else {
                agregarError(actual, "Se esperaba un identificador para la locación.");
            }
        } else {
            agregarError(actual, "Se esperaba la palabra reservada 'place'.");
        }
    }

    // Regla: cero o más conexiones
    private void CONEXIONES() {
        System.out.println("CONEXIONES");
        Token actual = obtenerTokenActual();
        while (actual != null && actual.getTipo().equals("connect")) {
            CONEXION();                  // Procesa cada conexión
            actual = obtenerTokenActual();
        }
    }

    // Regla para una conexión individual
    private void CONEXION() {
        System.out.println("CONEXION");
        Token actual = obtenerTokenActual();
        if (actual != null && actual.getTipo().equals("connect")) { // "connect"
            consumirToken();            // Consume "connect"
            actual = obtenerTokenActual();
            if (actual != null && actual.getTipo().equals("identificador")) {
                String origen = actual.getLexema(); // Lugar de origen
                consumirToken();
                actual = obtenerTokenActual();
                if (actual != null && actual.getTipo().equals("to")) { // "to"
                    consumirToken();
                    actual = obtenerTokenActual();
                    if (actual != null && actual.getTipo().equals("identificador")) {
                        String destino = actual.getLexema(); // Lugar destino
                        consumirToken();
                        actual = obtenerTokenActual();
                        if (actual != null && actual.getTipo().equals("with")) { // "with"
                            consumirToken();
                            actual = obtenerTokenActual();
                            if (actual != null && actual.getTipo().equals("cadena")) {
                                String descripcion = actual.getLexema(); // Descripción
                                consumirToken();
                                // Añade la conexión al mapa
                                descripcionMapa.append(
                                  String.format("connect %s to %s with \"%s\"\n",
                                    origen, destino, descripcion));
                                return;
                            } else {
                                agregarError(actual, "Se esperaba una descripción de conexión entre comillas.");
                            }
                        } else {
                            agregarError(actual, "Se esperaba 'with' en la conexión.");
                        }
                    } else {
                        agregarError(actual, "Se esperaba un identificador de lugar destino.");
                    }
                } else {
                    agregarError(actual, "Se esperaba 'to' en la conexión.");
                }
            } else {
                agregarError(actual, "Se esperaba un identificador de lugar origen.");
            }
        } else {
            agregarError(actual, "Se esperaba 'connect' para iniciar una conexión.");
        }
    }

    // Regla: cero o más objetos
    private void OBJETOS() {
        System.out.println("OBJETOS");
        Token actual = obtenerTokenActual();
        while (actual != null && actual.getTipo().equals("object")) {
            OBJETO();                    // Procesa cada objeto
            actual = obtenerTokenActual();
        }
    }

    // Regla para un objeto individual
    private void OBJETO() {
        System.out.println("OBJETO");
        Token actual = obtenerTokenActual();
        if (actual != null && actual.getTipo().equals("object")) { // "object"
            consumirToken();            // Consume "object"
            actual = obtenerTokenActual();
            if (actual != null && actual.getTipo().equals("cadena")) {
                String nombre = actual.getLexema(); // Nombre del objeto
                consumirToken();
                actual = obtenerTokenActual();
                if (actual != null && actual.getTipo().equals(":")) { // ":"
                    consumirToken();        // Consume ":"
                    actual = obtenerTokenActual();
                    if (actual != null && actual.getTipo().equals("identificador")) {
                        String tipo = actual.getLexema(); // Tipo de objeto
                        consumirToken();
                        actual = obtenerTokenActual();
                        if (actual != null && actual.getTipo().equals("at")) { // "at"
                            consumirToken();    
                            actual = obtenerTokenActual();
                            if (actual != null && actual.getTipo().equals("identificador")) {
                                String ubicacion = actual.getLexema(); // Ubicación
                                consumirToken();
                                // Añade objeto sin coordenadas
                                descripcionMapa.append(
                                  String.format("object \"%s\" : %s at %s\n",
                                    nombre, tipo, ubicacion));
                                return;
                            } else if (actual != null && actual.getTipo().equals("parentesis_abre")) {
                                // Variante con coordenadas
                                consumirToken();
                                actual = obtenerTokenActual();
                                if (actual != null && actual.getTipo().equals("numero")) {
                                    String x = actual.getLexema();
                                    consumirToken();
                                    actual = obtenerTokenActual();
                                    if (actual != null && actual.getTipo().equals("coma")) {
                                        consumirToken();
                                        actual = obtenerTokenActual();
                                        if (actual != null && actual.getTipo().equals("numero")) {
                                            String y = actual.getLexema();
                                            consumirToken();
                                            actual = obtenerTokenActual();
                                            if (actual != null && actual.getTipo().equals("parentesis_cierra")) {
                                                consumirToken();
                                                // Añade objeto con coordenadas
                                                descripcionMapa.append(
                                                  String.format("object \"%s\" : %s at (%s,%s)\n",
                                                    nombre, tipo, x, y));
                                                return;
                                            } else {
                                                agregarError(actual, "Se esperaba ')' para cerrar las coordenadas.");
                                            }
                                        } else {
                                            agregarError(actual, "Se esperaba un número para la coordenada Y.");
                                        }
                                    } else {
                                        agregarError(actual, "Se esperaba ',' entre las coordenadas.");
                                    }
                                } else {
                                    agregarError(actual, "Se esperaba un número para la coordenada X.");
                                }
                            } else {
                                agregarError(actual, "Se esperaba una ubicación o coordenadas para el objeto.");
                            }
                        } else {
                            agregarError(actual, "Se esperaba 'at' para especificar la ubicación del objeto.");
                        }
                    } else {
                        agregarError(actual, "Se esperaba un tipo de objeto.");
                    }
                } else {
                    agregarError(actual, "Se esperaba ':' después del nombre del objeto.");
                }
            } else {
                agregarError(actual, "Se esperaba un nombre de objeto entre comillas.");
            }
        } else {
            agregarError(actual, "Se esperaba 'object' para iniciar un objeto.");
        }
    }
}
