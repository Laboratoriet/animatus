import { useEffect, useRef, useState } from "react";

function VideoBlock({ src, fullSrc, label = "Watch Video" }: { src: string; fullSrc?: string; label?: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [ended, setEnded] = useState(false);
  const [hasPlayed, setHasPlayed] = useState(false);

  // Play once when scrolled into view
  useEffect(() => {
    const video = videoRef.current;
    const container = containerRef.current;
    if (!video || !container) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasPlayed) {
          video.currentTime = 0;
          video.play();
          setHasPlayed(true);
        }
      },
      { threshold: 0.4 }
    );
    observer.observe(container);
    return () => observer.disconnect();
  }, [hasPlayed]);

  // Track when video ends
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    const onEnded = () => setEnded(true);
    video.addEventListener("ended", onEnded);
    return () => video.removeEventListener("ended", onEnded);
  }, []);

  // Fullscreen exit handler — restore short clip src
  useEffect(() => {
    const handleFsChange = () => {
      if (!document.fullscreenElement && videoRef.current) {
        videoRef.current.muted = true;
        if (fullSrc && videoRef.current.src !== new URL(src, location.href).href) {
          videoRef.current.src = src;
        }
      }
    };
    document.addEventListener("fullscreenchange", handleFsChange);
    return () => document.removeEventListener("fullscreenchange", handleFsChange);
  }, [src, fullSrc]);

  const handleReplay = () => {
    if (!videoRef.current) return;
    videoRef.current.currentTime = 0;
    videoRef.current.play();
    setEnded(false);
  };

  const handleWatch = () => {
    if (!videoRef.current) return;
    if (fullSrc) videoRef.current.src = fullSrc;
    videoRef.current.muted = false;
    videoRef.current.currentTime = 0;
    videoRef.current.play();
    videoRef.current.requestFullscreen?.();
    setEnded(false);
  };

  return (
    <div ref={containerRef} className="relative rounded-2xl overflow-hidden">
      <video
        ref={videoRef}
        src={src}
        muted
        playsInline
        preload="auto"
        className="w-full block"
      />
      {/* Buttons */}
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex flex-col items-center gap-3">
        <button
          onClick={handleWatch}
          className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-black/50 backdrop-blur-md border border-white/10 text-white/80 text-sm tracking-wide hover:bg-black/70 transition-all cursor-pointer"
        >
          <svg className="w-3.5 h-3.5" viewBox="0 0 16 16" fill="currentColor">
            <path d="M4 2.5v11l10-5.5L4 2.5z" />
          </svg>
          {label}
        </button>
        <button
          onClick={handleReplay}
          className="flex items-center gap-2 text-amber-400/80 text-sm tracking-wide hover:text-amber-300 transition-colors cursor-pointer"
          style={{ opacity: ended ? 1 : 0, pointerEvents: ended ? "auto" : "none", transition: "opacity 0.3s" }}
        >
          <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
            <path d="M1 4v6h6M23 20v-6h-6" />
            <path d="M20.49 9A9 9 0 005.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 013.51 15" />
          </svg>
          Replay
        </button>
      </div>
    </div>
  );
}

function VideoWithPoster({ src, poster, alt }: { src: string; poster: string; alt: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [hasPlayed, setHasPlayed] = useState(false);
  const [showVideo, setShowVideo] = useState(false);
  const [ended, setEnded] = useState(false);

  // Play once when scrolled into view
  useEffect(() => {
    const video = videoRef.current;
    const container = containerRef.current;
    if (!video || !container) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasPlayed) {
          setShowVideo(true);
          setEnded(false);
          video.currentTime = 0;
          video.play();
          setHasPlayed(true);
        }
      },
      { threshold: 0.4 }
    );
    observer.observe(container);
    return () => observer.disconnect();
  }, [hasPlayed]);

  // Fade back to image when video ends
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    const onEnded = () => {
      setEnded(true);
      setTimeout(() => setShowVideo(false), 600);
    };
    video.addEventListener("ended", onEnded);
    return () => video.removeEventListener("ended", onEnded);
  }, []);

  const handleReplay = () => {
    if (!videoRef.current) return;
    setShowVideo(true);
    setEnded(false);
    videoRef.current.currentTime = 0;
    videoRef.current.play();
  };

  return (
    <div ref={containerRef} className="relative rounded-2xl overflow-hidden">
      <img src={poster} alt={alt} className="w-full block" draggable={false} />
      <video
        ref={videoRef}
        src={src}
        muted
        playsInline
        preload="auto"
        className="absolute inset-0 w-full h-full object-cover transition-opacity duration-500"
        style={{ opacity: showVideo && !ended ? 1 : 0 }}
      />
      {ended && (
        <button
          onClick={handleReplay}
          className="absolute bottom-6 left-1/2 -translate-x-1/2 flex items-center gap-2 text-amber-400/80 text-sm tracking-wide hover:text-amber-300 transition-colors cursor-pointer"
        >
          <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
            <path d="M1 4v6h6M23 20v-6h-6" />
            <path d="M20.49 9A9 9 0 005.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 013.51 15" />
          </svg>
          Replay
        </button>
      )}
    </div>
  );
}

function FeatureIcon({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="flex flex-col items-center text-center gap-4 py-4">
      <div className="w-16 h-16 rounded-full bg-white/[0.05] border border-white/[0.08] flex items-center justify-center text-white/40">
        {icon}
      </div>
      <h4 className="text-base md:text-lg font-medium tracking-wide text-white/80">{title}</h4>
      <p className="text-sm md:text-base leading-relaxed text-white/50 max-w-[280px]">{description}</p>
    </div>
  );
}

function SectionHeading({ title, description }: { title: string; description?: string }) {
  return (
    <div className="w-full text-center mb-10">
      <h2 className="text-3xl md:text-5xl font-medium tracking-tight text-white/90 mb-4">
        {title}
      </h2>
      {description && (
        <p className="text-base md:text-lg leading-relaxed text-white/55 max-w-2xl mx-auto">
          {description}
        </p>
      )}
    </div>
  );
}

function App() {
  const [progress, setProgress] = useState(0);
  const [titleProgress, setTitleProgress] = useState(0);
  const [outroProgress, setOutroProgress] = useState(0);
  const heroRef = useRef<HTMLDivElement>(null);
  const titleRef = useRef<HTMLDivElement>(null);
  const outroRef = useRef<HTMLDivElement>(null);
  const rafRef = useRef<number>(0);

  useEffect(() => {
    const handleScroll = () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      rafRef.current = requestAnimationFrame(() => {
        if (heroRef.current) {
          const rect = heroRef.current.getBoundingClientRect();
          const heroHeight = heroRef.current.offsetHeight;
          const scrolled = -rect.top;
          const start = heroHeight * 0.05;
          const end = heroHeight * 0.4;
          const raw = (scrolled - start) / (end - start);
          setProgress(Math.min(1, Math.max(0, raw)));
        }
        if (titleRef.current) {
          const rect = titleRef.current.getBoundingClientRect();
          const vh = window.innerHeight;
          const raw = 1 - (rect.top - vh * 0.7) / (vh * 0.3);
          setTitleProgress(Math.min(1, Math.max(0, raw)));
        }
        if (outroRef.current) {
          const scrollBottom = window.innerHeight + window.scrollY;
          const docHeight = document.body.scrollHeight;
          const remaining = docHeight - scrollBottom;
          // Rest zone: nothing happens in last 350-270px, then dim in last 270px
          const restEnd = 270;
          const raw = remaining < restEnd ? 1 - (remaining / restEnd) : 0;
          setOutroProgress(Math.min(1, Math.max(0, raw)));
        }
      });
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => {
      window.removeEventListener("scroll", handleScroll);
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, []);

  const eased = progress < 0.5 ? 2 * progress * progress : 1 - Math.pow(-2 * progress + 2, 2) / 2;
  const titleEased = titleProgress < 0.5 ? 2 * titleProgress * titleProgress : 1 - Math.pow(-2 * titleProgress + 2, 2) / 2;
  // Smooth ease-in — gentle dim out
  const outroEased = outroProgress * outroProgress;

  return (
    <div className="bg-black">
      {/* ===== HERO ===== */}
      <div ref={heroRef} className="relative" style={{ height: "180vh" }}>
        <div className="sticky top-0 h-screen w-full overflow-hidden">
          <div className="absolute inset-0 pointer-events-none" style={{ background: `radial-gradient(ellipse 60% 60% at 50% 45%, rgba(100, 180, 255, ${eased * 0.08}) 0%, transparent 70%)` }} />
          <img src="/robot-off.jpg" alt="" className="absolute inset-0 w-full h-full object-cover" style={{ opacity: 1 - eased * 0.1 }} draggable={false} />
          <img src="/robot-on.jpg" alt="Animatus robot" className="absolute inset-0 w-full h-full object-cover" style={{ opacity: eased, willChange: "opacity" }} draggable={false} />
          <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center gap-3 pointer-events-none" style={{ opacity: Math.max(0, 1 - progress * 4) }}>
            <span className="text-[10px] tracking-[0.35em] uppercase text-white/30 font-light">Scroll</span>
            <div className="w-px h-10 overflow-hidden">
              <div className="w-px h-10 bg-gradient-to-b from-white/40 to-transparent animate-[scrollPulse_2s_ease-in-out_infinite]" />
            </div>
          </div>
        </div>
      </div>

      {/* ===== TITLE ===== */}
      <section ref={titleRef} className="flex flex-col items-center justify-center py-16 md:py-20">
        <h1 className="text-4xl sm:text-5xl md:text-7xl lg:text-8xl font-medium tracking-[0.3em] uppercase" style={{ opacity: titleEased * 0.9, transform: `translateY(${(1 - titleEased) * 30}px)`, color: "#fff", textShadow: titleEased > 0.3 ? `0 0 ${50 * titleEased}px rgba(100,180,255,${titleEased * 0.15})` : "none", willChange: "opacity, transform" }}>
          Animatus
        </h1>
        <p className="mt-6 md:mt-8 text-xs sm:text-sm md:text-base tracking-[0.4em] uppercase font-light" style={{ opacity: Math.max(0, (titleEased - 0.3) / 0.7) * 0.6, transform: `translateY(${Math.max(0, 1 - titleEased) * 20}px)`, color: "#fff", willChange: "opacity, transform" }}>
          Å gi sjel til maskiner
        </p>
      </section>

      {/* ===== HVA OM EN MASKIN ===== */}
      <section className="px-6 md:px-16 lg:px-24 py-12 md:py-16 text-center">
        <div className="max-w-[1100px] mx-auto flex flex-col items-center">
          <SectionHeading
            title="Hva om en maskin kunne være varm?"
            description="Teknologi blir stadig smartere. Men sjelden varmere. Animatus er et kunstprosjekt som stiller et enkelt spørsmål: hva skjer når vi designer en maskin for nærvær — ikke for effektivitet?"
          />
          <div className="w-full">
            <VideoWithPoster src="/video-oslo.mp4" poster="/robot-oslo.webp" alt="Animatus robot walking in Oslo" />
          </div>
        </div>
      </section>

      {/* ===== FEATURE GRID ===== */}
      <section className="px-6 md:px-16 lg:px-24 py-12 md:py-16 text-center border-t border-b border-white/[0.06]">
        <div className="max-w-[1100px] mx-auto grid grid-cols-2 md:grid-cols-4 gap-12 md:gap-8">
          <FeatureIcon
            icon={<svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" /></svg>}
            title="Personlighet"
            description="En karakter med verdier, humor og grenser. Designet, ikke generert."
          />
          <FeatureIcon
            icon={<svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.076-4.076a1.526 1.526 0 011.037-.443 48.282 48.282 0 005.68-.494c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" /></svg>}
            title="Samtale"
            description="Ekte dialog i sanntid. Lytter, forstår, svarer — som noen som er til stede."
          />
          <FeatureIcon
            icon={<svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path d="M21 7.5l-2.25-1.313M21 7.5v2.25m0-2.25l-2.25 1.313M3 7.5l2.25-1.313M3 7.5l2.25 1.313M3 7.5v2.25m9 3l2.25-1.313M12 12.75l-2.25-1.313M12 12.75V15m0 6.75l2.25-1.313M12 21.75V19.5m0 2.25l-2.25-1.313m0-16.875L12 2.25l2.25 1.313M21 14.25v2.25l-2.25 1.313m-13.5 0L3 16.5v-2.25" /></svg>}
            title="Kropp"
            description="En humanoid robot som går blant folk. 127 cm. Ikke bak glass — midt i rommet."
          />
          <FeatureIcon
            icon={<svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path d="M12 18v-5.25m0 0a6.01 6.01 0 001.5-.189m-1.5.189a6.01 6.01 0 01-1.5-.189m3.75 7.478a12.06 12.06 0 01-4.5 0m3.75 2.383a14.406 14.406 0 01-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 10-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" /></svg>}
            title="Hukommelse"
            description="Husker hvem den møtte. Lærer av erfaringer. Blir til over tid."
          />
        </div>
      </section>

      {/* ===== ET KUNSTPROSJEKT ===== */}
      <section className="px-6 md:px-16 lg:px-24 py-12 md:py-16 text-center">
        <div className="max-w-[1100px] mx-auto flex flex-col items-center">
          <SectionHeading
            title="Et kunstprosjekt, ikke et produkt"
            description="Animatus utforsker grensen mellom design, kunstig intelligens og menneskelig kontakt. Hva betyr det å gi en maskin sjel? Hvordan bør teknologi føles når den møter oss ansikt til ansikt? Prosjektet er initiert av Alkemist og utvikles i samarbeid med kunstnere, forskere og kulturinstitusjoner."
          />
          <div className="w-full"><VideoBlock src="/video-2-short.mp4" fullSrc="/video-2.mp4" label="Watch Video" /></div>
        </div>
      </section>

      {/* ===== PLATTFORMEN ===== */}
      <section className="px-6 md:px-16 lg:px-24 py-12 md:py-16 text-center">
        <div className="max-w-[1100px] mx-auto flex flex-col items-center">
          <SectionHeading
            title="Plattformen"
            description="Prosjektet bygger på Unitree G1 — en av verdens mest tilgjengelige humanoide roboter. Personligheten drives av en stor språkmodell. Bevegelse, samtale og karakter smelter sammen til noe som føles levende. Teknologien finnes. Spørsmålet er hva vi gjør med den."
          />
          <div className="w-full"><VideoBlock src="/video-1.mp4" label="Watch Video" /></div>

          <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-10 mt-20">
            <FeatureIcon
              icon={<svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" /></svg>}
              title="Kunstnerisk utforskning"
              description="Hva skjer når design møter robotikk? Animatus er en undersøkelse — ikke et svar."
            />
            <FeatureIcon
              icon={<svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" /></svg>}
              title="Offentlig møte"
              description="Roboten hører hjemme der folk er. Gater, gallerier, jubileer, scener."
            />
            <FeatureIcon
              icon={<svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" /></svg>}
              title="Åpen prosess"
              description="Vi dokumenterer alt — fra fabrikkgulvet i Kina til første møte med publikum i Oslo."
            />
          </div>
        </div>
      </section>

      {/* ===== FØRSTE KAPITTEL ===== */}
      <section className="px-6 md:px-16 lg:px-24 pt-12 md:pt-16 pb-0 text-center">
        <div className="max-w-[1100px] mx-auto flex flex-col items-center">
          <SectionHeading
            title="Første kapittel"
            description="Animatus søker sin første scene og sine første samarbeidspartnere. Et jubileum, en institusjon, en festival — et sted der hundre års historie møter fremtiden."
          />
        </div>
      </section>

      {/* ===== BOTTOM — ON → OFF ===== */}
      <div ref={outroRef} className="relative pb-10">
        <div className="w-full flex justify-center">
          <div className="max-w-lg w-full px-6 relative">
            <div className="absolute inset-0 pointer-events-none" style={{ background: `radial-gradient(ellipse 80% 80% at 50% 40%, rgba(100, 180, 255, ${(1 - outroEased) * 0.06}) 0%, transparent 70%)` }} />
            <div className="relative">
              <img src="/robot-sitting-on.webp" alt="Animatus robot" className="w-full h-auto block" style={{ opacity: 1 - outroEased, willChange: "opacity" }} draggable={false} />
              <img src="/robot-sitting-off.webp" alt="" className="absolute top-0 left-0 w-full h-full block" style={{ opacity: outroEased, willChange: "opacity" }} draggable={false} />
            </div>
          </div>
        </div>
      </div>

      {/* ===== PRE-FOOTER ===== */}
      <div className="px-6 md:px-16 lg:px-24 py-8 text-center">
        <p className="text-sm text-white/30 italic max-w-2xl mx-auto leading-relaxed">
          Prosjektet er i tidlig fase. Vi søker partnere, finansiering og den rette første scenen.
        </p>
      </div>

      {/* ===== FOOTER ===== */}
      <footer className="bg-white/[0.03] px-6 md:px-16 lg:px-24 pt-14 pb-10">
        <div className="max-w-[1100px] mx-auto">
          <div className="flex flex-col md:flex-row justify-between gap-10 md:gap-6">
            {/* Left — logo + company info */}
            <div className="flex flex-col gap-5">
              <a href="https://www.alkemist.no" target="_blank" rel="noopener noreferrer">
                <img src="/alkemist-logo.svg" alt="Alkemist" className="h-5 w-auto self-start" draggable={false} />
              </a>
              <div className="text-sm text-white/40 leading-relaxed">
                <p className="font-medium text-white/50">Alkemist (The Worst AS)</p>
                <p>Org. nr. 919 076 313</p>
                <p>Lilletorget 1, 0184 Oslo</p>
              </div>
            </div>
            {/* Right — contact + socials */}
            <div className="flex flex-col items-start md:items-end gap-5">
              <a href="mailto:kontakt@alkemist.no" className="text-sm tracking-[0.15em] text-white/60 hover:text-white/90 transition-colors">kontakt@alkemist.no</a>
              <div className="flex items-center gap-4">
                <a href="https://www.instagram.com/alkemist.no/" target="_blank" rel="noopener noreferrer" aria-label="Instagram" className="text-white/30 hover:text-white/60 transition-colors">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z" /></svg>
                </a>
                <a href="https://www.facebook.com/alkemist.no/" target="_blank" rel="noopener noreferrer" aria-label="Facebook" className="text-white/30 hover:text-white/60 transition-colors">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" /></svg>
                </a>
              </div>
            </div>
          </div>
          {/* Bottom row */}
          <div className="mt-10 pt-6 border-t border-white/[0.06] text-center">
            <p className="text-xs tracking-[0.1em] text-white/25">Privacy-Friendly Policy</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
