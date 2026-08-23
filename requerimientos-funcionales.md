# Requerimientos Funcionales Backend - RescataComida

> Estado: [x] implementado · [~] parcial · [ ] pendiente
> (última actualización: integración frontend con Supabase real)

## 1. Módulo de Autenticación y Perfiles (`/auth`)
* **Registro de Usuario:** Crear el perfil base en la plataforma y asignar el rol correspondiente (`customer`, `worker`, `admin`). [x]
* **Inicio de Sesión:** Autenticar credenciales y devolver el token de sesión (JWT). [x]
* **Ver/Editar Perfil:** Endpoint para que el usuario consumidor pueda visualizar y actualizar sus datos personales. [x]
* **Vincular Trabajador (Admin Local):** Endpoint protegido para asignar un `business_id` específico a un usuario que tiene el rol de `worker`. [x]

## 2. Módulo de Comercios y Geolocalización (`/businesses`)
* **Registrar/Onboarding Local:** Dar de alta un nuevo comercio con su categoría, dirección física y coordenadas exactas (PostGIS). [x]
* **Buscar Locales Cercanos:** Recibir la latitud y longitud actual del cliente y devolver una lista de locales con ofertas activas dentro de un radio específico (ej. 5 km). [~] Endpoint listo; requiere que la función RPC de PostGIS exista en la BD.

## 3. Módulo de Ofertas / Bolsas Sorpresa (`/offers`)
* **Publicar Bolsa:** El admin del local (`worker`) crea una oferta indicando el precio original, el precio rebajado, el stock disponible y la ventana de horario para el retiro. El backend calcula y asocia los kg salvados y el CO2 evitado por unidad. [x]
* **Modificar/Eliminar Bolsa:** Gestión básica (CRUD) de las ofertas publicadas por el local. [x]
* **Listar Ofertas Activas:** El *feed* principal de la app para el consumidor. Filtra automáticamente las bolsas con estado `active` y `quantity_available > 0`. [x]

## 4. Módulo de Reservas y Transacciones (`/reservations`)
* **Crear Reserva:** El cliente selecciona una oferta. El backend valida que exista stock, crea la reserva en estado `pending` y descuenta el inventario (trigger con `FOR UPDATE`). [x]
* **Pagar Reserva:** Procesa el pago (o lo simula en esta etapa) y cambia el estado de la reserva a `paid` (ventana de 15 minutos). [x]
* **Cancelar Reserva:** Permite al cliente arrepentirse antes del pago, o al local cancelar por fuerza mayor. Retorna el stock a la oferta. [x]
* **Confirmar Retiro (Worker):** El admin del local marca la reserva como `collected` cuando el cliente se lleva la comida. **Este es el evento crítico** que alimenta la tabla de histórico de ML y suma a las métricas del local. [~] Funciona vía `PATCH /reservations/update/{id}`; falta un endpoint dedicado.
* **Historial del Cliente:** Endpoint para que el consumidor vea sus pedidos pasados y activos. [x]
* **Gestión de Reseñas:** El cliente puede dejar un rating y comentario sobre una reserva finalizada. El admin del local puede consultar el listado de reseñas recibidas. [x]

## 5. Módulo de Fidelización (`/favorites`)
* **Gestionar Favoritos:** El cliente puede agregar o eliminar un local de su lista de favoritos. [x]
* **Feed de Favoritos:** Endpoint específico que devuelve únicamente las ofertas activas de los locales que el usuario tiene marcados. [~] Endpoint listo; requiere la función RPC en la BD.

## 6. Módulo de Impacto Social y ML (`/analytics`, `/donations`, `/ml`)
* **Panel de Métricas (Dashboard Local):** Devuelve el consolidado de ventas, dinero recuperado, CO2 evitado y kg de comida salvada por el comercio en un periodo de tiempo. [ ] Pendiente (no existe `/analytics`; el front calcula métricas simples client-side).
* **Registro de Donaciones:** El admin del local consulta el listado de Bancos de Alimentos disponibles y registra el envío de excedentes (guardando peso y comprobante). [x] Backend listo (`/donations`, `/foodbanks`); falta UI en el frontend.
* **Pricing Dinámico (ML):** Endpoint interno que el frontend del local consulta antes de publicar una bolsa. Envía variables de contexto (clima, hora, día) y el modelo predictivo devuelve una sugerencia de precio y la estimación de excedentes para hoy. [ ] Pendiente (`MlHistoricalDataService` es un stub).

## 7. Módulo de Administración de Plataforma (`/admin`)
* **Gestión de Bancos de Alimentos:** Alta, baja y modificación del directorio de bancos de alimentos disponibles para donación. [x]
* **Cron Jobs (Procesos en segundo plano):** Tareas automáticas del sistema que se ejecutan cada cierto tiempo para:
    * Pasar las bolsas no vendidas a estado `expired` cuando termina su ventana de retiro. [ ]
    * Cancelar reservas en estado `pending` que superaron el tiempo límite de pago. [~] La función SQL `cancelar_reservas_expiradas()` existe; falta activar `pg_cron` en Supabase.
