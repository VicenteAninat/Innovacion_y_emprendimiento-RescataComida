import { useEffect, useRef, useState } from "react";

/**
 * Cuenta regresiva hacia un timestamp objetivo (ms).
 * Si el objetivo no es válido o ya pasó, usa una ventana por defecto de 1.8 h.
 */
export function useCountdown(targetMs?: number) {
  const target = useRef<number>(
    targetMs && !isNaN(targetMs) && targetMs > Date.now()
      ? targetMs
      : Date.now() + 1.8 * 3_600_000,
  );
  const [t, setT] = useState({ h: 0, m: 0, s: 0 });

  useEffect(() => {
    const calc = () => {
      const diff = Math.max(0, target.current - Date.now());
      setT({
        h: Math.floor(diff / 3_600_000),
        m: Math.floor((diff % 3_600_000) / 60_000),
        s: Math.floor((diff % 60_000) / 1_000),
      });
    };
    calc();
    const id = setInterval(calc, 1000);
    return () => clearInterval(id);
  }, []);

  const pad = (n: number) => String(n).padStart(2, "0");
  return `${pad(t.h)}:${pad(t.m)}:${pad(t.s)}`;
}
