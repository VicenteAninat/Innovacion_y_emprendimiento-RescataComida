# Documentación Completa y Resumen de Desarrollo Backend - Octafood

Este documento sirve como referencia oficial y guía de desarrollo para la API del backend de **Octafood**, desarrollada con FastAPI, Pydantic y Supabase (PostgreSQL + PostGIS).

---

## 🔑 Autenticación y Autorización Global
La mayoría de los endpoints del sistema requieren que el cliente envíe una cabecera de autorización HTTP con un token JWT de Supabase Auth:
```http
Authorization: Bearer <JWT_TOKEN>
```
Se dispone de los siguientes roles de usuario:
* `customer`: Consumidor final de bolsas sorpresa.
* `worker`: Trabajador/administrador de un local comercial específico (`business_id`).
* `admin`: Administrador global del sistema.

---

## 📡 Referencia Completa de Endpoints

### 1. Módulo de Autenticación (`/auth`)
Permite el registro, inicio de sesión y gestión básica del perfil del usuario.
* **Controlador:** `app/controller/AuthController.py` | **Servicio:** `app/service/UserService.py`

| Método | Endpoint | Cabecera Auth | Descripción |
| :--- | :--- | :---: | :--- |
| `POST` | `/auth/register` | No | Registra un usuario en Supabase Auth y crea su perfil local en la tabla `users`. Admite un `business_id` opcional. |
| `POST` | `/auth/login` | No | Autentica con `email` y `password`, retornando los tokens de sesión (`access_token`, `refresh_token`) y el objeto perfil del usuario. |
| `GET` | `/auth/profile` | Sí | Recupera el perfil del usuario autenticado actual (`UserEntity`). |
| `PATCH` | `/auth/profile` | Sí | Permite la actualización parcial del perfil (campos: `name`, `phone`). |
| `GET` | `/auth/reservations` | Sí | Retorna de forma directa el historial de reservas de la sesión activa. |

* **Modelos de Entrada (Pydantic):**
  * `RegisterRequest`: `email: str`, `password: str`, `name: str?`, `phone: str?`, `role: str? = 'customer'`, `business_id: int?`
  * `LoginRequest`: `email: str`, `password: str`
  * `UpdateProfileRequest`: `name: str?`, `phone: str?`

---

### 2. Módulo de Locales y Geolocalización (`/businesses`)
Administración de comercios y consultas de mapas con filtros geoespaciales.
* **Controlador:** `app/controller/BusinessesController.py` | **Servicio:** `app/service/BusinessesService.py`

| Método | Endpoint | Cabecera Auth | Descripción |
| :--- | :--- | :---: | :--- |
| `POST` | `/businesses/create` | Sí | Da de alta un nuevo comercio en la base de datos (nombre, rut, categoría, dirección, ubicación PostGIS). |
| `GET` | `/businesses/get_all` | Sí | Retorna un listado de todos los comercios del sistema. |
| `GET` | `/businesses/get/{business_id}` | Sí | Obtiene los detalles de un comercio específico según su ID. |
| `PATCH` | `/businesses/update` | Sí | Modifica un comercio. Recibe `business_id` como parámetro de consulta (query) y los campos a editar en el body. |
| `POST` | `/businesses/delete/{business_id}` | Sí | Elimina físicamente un comercio de la base de datos. |
| `GET` | `/businesses/nearby-with-offers` | Sí | Retorna comercios cercanos con ofertas activas. Parámetros de consulta (query): `lat: float`, `lng: float`, `radius_km: float? = 5.0`. |
| `GET` | `/businesses/favorite-nearby` | Sí | Retorna comercios **favoritos** del usuario que posean ofertas activas dentro del radio especificado. Parámetros de consulta (query): `lat`, `lng`, `radius_km`. |

* **Modelos de Entrada (Pydantic):**
  * `registerBusiness`: `rut: str`, `name: str?`, `category: str?`, `address: str?`, `location: str?` (cadena de coordenadas, ej: `POINT(lng lat)`).

---

### 3. Módulo de Ofertas / Bolsas Sorpresa (`/offers`)
Publicación y consulta de bolsas sorpresa disponibles.
* **Controlador:** `app/controller/OffersController.py` | **Servicio:** `app/service/OffersService.py`

| Método | Endpoint | Cabecera Auth | Permisos requeridos | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `POST` | `/offers/create` | Sí | `worker` / `admin` | Crea una nueva bolsa sorpresa. El backend calcula y asocia de forma automática los `kg_saved_per_unit` y `co2_avoided_per_unit` si no se especifican. Los `worker` solo pueden crear ofertas para su propio negocio. |
| `GET` | `/offers/get_all` | Sí | Cualquiera | Lista todas las ofertas de la base de datos. |
| `GET` | `/offers/get/{offer_id}` | Sí | Cualquiera | Obtiene el detalle de una oferta por su ID. |
| `PATCH` | `/offers/update/{offer_id}` | Sí | `worker` / `admin` | Actualiza parcialmente una oferta. Si se modifica el precio original, recalcula los valores de Kg y CO2. Los `worker` están validados para modificar únicamente ofertas de su propio negocio. |
| `DELETE` | `/offers/delete/{offer_id}` | Sí | `worker` / `admin` | Elimina una oferta de forma física. Validado por negocio del `worker`. |
| `GET` | `/offers/business/{business_id}` | Sí | Cualquiera | Recupera todas las ofertas registradas bajo el comercio especificado (incluyendo inactivas). |
| `GET` | `/offers/favorite-nearby` | Sí | Cualquiera | Devuelve las ofertas activas disponibles en los locales marcados como favoritos dentro del radio. Parámetros: `lat`, `lng`, `radius_km`. |
| `GET` | `/offers/active/{business_id}` | Sí | Cualquiera | Retorna únicamente ofertas con `status = 'active'` and `quantity_available > 0` de un negocio específico (usado al hacer click en el local). |

* **Modelos de Entrada (Pydantic):**
  * `CreateOfferRequest`: `business_id: int`, `title: str`, `description: str?`, `original_price: float`, `discounted_price: float`, `quantity_available: int? = 1`, `pickup_start_time: datetime`, `pickup_end_time: datetime`, `status: str? = 'active'`, `kg_saved_per_unit: float?`, `co2_avoided_per_unit: float?`
  * `UpdateOfferRequest`: Todos los campos anteriores opcionales (excluyendo `business_id`).

---

### 4. Módulo de Favoritos (`/favorites`)
Sistema para guardar locales de interés por parte del consumidor.
* **Controlador:** `app/controller/UserFavoritesController.py` | **Servicio:** `app/service/UserFavoritesService.py`

| Método | Endpoint | Cabecera Auth | Descripción |
| :--- | :--- | :---: | :--- |
| `POST` | `/favorites/add/{business_id}` | Sí | Registra la relación favorito entre el usuario autenticado y el comercio. |
| `DELETE` | `/favorites/remove/{business_id}`| Sí | Elimina la relación favorito. |
| `GET` | `/favorites/check/{business_id}` | Sí | Retorna `True` si el comercio ya está marcado como favorito por el usuario, `False` de lo contrario. |
| `GET` | `/favorites/my-favorites` | Sí | Devuelve el listado de comercios (`List[BusinessesEntity]`) marcados como favoritos por el usuario actual. |

---

### 5. Módulo de Reservas y Transacciones (`/reservations`)
Permite reservar y gestionar las bolsas sorpresa por parte de los usuarios.
* **Controlador:** `app/controller/ReservationsController.py` | **Servicio:** `app/service/ReservationsService.py`

| Método | Endpoint | Cabecera Auth | Descripción |
| :--- | :--- | :---: | :--- |
| `POST` | `/reservations/create` | Sí | Registra una reserva en estado `pending`. El trigger nativo en Supabase valida que la oferta esté activa, bloquea las filas (`FOR UPDATE`) y reduce el stock de la oferta de manera transaccional. |
| `GET` | `/reservations/my-reservations` | Sí | Obtiene las reservas del usuario autenticado (incluye los datos anidados de la oferta). |
| `GET` | `/reservations/get_all` | Sí | *Ruta Administrativa:* Lista todas las reservas del sistema. |
| `GET` | `/reservations/get/{id_val}` | Sí | *Ruta Administrativa:* Consulta el detalle de una reserva por su ID. |
| `PATCH` | `/reservations/update/{id_val}`| Sí | *Ruta Administrativa:* Actualización parcial de una reserva. |
| `POST` | `/reservations/delete/{id_val}`| Sí | *Ruta Administrativa:* Elimina una reserva. |

* **Modelos de Entrada (Pydantic):**
  * `ReservationCreateRequest`: `offer_id: int`, `quantity: int = 1`, `payment_method: str?`, `transaction_fee: float?`
  * `ReservationUpdateRequest`: `quantity: int?`, `status: str?` (`pending`, `paid`, `cancelled`, `collected`), `payment_method: str?`, `transaction_fee: float?`

---

### 6. Módulo de Calificaciones y Reseñas (`/reviews`)
Integridad de feedback para calificar el servicio de los locales posterior al retiro.
* **Controlador:** `app/controller/ReviewsController.py` | **Servicio:** `app/service/ReviewsService.py`

| Método | Endpoint | Cabecera Auth | Descripción |
| :--- | :--- | :---: | :--- |
| `POST` | `/reviews/create` | Sí | Crea una valoración (1 a 5 estrellas) vinculada a una reserva. Valida que el estado de la reserva sea `completed` (o `collected`) y pertenezca al usuario. Asocia automáticamente el `business_id` de la oferta. |
| `PATCH` | `/reviews/update/{review_id}` | Sí | Permite al usuario editar su comentario y calificación. |
| `DELETE` | `/reviews/delete/{review_id}` | Sí | Elimina la reseña, verificando previamente que sea propiedad del usuario que la solicita. |
| `GET` | `/reviews/business/{business_id}` | Sí | Obtiene de forma pública el listado de reseñas asociadas a un local comercial con comentarios y ratings. |

* **Modelos de Entrada (Pydantic):**
  * `ReviewCreateRequest`: `reservation_id: int`, `rating: int` (1 a 5), `comment: str?`
  * `ReviewUpdateRequest`: `rating: int?` (1 a 5), `comment: str?`

---

### 7. Módulo de Soporte Administrativo: Bancos de Alimentos (`/foodbanks`)
Directorio de organizaciones sociales para coordinar la entrega de comida no vendida.
* **Controlador:** `app/controller/FoodBanksController.py` | **Servicio:** `app/service/FoodBanksService.py`

| Método | Endpoint | Cabecera Auth | Descripción |
| :--- | :--- | :---: | :--- |
| `POST` | `/foodbanks/create` | Sí | Registra una organización benéfica (RUT, nombre, correo de contacto, teléfono, dirección). |
| `GET` | `/foodbanks/get_all` | Sí | Obtiene el directorio de todos los bancos de alimentos. |
| `GET` | `/foodbanks/get/{id_val}` | Sí | Detalle de un banco de alimentos. |
| `PATCH` | `/foodbanks/update/{id_val}` | Sí | Actualización parcial de los datos de contacto o dirección. |
| `POST` | `/foodbanks/delete/{id_val}` | Sí | Elimina un banco de alimentos. |

* **Modelos de Entrada (Pydantic):**
  * `FoodBankCreateRequest`: `rut: str`, `name: str?`, `contact_email: str?`, `contact_phone: str?`, `address: str?`
  * `FoodBankUpdateRequest`: Todos los campos anteriores opcionales.

---

### 8. Módulo de Soporte Administrativo: Donaciones (`/donations`)
Registro logístico de comida donada a los bancos de alimentos.
* **Controlador:** `app/controller/DonationsController.py` | **Servicio:** `app/service/DonationsService.py`

| Método | Endpoint | Cabecera Auth | Descripción |
| :--- | :--- | :---: | :--- |
| `POST` | `/donations/create` | Sí | Registra una donación indicando peso en kg, descripción y URL del certificado tributario. |
| `GET` | `/donations/get_all` | Sí | Historial de todas las donaciones hechas en el sistema. |
| `GET` | `/donations/get/{id_val}` | Sí | Detalle de una donación específica. |
| `GET` | `/donations/business/{business_id}`| Sí | Historial de donaciones hechas por un comercio en específico. |
| `PATCH` | `/donations/update/{id_val}` | Sí | Edición de la descripción o carga del comprobante de donación. |
| `POST` | `/donations/delete/{id_val}` | Sí | Elimina un registro de donación. |

* **Modelos de Entrada (Pydantic):**
  * `DonationCreateRequest`: `business_id: int`, `food_bank_id: int`, `description: str?`, `weight_kg: float?`, `tax_deductible_receipt_url: str?`
  * `DonationUpdateRequest`: Todos los campos anteriores opcionales.

---

## 🛠️ Estado del Proyecto y Gaps Críticos

### ❌ Requerimientos Pendientes de Implementación
1. **Pagar Reserva:** Lógica dedicada para pasar el estado a `paid` tras la pasarela/simulación.
2. **Cancelar Reserva:** Flujo específico que incrementa de nuevo el stock (`quantity_available`) de la oferta cancelada.
3. **Confirmar Retiro (Worker):** Endpoint para que el local confirme la recogida física de la comida, cambiando el estado a `collected` y guardando el histórico.
4. **Feed Global de Ofertas Activas:** Endpoint `GET /offers/active` para listar las ofertas con stock en la página de inicio.
5. **Vincular Trabajador a Local:** Endpoint para asociar administradores de local a su comercio.
6. **Módulo de Impacto Social / Dashboard de Métricas:** Endpoint `/analytics` para calcular ahorros consolidados.
7. **Pricing Dinámico (ML):** Integración con el modelo predictivo de excedentes y precios.
8. **Cron Jobs en Segundo Plano:** Expire automático de ofertas no vendidas y reservas no pagadas.
