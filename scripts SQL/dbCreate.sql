CREATE TABLE "users" (
  "id" serial PRIMARY KEY,
  "name" varchar,
  "email" varchar UNIQUE NOT NULL,
  "password_hash" varchar,
  "phone" varchar,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "businesses" (
  "id" serial PRIMARY KEY,
  "rut" varchar UNIQUE NOT NULL,
  "name" varchar,
  "category" varchar,
  "address" varchar,
  "location" "geometry(Point,4326)",
  "is_premium" boolean DEFAULT false,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "offers" (
  "id" serial PRIMARY KEY,
  "business_id" integer,
  "title" varchar NOT NULL,
  "description" text,
  "original_price" decimal(10,2),
  "discounted_price" decimal(10,2),
  "quantity_available" integer DEFAULT 1,
  "pickup_start_time" timestamp NOT NULL,
  "pickup_end_time" timestamp NOT NULL,
  "status" varchar DEFAULT 'active',
  "kg_saved_per_unit" decimal(5,2),
  "co2_avoided_per_unit" decimal(5,2),
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "reservations" (
  "id" serial PRIMARY KEY,
  "user_id" integer,
  "offer_id" integer,
  "quantity" integer DEFAULT 1,
  "total_price" decimal(10,2),
  "status" varchar DEFAULT 'pending',
  "payment_method" varchar,
  "transaction_fee" decimal(10,2),
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "reviews" (
  "id" serial PRIMARY KEY,
  "user_id" integer,
  "business_id" integer,
  "reservation_id" integer,
  "rating" integer NOT NULL,
  "comment" text,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "user_favorites" (
  "user_id" integer,
  "business_id" integer,
  "created_at" timestamp DEFAULT (now()),
  PRIMARY KEY ("user_id", "business_id")
);

CREATE TABLE "food_banks" (
  "id" serial PRIMARY KEY,
  "rut" varchar UNIQUE NOT NULL,
  "name" varchar,
  "contact_email" varchar,
  "contact_phone" varchar,
  "address" varchar,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "donations" (
  "id" serial PRIMARY KEY,
  "business_id" integer,
  "food_bank_id" integer,
  "description" text,
  "weight_kg" decimal(8,2),
  "tax_deductible_receipt_url" varchar,
  "donated_at" timestamp DEFAULT (now())
);

CREATE TABLE "ml_historical_data" (
  "id" serial PRIMARY KEY,
  "business_id" integer,
  "date" date,
  "hour" integer,
  "weather_condition" varchar,
  "surplus_kg" decimal(8,2),
  "sold_bags" integer,
  "wasted_bags" integer,
  "dynamic_pricing_suggested" decimal(10,2)
);

COMMENT ON TABLE "users" IS 'Usuarios consumidores finales de la plataforma';

COMMENT ON TABLE "businesses" IS 'Comercios, restaurantes y supermercados asociados';

COMMENT ON TABLE "offers" IS 'Publicación de excedentes (Bolsas sorpresa)';

COMMENT ON TABLE "reservations" IS 'Transacciones y reservas de los usuarios';

COMMENT ON TABLE "user_favorites" IS 'Sistema de favoritos para los consumidores';

COMMENT ON TABLE "donations" IS 'Registro de donaciones de comercios a bancos de alimentos';

COMMENT ON TABLE "ml_historical_data" IS 'Datos históricos consolidados para entrenar el modelo de predicción de excedentes y pricing dinámico';

ALTER TABLE "offers" ADD FOREIGN KEY ("business_id") REFERENCES "businesses" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "reservations" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "reservations" ADD FOREIGN KEY ("offer_id") REFERENCES "offers" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "reviews" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "reviews" ADD FOREIGN KEY ("business_id") REFERENCES "businesses" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "reviews" ADD FOREIGN KEY ("reservation_id") REFERENCES "reservations" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "user_favorites" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "user_favorites" ADD FOREIGN KEY ("business_id") REFERENCES "businesses" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "donations" ADD FOREIGN KEY ("business_id") REFERENCES "businesses" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "donations" ADD FOREIGN KEY ("food_bank_id") REFERENCES "food_banks" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "ml_historical_data" ADD FOREIGN KEY ("business_id") REFERENCES "businesses" ("id") DEFERRABLE INITIALLY IMMEDIATE;
