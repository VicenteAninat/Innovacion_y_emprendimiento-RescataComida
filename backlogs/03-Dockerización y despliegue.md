# Tarea-03: Dockerización y despliegue

**Estado:** 

**Director:** Ignacio D'Agostino

**Agente utilizado:** Antigravity

### 1. Contexto y Objetivo
Se pide al agente el qué se debe hacer para dockerizar el proyecto, luego se pregunta cómo disponibilizarlo y por último se le pide aplicar los cambios necesarios para que se pueda desplegar el proyecto.

### 2. Prompts
> "Qué comando(s) debo ejecutar para buildear y ejecutar las imagenes docker"

> "¿Si quiero disponibilizar el proyecto usando un tunel como Cloudflared, ¿Sólo debo abrir una URL al frontend del proyecto?"

> "Haz los cambios necesarios para que el proyecto funcione en despliegue, considerando que las urls serán (URLs del proyecto)"

### 3. Criterios de Éxito Verificables
#### Prompt 1:
- Una respuesta que contenga las definiciones de los Dockerfiles correspondientes, archivo docker-compose y comando para construir y levantar los contenedores (docker compose up -d --build).  

#### Prompt 2:
- Una respuesta que contenga la respuesta a la pregunta hecha y guíe con las URLs de despliegue tanto del Backend como el Frontend. 

#### Prompt 3:
- Modificación de configuraciones, tanto en el backend como en el frontend, para acomodar la disponibilización del proyecto mediante las URLs indicadas 

### 4. Resolución
- **Commit:** [(enlace)](https://github.com/VicenteAninat/Innovacion_y_emprendimiento-Backend/commit/c51a91e3fee4272ff938386c4bd0e43bb614f28e)

- **Aprendizaje:**
Se aprendió el flujo para definir y construir imágenes de docker de los componentes del proyecto, de tal manera que estos contenedores puedan ser levantados directamente mediante el uso del repositorio, sin pasar por servicios externos como Dockerhub.
