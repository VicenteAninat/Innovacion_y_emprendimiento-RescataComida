import { ArrowLeft, ArrowRight, Lightbulb, Store } from "lucide-react";

/**
 * Pantalla para clientes que intentan entrar al panel de comercio sin una
 * cuenta worker: explica el requisito y permite cambiar de cuenta o volver.
 */
export default function ProviderGate({
  onBack,
  onSwitchAccount,
}: {
  onBack: () => void;
  onSwitchAccount: () => void;
}) {
  return (
    <div className="h-full flex flex-col overflow-hidden">
      <div className="flex-1 overflow-y-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
        <div className="px-5 pt-5 pb-4 flex items-center gap-3">
          <button
            onClick={onBack}
            className="w-9 h-9 rounded-full bg-muted flex items-center justify-center"
          >
            <ArrowLeft size={18} className="text-foreground" />
          </button>
          <h1
            className="font-black text-2xl text-foreground"
            style={{ fontFamily: "'Righteous', sans-serif" }}
          >
            Modo proveedor
          </h1>
        </div>

        <div className="px-5">
          <div className="bg-card border border-border rounded-3xl p-6 text-center mb-5">
            <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-4">
              <Store size={28} className="text-primary" />
            </div>
            <p className="font-black text-base text-foreground mb-2">
              Tu cuenta actual es de cliente
            </p>
            <p className="text-xs text-muted-foreground leading-relaxed mb-5">
              Para gestionar un comercio y publicar bolsas necesitas una cuenta
              de tipo <span className="font-bold">worker</span> vinculada a tu
              local. Regístrate como comercio o pide a un administrador que
              asocie tu cuenta a un business_id.
            </p>
            <button
              onClick={onSwitchAccount}
              className="w-full h-12 rounded-2xl bg-primary text-white text-sm font-bold flex items-center justify-center gap-2"
            >
              Cambiar de cuenta
              <ArrowRight size={16} />
            </button>
          </div>

          <div className="bg-secondary/10 border border-secondary/20 rounded-2xl p-3.5 flex items-start gap-2">
            <Lightbulb size={16} className="text-secondary shrink-0 mt-0.5" />
            <p className="text-[11px] text-foreground/70 leading-relaxed">
              Flujo recomendado: crea una cuenta con rol "comercio" en la
              pantalla de registro y luego contacta al admin del proyecto para
              vincularla a tu negocio.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
