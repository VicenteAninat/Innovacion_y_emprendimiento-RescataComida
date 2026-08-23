"""Siembra datos de demostración para OctaFood contra el backend real.

Requisitos:
  - Backend FastAPI corriendo (uvicorn app.main:app --port 8000)
  - RLS configurado (ver scripts SQL/enable_rls_policies.sql)

Uso:
  .venv\\Scripts\\python seed_demo.py

Es idempotente: no duplica comercios, ofertas ni usuarios.

Cuentas que crea (o reutiliza):
  - admin_octa@example.com   / demo1234   (admin)
  - comercio@octafood.cl     / password123 (worker de "Panadería La Espiga")
  - cliente@octafood.cl      / password123 (customer con favoritos y pedidos)
"""

import os
import httpx
from datetime import datetime, timedelta

BASE = os.environ.get("OCTA_API_URL", "http://localhost:8000")
c = httpx.Client(base_url=BASE, timeout=30)


def call(method, path, body=None, token=None):
    h = {"Authorization": f"Bearer {token}"} if token else {}
    r = c.request(method, path, json=body, headers=h)
    if r.status_code >= 400:
        print(f"{method} {path} -> {r.status_code} {r.text[:200]}")
        return None
    return r.json()


def login_or_register(email, password, name, role, business_id=None):
    res = call("POST", "/auth/login", {"email": email, "password": password})
    if res:
        return res["access_token"]
    call(
        "POST",
        "/auth/register",
        {
            "email": email,
            "password": password,
            "name": name,
            "role": role,
            "business_id": business_id,
        },
    )
    res = call("POST", "/auth/login", {"email": email, "password": password})
    if not res:
        raise RuntimeError(f"No se pudo autenticar {email}")
    return res["access_token"]


def ensure_business(token, rut, name, category, address, location):
    existing = call("GET", "/businesses/get_all", token=token) or []
    for b in existing:
        if b.get("name") == name:
            print(f"Comercio existente: {name} (id={b['id']})")
            return b
    b = call(
        "POST",
        "/businesses/create",
        {
            "rut": rut,
            "name": name,
            "category": category,
            "address": address,
            "location": location,
        },
        token=token,
    )
    if not b:
        raise RuntimeError(f"No se pudo crear el comercio {name}")
    print(f"Comercio creado: {name} (id={b['id']})")
    return b


def seed_offers_if_empty(token, business, offers):
    existing = call("GET", f"/offers/business/{business['id']}", token=token) or []
    if existing:
        print(f"El comercio {business['name']} ya tiene {len(existing)} oferta(s).")
        return
    now = datetime.now()
    for o in offers:
        o = dict(o)
        o["business_id"] = business["id"]
        o["pickup_start_time"] = (now + timedelta(hours=2)).isoformat()
        o["pickup_end_time"] = (now + timedelta(hours=4)).isoformat()
        res = call("POST", "/offers/create", o, token=token)
        print(f"Oferta creada: {res['title']} (id={res['id']})")


def main():
    t_admin = login_or_register(
        "admin_octa@example.com", "demo1234", "Admin Demo", "admin"
    )

    businesses = [
        (
            "76.123.456-1",
            "Panadería La Espiga",
            "bakery",
            "Av. Providencia 1234, Providencia",
            "POINT(-70.6091 -33.4270)",
        ),
        (
            "77.987.654-2",
            "Nori Sushi Bar",
            "sushi",
            "Av. Manuel Montt 890, Providencia",
            "POINT(-70.6152 -33.4350)",
        ),
        (
            "78.555.111-3",
            "Café Lumière",
            "cafe",
            "Calle Suecia 45, Providencia",
            "POINT(-70.6010 -33.4230)",
        ),
        (
            "79.222.333-4",
            "Trattoria Bella Roma",
            "restaurant",
            "Av. Italia 1200, Providencia",
            "POINT(-70.6190 -33.4400)",
        ),
    ]
    created = [ensure_business(t_admin, *args) for args in businesses]
    b_bakery, b_sushi, b_cafe, b_italian = created

    t_worker = login_or_register(
        "comercio@octafood.cl",
        "password123",
        "José Panadero",
        "worker",
        business_id=b_bakery["id"],
    )
    t_cust = login_or_register(
        "cliente@octafood.cl", "password123", "Marta García", "customer"
    )

    seed_offers_if_empty(
        t_worker,
        b_bakery,
        [
            {
                "title": "Bolsa Sorpresa de Pan",
                "description": "Pan artesanal, croissants, galletas y bollería variada del día.",
                "original_price": 11990,
                "discounted_price": 3990,
                "quantity_available": 3,
            },
            {
                "title": "Bolsa Sorpresa de Pastelería",
                "description": "Tartas, queques, tortas y postres finos preparados en el día.",
                "original_price": 14990,
                "discounted_price": 4990,
                "quantity_available": 2,
            },
        ],
    )
    seed_offers_if_empty(
        t_admin,
        b_sushi,
        [
            {
                "title": "Bolsa Sorpresa de Sushi",
                "description": "Nigiri, maki, temaki y entrantes varios. Fresco y preparado cada día.",
                "original_price": 21990,
                "discounted_price": 6990,
                "quantity_available": 5,
            }
        ],
    )
    seed_offers_if_empty(
        t_admin,
        b_cafe,
        [
            {
                "title": "Bolsa Sorpresa de Café",
                "description": "Sándwiches, wraps, pasteles y una bebida sorpresa.",
                "original_price": 13990,
                "discounted_price": 4490,
                "quantity_available": 2,
            }
        ],
    )
    seed_offers_if_empty(
        t_admin,
        b_italian,
        [
            {
                "title": "Bolsa Sorpresa Italiana",
                "description": "Pasta fresca, pizza, entrantes y alguna sorpresa dulce.",
                "original_price": 17990,
                "discounted_price": 5990,
                "quantity_available": 7,
            }
        ],
    )

    # Favorito del cliente hacia el sushi
    favs = call("GET", "/favorites/my-favorites", token=t_cust) or []
    if not any(f.get("id") == b_sushi["id"] for f in favs):
        call("POST", f"/favorites/add/{b_sushi['id']}", {}, token=t_cust)
        print("Favorito agregado: Nori Sushi Bar")

    # Una reserva pagada y retirada con reseña (para probar el flujo completo)
    my = call("GET", "/reservations/my-reservations", token=t_cust) or []
    if not any(r["status"] == "collected" for r in my):
        offers = call("GET", f"/offers/business/{b_bakery['id']}", token=t_cust) or []
        active = [o for o in offers if o["status"] == "active" and o["quantity_available"] > 0]
        if active:
            o = active[0]
            r = call(
                "POST",
                "/reservations/create",
                {"offer_id": o["id"], "quantity": 1, "payment_method": "card"},
                token=t_cust,
            )
            call("POST", f"/reservations/pay/{r['id']}", {}, token=t_cust)
            call("PATCH", f"/reservations/update/{r['id']}", {"status": "collected"}, token=t_worker)
            reviews = call("GET", f"/reviews/business/{b_bakery['id']}", token=t_cust) or []
            if not reviews:
                call(
                    "POST",
                    "/reviews/create",
                    {
                        "reservation_id": r["id"],
                        "rating": 5,
                        "comment": "El pan estaba increíble, repetiré sin duda.",
                    },
                    token=t_cust,
                )
                print("Reserva pagada/retirada + reseña creada.")

    feed = call("GET", "/offers/active?limit=50", token=t_cust) or []
    print(f"\nOK: {len(feed)} ofertas activas visibles para el cliente.")
    print("Listo. Puedes probar el frontend con las cuentas de arriba.")


if __name__ == "__main__":
    main()
