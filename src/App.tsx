import { useEffect, useRef, useState } from "react";

function App() {
  const [progress, setProgress] = useState(0);
  const [titleProgress, setTitleProgress] = useState(0);
  const heroRef = useRef<HTMLDivElement>(null);
  const titleRef = useRef<HTMLDivElement>(null);
  const rafRef = useRef<number>(0);

  useEffect(() => {
    const handleScroll = () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      rafRef.current = requestAnimationFrame(() => {
        // Robot transition
        if (heroRef.current) {
          const rect = heroRef.current.getBoundingClientRect();
          const heroHeight = heroRef.current.offsetHeight;
          const scrolled = -rect.top;
          const start = heroHeight * 0.05;
          const end = heroHeight * 0.3;
          const raw = (scrolled - start) / (end - start);
          setProgress(Math.min(1, Math.max(0, raw)));
        }

        // Title fade-in
        if (titleRef.current) {
          const rect = titleRef.current.getBoundingClientRect();
          const vh = window.innerHeight;
          // Start fading in when top enters bottom 30% of viewport
          const raw = 1 - (rect.top - vh * 0.7) / (vh * 0.3);
          setTitleProgress(Math.min(1, Math.max(0, raw)));
        }
      });
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => {
      window.removeEventListener("scroll", handleScroll);
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, []);

  // Ease-in-out
  const eased =
    progress < 0.5
      ? 2 * progress * progress
      : 1 - Math.pow(-2 * progress + 2, 2) / 2;

  const titleEased =
    titleProgress < 0.5
      ? 2 * titleProgress * titleProgress
      : 1 - Math.pow(-2 * titleProgress + 2, 2) / 2;

  return (
    <>
      {/* Hero: scroll room for robot transition */}
      <div ref={heroRef} className="relative" style={{ height: "200vh" }}>
        {/* Sticky viewport-filling container */}
        <div className="sticky top-0 h-screen w-full overflow-hidden bg-black">
          {/* Ambient glow */}
          <div
            className="absolute inset-0 pointer-events-none"
            style={{
              background: `radial-gradient(ellipse 60% 60% at 50% 45%, rgba(100, 180, 255, ${eased * 0.08}) 0%, transparent 70%)`,
            }}
          />

          {/* Robot OFF */}
          <img
            src="/robot-off.jpg"
            alt=""
            className="absolute inset-0 w-full h-full object-cover"
            style={{ opacity: 1 - eased * 0.1 }}
            draggable={false}
          />

          {/* Robot ON */}
          <img
            src="/robot-on.jpg"
            alt="Animatus robot"
            className="absolute inset-0 w-full h-full object-cover"
            style={{
              opacity: eased,
              willChange: "opacity",
            }}
            draggable={false}
          />

          {/* Scroll indicator */}
          <div
            className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center gap-3 pointer-events-none"
            style={{ opacity: Math.max(0, 1 - progress * 4) }}
          >
            <span className="text-[10px] tracking-[0.35em] uppercase text-white/30 font-light">
              Scroll
            </span>
            <div className="w-px h-10 overflow-hidden">
              <div className="w-px h-10 bg-gradient-to-b from-white/40 to-transparent animate-[scrollPulse_2s_ease-in-out_infinite]" />
            </div>
          </div>
        </div>
      </div>

      {/* Title section - below the robot */}
      <section
        ref={titleRef}
        className="relative bg-black flex flex-col items-center justify-center py-24 md:py-32"
      >
        <h1
          className="text-4xl sm:text-5xl md:text-7xl lg:text-8xl font-medium tracking-[0.3em] uppercase"
          style={{
            opacity: titleEased * 0.9,
            transform: `translateY(${(1 - titleEased) * 30}px)`,
            color: "#ffffff",
            textShadow:
              titleEased > 0.3
                ? `0 0 ${50 * titleEased}px rgba(100, 180, 255, ${titleEased * 0.15})`
                : "none",
            willChange: "opacity, transform",
          }}
        >
          Animatus
        </h1>
        <p
          className="mt-6 md:mt-8 text-xs sm:text-sm md:text-base tracking-[0.4em] uppercase font-light"
          style={{
            opacity: Math.max(0, (titleEased - 0.3) / 0.7) * 0.6,
            transform: `translateY(${Math.max(0, 1 - titleEased) * 20}px)`,
            color: "#ffffff",
            willChange: "opacity, transform",
          }}
        >
          Awakening Intelligence
        </p>
      </section>

      {/* Below-fold placeholder */}
      <section className="min-h-screen bg-black flex items-center justify-center">
        <p className="text-white/15 text-xs tracking-[0.25em] uppercase font-light">
          More coming soon
        </p>
      </section>
    </>
  );
}

export default App;
