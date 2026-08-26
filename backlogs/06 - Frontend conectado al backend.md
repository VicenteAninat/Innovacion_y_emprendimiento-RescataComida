# Tarea-06: Frontend por features e integración con backend real

**Estado:** Hecho

**Director:** Nelson Cereño

**Agente utilizado:** Deepseek V4

### 1. Contexto y Objetivo
El frontend era un único archivo (App.tsx, ~3.800 líneas) con datos de prueba en memoria y sin conexión con el backend. Se pidió separarlo en componentes organizados por features, conectarlo a la API real (FastAPI + Supabase) y limpiar lo que quedó de más (mock de pruebas, componentes sin uso y archivos del template de Figma).

### 2. Prompts
> "Tenemos un frontend que es un solo archivo: sepáralo en componentes y déjalo para que tenga sentido con el backend"

> "Agrega un mock del backend para probar la interfaz sin backend y luego conéctala al backend real de Supabase"

> "Limpia lo que quedó de más: mock, componentes sin uso y archivos del template; deja una forma fácil de levantar el proyecto"

### 3. Criterios de Éxito Verificables
#### Prompt 1:
- El frontend queda organizado en features (auth, consumer, provider, shared) y compila sin errores (`tsc --noEmit` y `vite build`).

#### Prompt 2:
- Login, feed de ofertas, reservas con pago y cancelación, reseñas, favoritos y panel del comerciante funcionan contra datos reales persistidos en Supabase.

#### Prompt 3:
- No quedan referencias al mock ni a los componentes del template; `run_backend.bat` y `Frontend/run_frontend.bat` levantan el proyecto con doble clic.

### 4. Resolución
- **Commit:** https://github.com/VicenteAninat/Innovacion_y_emprendimiento-RescataComida/commit/a94ec5cd9adc9f19d718565f2e768db294885b66
- **Aprendizaje:** Con la publishable key y sin foreign keys declaradas en la BD, los joins anidados de PostgREST fallan (PGRST200) y deben resolverse con consultas manuales. Los datetime deben serializarse a ISO 8601 antes de insertar, y la columna PostGIS devuelve GeoJSON en lugar de texto. El mock (MSW) sirvió para validar la interfaz sin backend y se eliminó al conectar el real.
