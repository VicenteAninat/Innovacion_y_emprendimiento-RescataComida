import { useEffect, useState } from "react";
import { useAuth } from "../features/auth/AuthContext";
import LoginScreen from "../features/auth/LoginScreen";
import ProviderGate from "../features/auth/ProviderGate";
import ConsumerApp from "../features/consumer/ConsumerApp";
import ProviderApp from "../features/provider/ProviderApp";

function SplashScreen() {
  return (
    <div className="h-full flex items-center justify-center">
      <div className="w-9 h-9 rounded-full border-2 border-primary/30 border-t-primary animate-spin" />
    </div>
  );
}

export default function App() {
  const { user, loading, logout } = useAuth();
  const [viewMode, setViewMode] = useState<"consumer" | "provider">("consumer");

  // Al cambiar de usuario (login/logout), el modo se adapta al rol real.
  useEffect(() => {
    if (user) {
      setViewMode(user.role === "customer" ? "consumer" : "provider");
    } else {
      setViewMode("consumer");
    }
  }, [user?.id]); // eslint-disable-line react-hooks/exhaustive-deps

  const isMerchant = user?.role === "worker" || user?.role === "admin";

  return (
    <div
      className="min-h-screen flex items-center justify-center py-0 sm:py-8"
      style={{
        background: "#C8BEB4",
        fontFamily: "'DM Sans', sans-serif",
      }}
    >
      <div className="relative w-full sm:w-[390px] h-screen sm:h-[844px] bg-background sm:rounded-[3rem] overflow-hidden sm:shadow-[0_48px_128px_rgba(0,0,0,0.4)] sm:border-[7px] sm:border-[rgba(0,0,0,0.15)]">
        {loading ? (
          <SplashScreen />
        ) : !user ? (
          <LoginScreen />
        ) : viewMode === "provider" && !isMerchant ? (
          <ProviderGate
            onBack={() => setViewMode("consumer")}
            onSwitchAccount={logout}
          />
        ) : viewMode === "provider" ? (
          <ProviderApp
            onSwitchToConsumer={() => setViewMode("consumer")}
            onLogout={logout}
          />
        ) : (
          <ConsumerApp
            onOpenMerchant={() => setViewMode("provider")}
            onLogout={logout}
          />
        )}
      </div>
    </div>
  );
}
