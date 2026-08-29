# OctaFood Frontend (React + Vite + Tailwind)

Interfaz móvil de la plataforma de bolsas sorpresa, conectada al backend
FastAPI (`/app`).

## Estructura

```
src/
  app/App.tsx            # Raíz: frame del teléfono, gating por rol
  features/
    auth/                # AuthContext, LoginScreen, ProviderGate
    shared/              # SectionHeader, SearchBar, BottomNav
    consumer/            # Flujo cliente: home, explorar, pedidos, perfil
      components/        # TopBar, FlashDeal, CategoryPills, cards, MapView
      screens/           # HomeScreen, ExploreScreen, OrdersScreen, ProfileScreen
      sheets/            # Detalle restaurante/bolsa, pago, reseña
    provider/            # Flujo comerciante: dashboard, bolsas, pedidos, store
  lib/
    api/                 # Cliente fetch y endpoints del backend
    data/                # Caché de entidades y mapeos (Offer→Bag, etc.)
    hooks/               # useCountdown
    types.ts             # Tipos del backend y modelos de vista
    format.ts            # Formateo CLP, fechas, geolocalización
    images.ts            # Categorías e imágenes placeholder
```

## Requisitos

- Node 18+
- Backend FastAPI corriendo: `uvicorn app.main:app --reload` (ver `../README.md`)

## Ejecutar

1. Copia `.env.example` a `.env` y ajusta `VITE_API_URL`
   (por defecto `http://localhost:8081`).
2. `npm install`
3. `npm run dev`

## Integración con el backend

- **Auth**: `/auth/login`, `/auth/register`, `/auth/profile` (token Bearer en
  `localStorage`).
- **Feed**: `/offers/active` (opcional lat/lng para cercanía).
- **Reservas**: crear → pagar (15 min) → cancelar; historial en "Pedidos".
- **Reseñas**: solo reservas `collected`/`completed`, una por reserva.
- **Favoritos**: por comercio (`/favorites/*`).
- **Comerciante**: publicar/editar/eliminar bolsas, ver pedidos del local.
  Requiere cuenta `worker` con `business_id` vinculado.

### Mapeo de datos (modelo UI ↔ backend)

| Modelo UI (Bag)   | Backend (`offers`)            |
| :---------------- | :---------------------------- |
| `price`           | `discounted_price`            |
| `originalValue`   | `original_price`              |
| `remaining`       | `quantity_available`          |
| `type` / `description` | `title` / `description`   |
| `pickup`          | `pickup_start_time – pickup_end_time` |
| `co2Saved` / `kgSaved` | `co2_avoided_per_unit` / `kg_saved_per_unit` |
| `restaurant*`     | `business` anidado (`name`, `category`, `address`, `location`) |
| `rating` / `reviews` | calculados desde `/reviews/business/{id}` |
| `image` / `tags`  | derivados de la categoría (el backend no guarda imágenes) |

Los favoritos son por **comercio** (`business_id`), no por bolsa. La donación del
checkout se guarda como `transaction_fee` de la reserva.

### Estados de una reserva

```
pending → paid → collected   (retiro confirmado por el worker)
    └───────→ cancelled      (usuario cancela, o expira a los 15 min)
```

- El cliente puede **pagar** solo en estado `pending` (ventana de 15 min).
- El worker **marca el retiro** con `PATCH /reservations/update/{id}` → `collected`.
- Solo reservas `collected`/`completed` son **reseñables**.
