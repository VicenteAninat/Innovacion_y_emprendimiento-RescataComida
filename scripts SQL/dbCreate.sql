-- Habilitar extensión espacial y uuid-ossp
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  name VARCHAR,
  email VARCHAR UNIQUE NOT NULL,
  phone VARCHAR,
  role VARCHAR DEFAULT 'customer' CHECK (role IN ('customer', 'worker', 'admin')),
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
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
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
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
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
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
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

-- 4. Triggers y Funciones de Base de Datos
-- Verificar y descontar stock automáticamente al insertar una reserva
CREATE OR REPLACE FUNCTION verificar_y_descontar_stock()
RETURNS TRIGGER AS $$
DECLARE
    stock_actual INT;
BEGIN
    -- Seleccionamos el stock de la oferta bloqueando la fila (FOR UPDATE)
    -- para evitar condiciones de carrera en reservas simultáneas.
    SELECT quantity_available INTO stock_actual
    FROM offers
    WHERE id = NEW.offer_id
    FOR UPDATE;

    -- Verificar si existe la oferta
    IF stock_actual IS NULL THEN
        RAISE EXCEPTION 'La oferta no existe.' USING ERRCODE = 'P0002';
    END IF;

    -- Verificar si el stock es suficiente
    IF stock_actual < NEW.quantity THEN
        RAISE EXCEPTION 'Stock insuficiente para la oferta seleccionada.' USING ERRCODE = 'UE001';
    END IF;

    -- Descontar el stock de manera segura
    UPDATE offers
    SET quantity_available = quantity_available - NEW.quantity
    WHERE id = NEW.offer_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tg_verificar_y_descontar_stock ON reservations;
CREATE TRIGGER tg_verificar_y_descontar_stock
BEFORE INSERT ON reservations
FOR EACH ROW
EXECUTE FUNCTION verificar_y_descontar_stock();


-- Trigger para devolver el stock al cancelar o eliminar una reserva
CREATE OR REPLACE FUNCTION devolver_stock_al_cancelar_o_eliminar()
RETURNS TRIGGER AS $$
BEGIN
    -- Caso 1: Actualización (Cambio de estado a 'cancelled')
    IF (TG_OP = 'UPDATE') THEN
        IF (NEW.status = 'cancelled' AND OLD.status != 'cancelled') THEN
            UPDATE offers
            SET quantity_available = quantity_available + OLD.quantity
            WHERE id = OLD.offer_id;
        END IF;
    END IF;

    -- Caso 2: Eliminación física
    IF (TG_OP = 'DELETE') THEN
        -- Solo devolvemos stock si la reserva no estaba ya cancelada
        IF (OLD.status != 'cancelled') THEN
            UPDATE offers
            SET quantity_available = quantity_available + OLD.quantity
            WHERE id = OLD.offer_id;
        END IF;
    END IF;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tg_devolver_stock_al_cancelar_o_eliminar ON reservations;
CREATE TRIGGER tg_devolver_stock_al_cancelar_o_eliminar
AFTER UPDATE OR DELETE ON reservations
FOR EACH ROW
EXECUTE FUNCTION devolver_stock_al_cancelar_o_eliminar();


-- Función para cancelar automáticamente las reservas expiradas (que superan los 15 minutos en 'pending')
-- Esto disparará automáticamente el trigger de devolución de stock
CREATE OR REPLACE FUNCTION cancelar_reservas_expiradas()
RETURNS INTEGER AS $$
DECLARE
    cantidad_canceladas INTEGER;
BEGIN
    WITH canceladas AS (
        UPDATE reservations
        SET status = 'cancelled'
        WHERE status = 'pending'
          AND created_at < NOW() - INTERVAL '15 minutes'
        RETURNING id
    )
    SELECT COUNT(*) INTO cantidad_canceladas FROM canceladas;

    RETURN cantidad_canceladas;
END;
$$ LANGUAGE plpgsql;

-- Programación de la rutina utilizando pg_cron (para ejecutar en Supabase)
-- CREATE EXTENSION IF NOT EXISTS pg_cron;
-- SELECT cron.schedule('limpieza-reservas-expiradas', '*/1 * * * *', 'SELECT cancelar_reservas_expiradas();');
-- Para pausar/desprogramar el cron job:
-- SELECT cron.unschedule('limpieza-reservas-expiradas');