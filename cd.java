package com.mycompany.proyecto2;

import java.util.ArrayList;
import java.util.List;

/**
 * Analizador Sintáctico generado según la Gramática Libre de Contexto (GRL):
 *   INICIO     -> MUNDOS
 *   MUNDOS     -> MUNDO MUNDOS'
 *   MUNDOS'    -> "," MUNDO MUNDOS' | ε
 *   MUNDO      -> pr_world cadena "{" LOCACIONES CONEXIONES OBJETOS "}"
 *   LOCACIONES -> LOCACION LOCACIONES'
 *   LOCACIONES'-> LOCACION LOCACIONES' | ε
 *   LOCACION  -> pr_place identificador ":" pr_locacion pr_at "(" numero "," numero ")"
 *   CONEXIONES -> ("connect" identificador "to" identificador "with" cadena)*
 *   OBJETOS    -> ("object" cadena ":" identificador "at" (identificador | "(" numero "," numero ")"))*
 */
public class AnalizadorSitacticox {
    // ------------------- Estructuras internas -------------------
    private List<Token> tokens;           // tokens de entrada (análisis léxico previo)
    private List<Error> errores;          // colección de errores sintácticos
    private StringBuilder descripcionMapa; // salida Graphviz
    private String mundoActual;           // nombre del mundo en procesamiento

    public AnalizadorSitacticox (List<Token> tokens) {
        this.tokens = tokens;
        this.errores = new ArrayList<>();
        this.descripcionMapa = new StringBuilder();
        this.mundoActual = "";
    }

    // Agrega un error asociado a un token (o EOF)
    public void agregarError(Token token, String mensaje) {
        int linea = token != null ? token.getLinea() : 0;
        int columna = token != null ? token.getColumna() : 0;
        String caracter = token != null ? token.getLexema() : "EOF";
        errores.add(new Error(caracter, mensaje, linea, columna, "Sintáctico"));
    }

    public List<Error> getErrores() {
        return errores;
    }

    /**
     * Método principal que corresponde a la regla <INICIO> -> MUNDOS
     */
    public void analizar(String rutaDot, String rutaPng) {
        this.INICIO();                    
        if (!errores.isEmpty()) {
            System.out.println("Errores encontrados durante el análisis sintáctico.");
        } else {
            System.out.println("Análisis sintáctico completado sin errores.");
            try {
                GeneradorMapaa.generarMapaConGraphviz(descripcionMapa.toString(), rutaDot, rutaPng);
            } catch (Exception e) {
                System.err.println("Error al generar el mapa: " + e.getMessage());
            }
        }
    }

    // Obtiene o consume tokens auxiliar
    private Token obtenerTokenActual() { return tokens.isEmpty() ? null : tokens.get(0); }
    private void consumirToken() { if (!tokens.isEmpty()) tokens.remove(0); }

    /**
     * <INICIO> ::= <MUNDOS>
     */
    private void INICIO() {
        System.out.println("INICIO");
        MUNDOS();
    }

    /**
     * <MUNDOS> ::= <MUNDO> <MUNDOS'>
     */
    private void MUNDOS() {
        System.out.println("MUNDOS");
        MUNDO();               // corresponde a producción MUNDO
        MUNDOSP();             // corresponde a MUNDOS'
    }

    /**
     * <MUNDOS'> ::= "," <MUNDO> <MUNDOS'> | ε
     */
    private void MUNDOSP() {
        System.out.println("MUNDOSP");
        Token actual = obtenerTokenActual();
        if (actual != null && actual.getTipo().equals("coma")) { // ","
            consumirToken();
            MUNDO();           // producción recursiva
            MUNDOSP();
        }
        // epsilon: no hay coma, retorna
    }

    /**
     * <MUNDO> ::= pr_world cadena "{" LOCACIONES CONEXIONES OBJETOS "}"
     */
    private void MUNDO() {
        System.out.println("MUNDO");
        Token actual = obtenerTokenActual();
        if (actual != null && actual.getTipo().equals("pr_world")) { // "world"
            consumirToken();
            actual = obtenerTokenActual();
            if (actual != null && actual.getTipo().equals("cadena")) { // nombre de mundo
                mundoActual = actual.getLexema();
                descripcionMapa.append("// Mundo: ").append(mundoActual).append("\n");
                consumirToken();
                actual = obtenerTokenActual();
                if (actual != null && actual.getTipo().equals("llave_abre")) { // "{"
                    consumirToken();
                    LOCACIONES();   // producción LOCACIONES
                    CONEXIONES();   // producción CONEXIONES
                    OBJETOS();      // producción OBJETOS
                    actual = obtenerTokenActual();
                    if (actual != null && actual.getTipo().equals("llave_cierra")) { // "}"
                        consumirToken();
                        return;
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

    /**
     * <LOCACIONES> ::= <LOCACION> <LOCACIONES'>
     */
    private void LOCACIONES() {
        System.out.println("LOCACIONES");
        LOCACION();            // al menos una locación
        LOCACIONESP();         // cero o más locaciones adicionales
    }

    /**
     * <LOCACIONES'> ::= <LOCACION> <LOCACIONES'> | ε
     */
    private void LOCACIONESP() {
        System.out.println("LOCACIONESP");
        Token actual = obtenerTokenActual();
        if (actual != null && actual.getTipo().equals("pr_place")) {
            LOCACION();
            LOCACIONESP();
        }
    }

    /**
     * <LOCACION> ::= pr_place identificador ":" pr_locacion pr_at "(" numero "," numero ")"
     */
    private void LOCACION() {
        System.out.println("LOCACION");
        Token actual = obtenerTokenActual();
        if (actual != null && actual.getTipo().equals("pr_place")) { // "place"
            consumirToken();
            actual = obtenerTokenActual();
            if (actual != null && actual.getTipo().equals("identificador")) {
                String identificador = actual.getLexema();
                consumirToken();
                actual = obtenerTokenActual();
                if (actual != null && actual.getTipo().equals("dos_puntos")) { // ":"
                    consumirToken();
                    actual = obtenerTokenActual();
                    if (actual != null && actual.getTipo().equals("pr_locacion")) { // tipo de locación
                        consumirToken();
                        actual = obtenerTokenActual();
                        if (actual != null && actual.getTipo().equals("pr_at")) { // "at"
                            consumirToken();
                            actual = obtenerTokenActual();
                            if (actual != null && actual.getTipo().equals("parentesis_abre")) { // "("
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

    /**
     * <CONEXIONES> ::= (<CONEXION>)*
     * <CONEXION>  ::= connect identificador to identificador with cadena
     */
    private void CONEXIONES() {
        System.out.println("CONEXIONES");
        Token actual = obtenerTokenActual();
        while (actual != null && actual.getTipo().equals("connect")) {
            CONEXION();
            actual = obtenerTokenActual();
        }
    }

    private void CONEXION() {
        System.out.println("CONEXION");
        Token actual = obtenerTokenActual();
        // ... implementación análoga, mapeo directo a la producción CONEXION
    }

    /**
     * <OBJETOS> ::= (<OBJETO>)*
     * <OBJETO>  ::= object cadena ":" identificador "at" (identificador | "(" numero "," numero ")")
     */
    private void OBJETOS() {
        System.out.println("OBJETOS");
        Token actual = obtenerTokenActual();
        while (actual != null && actual.getTipo().equals("object")) {
            OBJETO();
            actual = obtenerTokenActual();
        }
    }

    private void OBJETO() {
        System.out.println("OBJETO");
        // ... implementación análoga, mapeo directo a la producción OBJETO
    }
}
