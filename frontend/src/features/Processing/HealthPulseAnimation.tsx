import { motion } from 'framer-motion';

/**
 * Icons for the orbiting satellites
 */
const HeartIcon = () => (
    <svg viewBox="0 0 24 24" fill="currentColor" className="w-full h-full text-rose-500">
        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
    </svg>
);

const AppleIcon = () => (
    <svg viewBox="0 0 24 24" fill="currentColor" className="w-full h-full text-green-500">
        <path d="M7.52646 4.54471C8.36199 4.60623 9.38079 4.14811 9.94042 3.47352C10.5186 2.77976 10.6681 1.83857 9.87321 1.76757C9.17937 1.708 8.01925 2.22637 7.424 2.94086C6.86438 3.61342 6.64333 4.4797 7.52646 4.54471ZM17.1528 17.5029C16.666 18.2124 15.9387 19.4124 14.4939 19.4124C12.9806 19.4124 12.569 18.5283 10.9669 18.5283C9.33614 18.5283 8.79058 19.383 7.40864 19.4124C5.74838 19.4442 4.11663 17.5181 3.20817 16.2081C1.35242 13.5323 1.96803 8.64307 5.77258 8.46849C7.29 8.39864 8.23666 9.47167 9.77353 9.47167C11.3082 9.47167 12.0674 8.33758 13.8866 8.39864C14.7358 8.42777 16.0963 8.72477 17.1517 10.2678C17.0601 10.3259 15.0118 11.536 15.0487 14.2407C15.0868 16.9205 17.6521 17.8931 17.697 17.912C17.6366 18.0682 17.4727 18.7076 17.1528 17.5029Z" />
    </svg>
);

const DnaIcon = () => (
    <svg viewBox="0 0 24 24" fill="currentColor" className="w-full h-full text-blue-500">
        <path d="M12 2C13.1 2 14 2.9 14 4C14 4.74 13.6 5.39 13 5.73V7.17C13.71 7.46 14.36 7.9 14.9 8.44C15.54 9.09 16 9.86 16.29 10.71H19C19.55 10.71 20 11.16 20 11.71C20 12.26 19.55 12.71 19 12.71H16.29C16 13.56 15.54 14.33 14.9 14.97C14.36 15.5 13.71 15.94 13 16.23V18.27C13.6 18.61 14 19.26 14 20C14 21.1 13.1 22 12 22C10.9 22 10 21.1 10 20C10 19.26 10.4 18.61 11 18.27V16.23C10.29 15.94 9.64 15.5 9.1 14.97C8.46 14.33 8 13.56 7.71 12.71H5C4.45 12.71 4 12.26 4 11.71C4 11.16 4.45 10.71 5 10.71H7.71C8 9.86 8.46 9.09 9.1 8.44C9.64 7.9 10.29 7.46 11 7.17V5.73C10.4 5.39 10 4.74 10 4C10 2.9 10.9 2 12 2ZM9.85 13.56C10.42 14.13 11.17 14.5 12 14.5C12.83 14.5 13.58 14.13 14.15 13.56C14.56 13.15 14.84 12.65 14.96 12.11H9.03C9.15 12.65 9.44 13.15 9.85 13.56ZM14.15 10.25C13.58 9.68 12.83 9.31 12 9.31C11.17 9.31 10.42 9.68 9.85 10.25C9.44 10.66 9.15 11.16 9.03 11.71H14.96C14.84 11.16 14.56 10.66 14.15 10.25Z" />
    </svg>
);

const FlameIcon = () => (
    <svg viewBox="0 0 24 24" fill="currentColor" className="w-full h-full text-orange-500">
        <path d="M12 23C7.6 23 4 19.4 4 15C4 12.5 5.5 10.3 7.8 9.3C7.5 10 7.3 10.8 7.3 11.6C7.3 14.4 9.6 16.7 12.4 16.7C12.8 16.7 13.2 16.6 13.6 16.5C13.2 18.5 11.4 20 9.3 20C9 20 8.7 20 8.4 20L8.7 20.3C10.1 21.7 12.2 21.7 13.6 20.3C15 18.9 15 16.8 13.6 15.4C13.1 14.9 12.6 14.5 12 14.1C11.1 13.5 10.3 12.9 9.6 12.2C8.6 11.2 8 9.9 8 8.4C8 5.6 10 3.2 12.7 2.6C12.2 4.4 12.5 6.4 13.7 7.9C14.8 9.3 16.4 10.1 18.1 10.1C18.8 10.1 19.4 10 20 9.8C20 10.2 20 10.6 20 11C20 15.4 16.4 19 12 19V23Z" />
    </svg>
);

const OrbitingSatellite = ({
    icon: Icon,
    angle,
    delay,
    radius = 100
}: {
    icon: React.ElementType,
    angle: number,
    delay: number,
    radius?: number
}) => {
    return (
        <motion.div
            className="absolute top-1/2 left-1/2 w-10 h-10 -ml-5 -mt-5 flex items-center justify-center bg-zinc-900 border border-zinc-700 rounded-full shadow-lg z-20"
            animate={{
                rotate: 360,
            }}
            style={{
                translateX: radius * Math.cos(angle * Math.PI / 180),
                translateY: radius * Math.sin(angle * Math.PI / 180),
                width: 40,
                height: 40,
                originX: `${-radius * Math.cos(angle * Math.PI / 180) + 20}px`,
                originY: `${-radius * Math.sin(angle * Math.PI / 180) + 20}px`,
            }}
            transition={{
                duration: 8,
                repeat: Infinity,
                ease: "linear",
            }}
        >
            {/* Counter-rotate icon to keep it upright */}
            <motion.div
                className="w-5 h-5"
                animate={{ rotate: -360 }}
                transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
            >
                <Icon />
            </motion.div>
        </motion.div>
    );
};

export const HealthPulseAnimation = () => {
    return (
        <div className="relative w-80 h-80 flex items-center justify-center">

            {/* 1. Orbit Paths (Decorative Rings) */}
            <motion.div
                className="absolute inset-4 border border-zinc-800 rounded-full opacity-50"
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            >
                <div className="absolute top-0 left-1/2 w-2 h-2 -ml-1 -mt-1 bg-zinc-700 rounded-full" />
            </motion.div>

            <motion.div
                className="absolute inset-[3rem] border border-amber-900/30 rounded-full"
                animate={{ rotate: -360 }}
                transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
            />

            {/* 2. Central AI Core (Pulsing Brain) */}
            <div className="relative z-10">
                {/* Glow effect */}
                <motion.div
                    className="absolute inset-0 bg-dosa-heat rounded-full blur-xl"
                    animate={{
                        opacity: [0.3, 0.6, 0.3],
                        scale: [0.8, 1.2, 0.8]
                    }}
                    transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: "easeInOut"
                    }}
                />

                {/* Core Object */}
                <motion.div
                    className="w-24 h-24 bg-gradient-to-br from-amber-400 to-orange-600 rounded-full shadow-[0_0_30px_rgba(245,158,11,0.5)] flex items-center justify-center relative overflow-hidden"
                    animate={{
                        scale: [1, 1.05, 1],
                    }}
                    transition={{
                        duration: 1.5,
                        repeat: Infinity,
                        ease: "easeInOut"
                    }}
                >
                    {/* Inner Texture */}
                    <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMSIgY3k9IjEiIHI9IjEiIGZpbGw9InJnYmEoMjU1LDI1NSwyNTUsMC4yKSIvPjwvc3ZnPg==')] opacity-30" />

                    {/* Tech Symbol inside */}
                    <svg viewBox="0 0 24 24" fill="white" className="w-10 h-10 opacity-90">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z" />
                    </svg>
                </motion.div>
            </div>

            {/* 3. Data Streams flowing to center */}
            {[0, 90, 180, 270].map((angle, i) => (
                <motion.div
                    key={`stream-${i}`}
                    className="absolute top-1/2 left-1/2 h-0.5 bg-gradient-to-r from-transparent via-amber-500/50 to-transparent w-32 -ml-16 origin-center"
                    style={{ rotate: angle }}
                >
                    <motion.div
                        className="w-2 h-2 bg-white rounded-full blur-[1px] absolute"
                        initial={{ x: 0, opacity: 0 }}
                        animate={{
                            x: [0, 64], // Move from outside towards center (approx)
                            opacity: [0, 1, 0]
                        }}
                        transition={{
                            duration: 1.5,
                            repeat: Infinity,
                            delay: i * 0.3,
                            ease: "linear"
                        }}
                    />
                </motion.div>
            ))}

            {/* 4. Orbiting Satellites */}
            {/* Note: In a real circular orbit implementation with CSS transforms, 
                we arrange them in a container that rotates. */}
            <motion.div
                className="absolute inset-0 animate-spin-slow"
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            >
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2">
                    <div className="w-10 h-10 bg-zinc-900 border border-rose-500/30 rounded-full flex items-center justify-center shadow-lg shadow-rose-900/20">
                        <div className="w-5 h-5"><HeartIcon /></div>
                    </div>
                </div>
                <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-1/2">
                    <div className="w-10 h-10 bg-zinc-900 border border-green-500/30 rounded-full flex items-center justify-center shadow-lg shadow-green-900/20">
                        <div className="w-5 h-5"><AppleIcon /></div>
                    </div>
                </div>
                <div className="absolute left-0 top-1/2 -translate-x-1/2 -translate-y-1/2">
                    <div className="w-10 h-10 bg-zinc-900 border border-blue-500/30 rounded-full flex items-center justify-center shadow-lg shadow-blue-900/20">
                        <div className="w-5 h-5"><DnaIcon /></div>
                    </div>
                </div>
                <div className="absolute right-0 top-1/2 translate-x-1/2 -translate-y-1/2">
                    <div className="w-10 h-10 bg-zinc-900 border border-orange-500/30 rounded-full flex items-center justify-center shadow-lg shadow-orange-900/20">
                        <div className="w-5 h-5"><FlameIcon /></div>
                    </div>
                </div>
            </motion.div>

            {/* Counter-rotation for icons to keep them upright (Optional refinement: simpler to just let them rotate if icons are simple) */}

            {/* Radar Scan Effect */}
            <motion.div
                className="absolute inset-0 bg-gradient-to-b from-transparent via-amber-500/10 to-transparent z-0"
                style={{ originY: 0.5 }}
                animate={{ rotate: 360 }}
                transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
            />
        </div>
    );
};
