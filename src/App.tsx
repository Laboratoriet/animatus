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

function MediaPlaceholder({ aspect = "video" }: { aspect?: "video" | "square" | "wide" | "tall" }) {
  const ratios = { video: "aspect-video", square: "aspect-square", wide: "aspect-[2/1]", tall: "aspect-[3/4]" };
  return (
    <div className={`${ratios[aspect]} w-full rounded-2xl bg-white/[0.04] border border-white/[0.06] flex items-center justify-center`}>
      <div className="flex flex-col items-center gap-2 text-white/15">
        <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
          <path d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909M3.75 21h16.5A2.25 2.25 0 0022.5 18.75V5.25A2.25 2.25 0 0020.25 3H3.75A2.25 2.25 0 001.5 5.25v13.5A2.25 2.25 0 003.75 21z" />
        </svg>
        <span className="text-[10px] tracking-widest uppercase">Placeholder</span>
      </div>
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
          // Trigger in the last 350px of scroll — gentle dim out
          const remaining = docHeight - scrollBottom;
          const raw = 1 - (remaining / 350);
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
          Awakening Intelligence
        </p>
      </section>

      {/* ===== EXPERT MODE ===== */}
      <section className="px-6 md:px-16 lg:px-24 py-12 md:py-16 text-center">
        <div className="max-w-[1100px] mx-auto flex flex-col items-center">
          <SectionHeading
            title="Expert Mode"
            description="Animatus monitors its environment in detail. It can detect, learn, and adapt in real-time, making intelligent decisions to keep things running smoothly."
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
            icon={<svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" /></svg>}
            title="Touch-sensitive Skin"
            description="Flexible, responsive surface that detects contact and adjusts accordingly."
          />
          <FeatureIcon
            icon={<svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" /><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>}
            title="Spatial Awareness"
            description="Dynamic 3D environment mapping for precise, confident navigation."
          />
          <FeatureIcon
            icon={<svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path d="M21 7.5l-2.25-1.313M21 7.5v2.25m0-2.25l-2.25 1.313M3 7.5l2.25-1.313M3 7.5l2.25 1.313M3 7.5v2.25m9 3l2.25-1.313M12 12.75l-2.25-1.313M12 12.75V15m0 6.75l2.25-1.313M12 21.75V19.5m0 2.25l-2.25-1.313m0-16.875L12 2.25l2.25 1.313M21 14.25v2.25l-2.25 1.313m-13.5 0L3 16.5v-2.25" /></svg>}
            title="Articulated Motion"
            description="30 degrees of freedom for natural, fluid movement patterns."
          />
          <FeatureIcon
            icon={<svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path d="M8.288 15.038a5.25 5.25 0 017.424 0M5.106 11.856c3.807-3.808 9.98-3.808 13.788 0M1.924 8.674c5.565-5.565 14.587-5.565 20.152 0M12.53 18.22l-.53.53-.53-.53a.75.75 0 011.06 0z" /></svg>}
            title="Always Connected"
            description="Seamless connectivity keeps Animatus in sync with your digital life."
          />
        </div>
      </section>

      {/* ===== AUTOMATE YOUR ENVIRONMENT ===== */}
      <section className="px-6 md:px-16 lg:px-24 py-12 md:py-16 text-center">
        <div className="max-w-[1100px] mx-auto flex flex-col items-center">
          <SectionHeading
            title="Automate Your Environment"
            description="Give Animatus a set of directives, schedule a time, and come back to a perfectly maintained space every day."
          />
          <div className="w-full"><VideoBlock src="/video-2-short.mp4" fullSrc="/video-2.mp4" label="Watch Video" /></div>
        </div>
      </section>

      {/* ===== LEARN AND ADAPT ===== */}
      <section className="px-6 md:px-16 lg:px-24 py-12 md:py-16 text-center">
        <div className="max-w-[1100px] mx-auto flex flex-col items-center">
          <SectionHeading
            title="Learn and Adapt"
            description="Ask Animatus questions and get instant access to knowledge, powered by intelligent reasoning."
          />
          <div className="w-full"><VideoBlock src="/video-1.mp4" label="Watch Video" /></div>

          <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-10 mt-20">
            <FeatureIcon
              icon={<svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path d="M12 18v-5.25m0 0a6.01 6.01 0 001.5-.189m-1.5.189a6.01 6.01 0 01-1.5-.189m3.75 7.478a12.06 12.06 0 01-4.5 0m3.75 2.383a14.406 14.406 0 01-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 10-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" /></svg>}
              title="Smart Reasoning"
              description="Processes complex queries with contextual understanding."
            />
            <FeatureIcon
              icon={<svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.076-4.076a1.526 1.526 0 011.037-.443 48.282 48.282 0 005.68-.494c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" /></svg>}
              title="Conversational"
              description="Natural dialogue with memory, personality, and emotional awareness."
            />
            <FeatureIcon
              icon={<svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path d="M4.26 10.147a60.436 60.436 0 00-.491 6.347A48.627 48.627 0 0112 20.904a48.627 48.627 0 018.232-4.41 60.46 60.46 0 00-.491-6.347m-15.482 0a50.57 50.57 0 00-2.658-.813A59.905 59.905 0 0112 3.493a59.902 59.902 0 0110.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.697 50.697 0 0112 13.489a50.702 50.702 0 017.74-3.342" /></svg>}
              title="Ever-learning"
              description="Continuously improves through interaction and environmental feedback."
            />
          </div>
        </div>
      </section>

      {/* ===== GROWS WITH YOU ===== */}
      <section className="px-6 md:px-16 lg:px-24 pt-12 md:pt-16 pb-0 text-center">
        <div className="max-w-[1100px] mx-auto flex flex-col items-center">
          <SectionHeading
            title="Grows With You"
            description="Animatus is built for full autonomy. It offers incremental upgrades and over-the-air updates, ensuring it evolves alongside your needs."
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

      {/* ===== FOOTER ===== */}
      <footer className="bg-white/[0.03] px-6 md:px-16 lg:px-24 pt-14 pb-10">
        <div className="max-w-[1100px] mx-auto">
          <div className="flex flex-col md:flex-row justify-between gap-10 md:gap-6">
            {/* Left — logo + company info */}
            <div className="flex flex-col gap-5">
              <img src="/alkemist-logo.svg" alt="Alkemist" className="h-5 w-auto self-start" draggable={false} />
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
