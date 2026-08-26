# Tarea-02: Errores pago y horarios

**Estado:** Hecho

**Director:** Ignacio D'Agostino

**Agente utilizado:** Antigravity

### 1. Contexto y Objetivo
Primero se pide al agente que modifique el código del frontend para bloquear el flujo de pago en caso de utilizar un formato de pago inválido, luego se pidió a buscar un error que causana que se aceptara la venta de una bolsa fuera del rango de tiempo y luego modificar el backedn y frontend para que sea pertinente.

### 2. Prompt
> "En el Frontend, en la pantalla de pago de un cliente, quiero que no se pueda continuar si la Información de método de pago está sin modificar o con formato inválido"

> "- Si un cliente ingresa Información de pago incorrecta (Fecha de vencimiento ya vencida), rechazar la realización de la venta. La aplicación aprobó la venta de un bolsa disponible entre las 17:43 a 02:43 (Actualmente son las 15:42). Encuentra el error y arreglalo. Haz modificaciones en backend y frontend como sea pertinente"

### 3. Criterios de Éxito Verificables
#### Prompt 1:
- En la interfaz de pago de una bolsa, efectivamente ocurre que no se puede continuar con el proceso cuándo la información del método de pago está sin rellenar o tiene un formato inválido.

#### Prompt 2:
- El sistema rechaza correctamente un intento de pagar una bolsa con un método de pago vencido. El sistema rechaza correctamente un intento de comprar una bolsa fuera de un horario que se extiende a la madrugada. 

### 4. Resolución
- **Commit:** [(insertar enlace)](https://github.com/VicenteAninat/Innovacion_y_emprendimiento-RescataComida/commit/ed59ddf8e4b2d179d294bd3cf8b6d6143a66f027)

- **Aprendizaje:**
Métodos para evitar el ingreso de datos erroneos por parte de los usuarios.
