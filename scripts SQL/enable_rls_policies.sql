-- ============================================================================
-- Políticas RLS para el backend OctaFood
-- ============================================================================
-- El backend FastAPI se conecta a Supabase con la PUBLISHABLE (anon) key y
-- valida a los usuarios con JWT de Supabase Auth a nivel de API. Por lo tanto,
-- la base de datos debe permitir que el rol 'anon' lea/escriba estas tablas:
-- la seguridad queda delegada a la capa de aplicación (FastAPI).
--
-- Cómo aplicar: Supabase Dashboard -> SQL Editor -> New query -> pegar y Run.
-- Es idempotente (DROP POLICY IF EXISTS antes de crear).
-- ============================================================================

-- usuarios (registro, perfil, link-worker)
DROP POLICY IF EXISTS "backend_users_all" ON public.users;
CREATE POLICY "backend_users_all" ON public.users
  FOR ALL TO anon USING (true) WITH CHECK (true);

-- comercios
DROP POLICY IF EXISTS "backend_businesses_all" ON public.businesses;
CREATE POLICY "backend_businesses_all" ON public.businesses
  FOR ALL TO anon USING (true) WITH CHECK (true);

-- ofertas / bolsas sorpresa
DROP POLICY IF EXISTS "backend_offers_all" ON public.offers;
CREATE POLICY "backend_offers_all" ON public.offers
  FOR ALL TO anon USING (true) WITH CHECK (true);

-- reservas
DROP POLICY IF EXISTS "backend_reservations_all" ON public.reservations;
CREATE POLICY "backend_reservations_all" ON public.reservations
  FOR ALL TO anon USING (true) WITH CHECK (true);

-- reseñas
DROP POLICY IF EXISTS "backend_reviews_all" ON public.reviews;
CREATE POLICY "backend_reviews_all" ON public.reviews
  FOR ALL TO anon USING (true) WITH CHECK (true);

-- favoritos
DROP POLICY IF EXISTS "backend_user_favorites_all" ON public.user_favorites;
CREATE POLICY "backend_user_favorites_all" ON public.user_favorites
  FOR ALL TO anon USING (true) WITH CHECK (true);

-- bancos de alimentos
DROP POLICY IF EXISTS "backend_food_banks_all" ON public.food_banks;
CREATE POLICY "backend_food_banks_all" ON public.food_banks
  FOR ALL TO anon USING (true) WITH CHECK (true);

-- donaciones
DROP POLICY IF EXISTS "backend_donations_all" ON public.donations;
CREATE POLICY "backend_donations_all" ON public.donations
  FOR ALL TO anon USING (true) WITH CHECK (true);

-- datos históricos ML
DROP POLICY IF EXISTS "backend_ml_historical_data_all" ON public.ml_historical_data;
CREATE POLICY "backend_ml_historical_data_all" ON public.ml_historical_data
  FOR ALL TO anon USING (true) WITH CHECK (true);
