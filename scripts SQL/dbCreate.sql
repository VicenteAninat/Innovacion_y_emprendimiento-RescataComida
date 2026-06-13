-- Habilitar extensión espacial
CREATE EXTENSION IF NOT EXISTS postgis;

-- 1. Tablas independientes
CREATE TABLE businesses (
  id SERIAL PRIMARY KEY,
  rut VARCHAR UNIQUE NOT NULL,
  name VARCHAR,
  category VARCHAR,
  address VARCHAR,
  location geometry(Point, 4326),
  is_premium BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE food_banks (
  id SERIAL PRIMARY KEY,
  rut VARCHAR UNIQUE NOT NULL,
  name VARCHAR,
  contact_email VARCHAR,
  contact_phone VARCHAR,
  address VARCHAR,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tablas dependientes
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  email VARCHAR UNIQUE NOT NULL,
  password_hash VARCHAR,
  phone VARCHAR,
  role VARCHAR DEFAULT 'customer',
  business_id INTEGER REFERENCES businesses(id) ON DELETE SET NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE offers (
  id SERIAL PRIMARY KEY,
  business_id INTEGER REFERENCES businesses(id) ON DELETE CASCADE,
  title VARCHAR NOT NULL,
  description TEXT,
  original_price DECIMAL(10,2),
  discounted_price DECIMAL(10,2),
  quantity_available INTEGER DEFAULT 1,
  pickup_start_time TIMESTAMP NOT NULL,
  pickup_end_time TIMESTAMP NOT NULL,
  status VARCHAR DEFAULT 'active',
  kg_saved_per_unit DECIMAL(5,2),
  co2_avoided_per_unit DECIMAL(5,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reservations (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  offer_id INTEGER REFERENCES offers(id) ON DELETE CASCADE,
  quantity INTEGER DEFAULT 1,
  total_price DECIMAL(10,2),
  status VARCHAR DEFAULT 'pending',
  payment_method VARCHAR,
  transaction_fee DECIMAL(10,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reviews (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  business_id INTEGER REFERENCES businesses(id) ON DELETE CASCADE,
  reservation_id INTEGER UNIQUE REFERENCES reservations(id) ON DELETE CASCADE,
  rating INTEGER NOT NULL,
  comment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ml_historical_data (
  id SERIAL PRIMARY KEY,
  business_id INTEGER REFERENCES businesses(id) ON DELETE CASCADE,
  date DATE,
  hour INTEGER,
  weather_condition VARCHAR,
  surplus_kg DECIMAL(8,2),
  sold_bags INTEGER,
  wasted_bags INTEGER,
  dynamic_pricing_suggested DECIMAL(10,2)
);

CREATE TABLE donations (
  id SERIAL PRIMARY KEY,
  business_id INTEGER REFERENCES businesses(id) ON DELETE CASCADE,
  food_bank_id INTEGER REFERENCES food_banks(id) ON DELETE CASCADE,
  description TEXT,
  weight_kg DECIMAL(8,2),
  tax_deductible_receipt_url VARCHAR,
  donated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_favorites (
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  business_id INTEGER REFERENCES businesses(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, business_id)
);

-- 3. Comentarios de Documentación
COMMENT ON TABLE users IS 'Usuarios consumidores finales y administradores de locales';
COMMENT ON TABLE businesses IS 'Comercios, restaurantes y supermercados asociados';
COMMENT ON TABLE offers IS 'Publicación de excedentes (Bolsas sorpresa)';
COMMENT ON TABLE reservations IS 'Transacciones y reservas de los usuarios';
COMMENT ON TABLE user_favorites IS 'Sistema de favoritos para los consumidores';
COMMENT ON TABLE donations IS 'Registro de donaciones de comercios a bancos de alimentos';
COMMENT ON TABLE ml_historical_data IS 'Datos históricos para entrenar el modelo de ML';