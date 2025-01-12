# Minecraft Agent Framework

Este proyecto implementa un marco de trabajo en Python que permite el desarrollo y ejecución de agentes 
programados para interactuar con un servidor compartido de Minecraft. 
Los agentes pueden moverse, interactuar con el entorno, construir y destruir bloques, y enviar o recibir 
mensajes del chat.

## Objetivo del Proyecto
El objetivo principal es proporcionar un framework extensible para crear agentes personalizados en Minecraft
que demuestren los conceptos de:
- **Programación funcional.**
- **Programación reflexiva.**

# Características Principales

- **Interacción con Minecraft:** Los agentes pueden comunicarse 
con el entorno y los jugadores a través de la API de Minecraft Pi Edition (`mcpi`).
- **Agentes personalizables:** Incluye ejemplos de agentes con diferentes funcionalidades, 
como `InsultBot`, `TNTBot`, `OracleBot` y `ChatBot`.
- **Extensibilidad:** El framework está diseñado para facilitar la creación de nuevos agentes 
mediante la clase base `Agent`.
- **Pruebas unitarias:** El proyecto incluye pruebas para asegurar la funcionalidad de cada agente.
- **Cobertura del código:** Integra un badge de GitHub Actions para verificar la cobertura de las pruebas.

## Agentes Disponibles

### 1. `Agent`
Clase base que define las funcionalidades comunes de los agentes:
- **Métodos dinámicos:** Listar y ejecutar métodos disponibles del agente.
- **Gestión de atributos:** Obtener y configurar atributos dinámicamente.
- **Control del ciclo de vida:** Iniciar y detener la ejecución del agente en hilos separados.

### 2. `ChatBot`
Responde preguntas en el chat utilizando la API de OpenAI.
- **Función principal:** Procesa entradas con el prefijo `chatbot:` y responde utilizando un modelo de lenguaje.

### 3. `InsultBot`
Envía insultos aleatorios al chat a intervalos regulares.
- **Configuración:** Permite ajustar el intervalo de tiempo entre insultos.

### 4. `OracleBot`
Responde preguntas en el chat con respuestas predefinidas o aleatorias.
- **Función principal:** Responde a mensajes con el prefijo `oracle:` usando programación funcional para procesar eventos.

### 5. `TNTBot`
Genera bloques de TNT cerca del jugador y los activa.
- **Función principal:** Coloca TNT en posiciones generadas dinámicamente cerca del jugador.


## Pruebas

Las pruebas unitarias están incluidas en el directorio `tests/` 
y cubren las funcionalidades principales de los agentes.