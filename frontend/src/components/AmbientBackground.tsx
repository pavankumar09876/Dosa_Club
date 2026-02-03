import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';

/**
 * Ambient Background Component
 * Uses GSAP for slow, continuous motion that adds depth without distraction
 */
export const AmbientBackground = () => {
    const containerRef = useRef<HTMLDivElement>(null);
    const orb1Ref = useRef<HTMLDivElement>(null);
    const orb2Ref = useRef<HTMLDivElement>(null);
    const orb3Ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!containerRef.current) return;

        const ctx = gsap.context(() => {
            // Subtle gradient orb animations
            // Very slow, continuous, barely noticeable but adds premium depth
            gsap.to(orb1Ref.current, {
                x: 100,
                y: 50,
                scale: 1.2,
                duration: 20,
                ease: 'sine.inOut',
                repeat: -1,
                yoyo: true,
            });

            gsap.to(orb2Ref.current, {
                x: -80,
                y: 80,
                scale: 1.1,
                duration: 25,
                ease: 'sine.inOut',
                repeat: -1,
                yoyo: true,
            });

            gsap.to(orb3Ref.current, {
                x: -50,
                y: -60,
                scale: 0.9,
                duration: 18,
                ease: 'sine.inOut',
                repeat: -1,
                yoyo: true,
            });
        }, containerRef);

        return () => ctx.revert();
    }, []);

    return (
        <div
            ref={containerRef}
            className="fixed inset-0 overflow-hidden pointer-events-none"
            style={{ zIndex: 0 }}
        >
            {/* Dark premium background */}
            <div className="absolute inset-0 bg-gradient-to-br from-black via-zinc-950 to-black" />

            {/* Ambient gradient orbs - GPU accelerated */}
            <div
                ref={orb1Ref}
                className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full gpu-accelerated"
                style={{
                    background: 'radial-gradient(circle, rgba(255, 107, 53, 0.08) 0%, transparent 70%)',
                    filter: 'blur(60px)',
                }}
            />

            <div
                ref={orb2Ref}
                className="absolute top-1/2 right-1/4 w-[500px] h-[500px] rounded-full gpu-accelerated"
                style={{
                    background: 'radial-gradient(circle, rgba(247, 147, 30, 0.06) 0%, transparent 70%)',
                    filter: 'blur(80px)',
                }}
            />

            <div
                ref={orb3Ref}
                className="absolute bottom-1/4 left-1/2 w-80 h-80 rounded-full gpu-accelerated"
                style={{
                    background: 'radial-gradient(circle, rgba(253, 183, 80, 0.05) 0%, transparent 70%)',
                    filter: 'blur(70px)',
                }}
            />

            {/* Subtle grain texture overlay */}
            <div
                className="absolute inset-0 opacity-[0.02]"
                style={{
                    backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
                }}
            />
        </div>
    );
};
