/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                dosa: {
                    heat: '#FF6B35',
                    warm: '#F7931E',
                    glow: '#FDB750',
                    green: '#22C55E', // Brand green
                    white: '#FFFFFF',  // Brand white
                    orange: '#FF6B35', // Brand orange (same as heat)
                },
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
                display: ['Outfit', 'Inter', 'sans-serif'],
            },
            animation: {
                'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'shine': 'shine 1.5s linear infinite',
                'gradient-sweep': 'gradient-sweep 2s ease-in-out infinite',
                'button-glow': 'button-glow 2s ease-in-out infinite',
                'press-scale': 'press-scale 0.15s ease-out',
            },
            keyframes: {
                shine: {
                    '0%': { transform: 'translateX(-100%)' },
                    '100%': { transform: 'translateX(100%)' },
                },
                'gradient-sweep': {
                    '0%': { 
                        backgroundPosition: '0% 50%',
                        boxShadow: '0 0 20px rgba(34, 197, 94, 0.4)'
                    },
                    '25%': { 
                        backgroundPosition: '50% 0%',
                        boxShadow: '0 0 30px rgba(255, 255, 255, 0.6)'
                    },
                    '50%': { 
                        backgroundPosition: '100% 50%',
                        boxShadow: '0 0 40px rgba(255, 107, 53, 0.8)'
                    },
                    '75%': { 
                        backgroundPosition: '50% 100%',
                        boxShadow: '0 0 30px rgba(255, 255, 255, 0.6)'
                    },
                    '100%': { 
                        backgroundPosition: '0% 50%',
                        boxShadow: '0 0 20px rgba(34, 197, 94, 0.4)'
                    },
                },
                'button-glow': {
                    '0%, 100%': { 
                        boxShadow: '0 0 20px rgba(34, 197, 94, 0.4), 0 4px 12px rgba(0, 0, 0, 0.15)'
                    },
                    '50%': { 
                        boxShadow: '0 0 40px rgba(255, 107, 53, 0.6), 0 8px 24px rgba(0, 0, 0, 0.2)'
                    },
                },
                'press-scale': {
                    '0%': { transform: 'scale(1)' },
                    '50%': { transform: 'scale(0.95)' },
                    '100%': { transform: 'scale(1)' },
                },
            }
        },
    },
    plugins: [
        function ({ addUtilities }) {
            addUtilities({
                '.perspective-1000': {
                    'perspective': '1000px',
                },
                '.preserve-3d': {
                    'transform-style': 'preserve-3d',
                },
            })
        },
    ],
}
