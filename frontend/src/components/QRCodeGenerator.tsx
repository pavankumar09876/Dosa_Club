import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import QRCode from 'react-qr-code';

interface QRCodeGeneratorProps {
    sessionId?: string;
    size?: number;
}

/**
 * QR Code Generator Component
 * Generates and displays a QR code for mobile questionnaire access
 */
export const QRCodeGenerator: React.FC<QRCodeGeneratorProps> = ({
    sessionId = 'default-session',
    size = 160
}) => {
    const [mobileUrl, setMobileUrl] = useState<string>('');
    const [isGenerating, setIsGenerating] = useState(false);
    const [scanCount, setScanCount] = useState(0);

    useEffect(() => {
        generateQRCode();
    }, [sessionId]);

    const generateQRCode = () => {
        setIsGenerating(true);

        // Generate mobile URL for questionnaire
        const url = `${window.location.origin}/mobile/quiz?session=${sessionId}`;
        setMobileUrl(url);

        // Simulate QR generation time
        setTimeout(() => {
            setIsGenerating(false);
        }, 1000);
    };

    const handleRefreshQR = () => {
        setScanCount(prev => prev + 1);
        generateQRCode();
    };

    const copyMobileLink = () => {
        navigator.clipboard.writeText(mobileUrl);
    };

    return (
        <div className="bg-gradient-to-br from-zinc-900/90 to-zinc-800/90 backdrop-blur-xl border border-zinc-700/50 rounded-2xl p-6 shadow-2xl max-w-xs mx-auto">
            {/* Header */}
            <div className="text-center mb-6">
                <div className="inline-flex items-center gap-2 bg-gradient-to-r from-emerald-500/20 to-teal-500/20 backdrop-blur-sm border border-emerald-500/30 rounded-full px-4 py-2 mb-3">
                    <span className="text-lg">📱</span>
                    <span className="text-emerald-400 font-semibold text-sm">Mobile Access</span>
                </div>
                <h3 className="text-lg font-bold text-white mb-1">Scan to Continue</h3>
                <p className="text-zinc-400 text-xs">Quick mobile questionnaire</p>
            </div>

            {/* QR Code Container */}
            <div className="relative mb-6">
                {/* Animated Glow Effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-teal-500/20 rounded-xl blur-xl animate-pulse" />

                <div className="relative bg-white rounded-xl p-4 shadow-lg">
                    {isGenerating ? (
                        <div className="w-40 h-40 flex items-center justify-center">
                            <motion.div
                                animate={{ rotate: 360 }}
                                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                                className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full"
                            />
                        </div>
                    ) : (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.3 }}
                            className="w-40 h-40 mx-auto flex items-center justify-center"
                        >
                            <QRCode
                                value={mobileUrl}
                                size={size}
                                level="H"
                                bgColor="#ffffff"
                                fgColor="#000000"
                            />
                        </motion.div>
                    )}
                </div>

                {/* Corner Brackets */}
                <div className="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-emerald-400 rounded-tl-lg" />
                <div className="absolute top-0 right-0 w-4 h-4 border-t-2 border-r-2 border-emerald-400 rounded-tr-lg" />
                <div className="absolute bottom-0 left-0 w-4 h-4 border-b-2 border-l-2 border-emerald-400 rounded-bl-lg" />
                <div className="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-emerald-400 rounded-br-lg" />

                {/* Scanning Line Animation */}
                <motion.div
                    initial={{ y: -80 }}
                    animate={{ y: 80 }}
                    transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                    className="absolute inset-x-4 top-0 h-0.5 bg-gradient-to-r from-transparent via-emerald-400 to-transparent opacity-70"
                />
            </div>

            {/* Quick Instructions */}
            <div className="space-y-3 mb-4">
                <div className="flex items-center justify-center gap-4 text-xs text-zinc-300">
                    <div className="flex items-center gap-1">
                        <span className="text-emerald-400">📷</span>
                        <span>Point camera</span>
                    </div>
                    <div className="flex items-center gap-1">
                        <span className="text-emerald-400">👆</span>
                        <span>Tap link</span>
                    </div>
                    <div className="flex items-center gap-1">
                        <span className="text-emerald-400">✓</span>
                        <span>Start quiz</span>
                    </div>
                </div>

                <div className="flex items-center justify-center gap-2 text-xs text-zinc-500">
                    <span className="flex items-center gap-1">
                        <span className="text-emerald-400">✓</span>
                        <span>iOS & Android</span>
                    </span>
                    <span className="text-zinc-600">•</span>
                    <span className="flex items-center gap-1">
                        <span className="text-emerald-400">✓</span>
                        <span>No app required</span>
                    </span>
                </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-2">
                <button
                    onClick={handleRefreshQR}
                    className="flex-1 bg-zinc-800/50 hover:bg-zinc-700/50 text-zinc-300 hover:text-white border border-zinc-700/50 hover:border-zinc-600/50 rounded-lg px-3 py-2 text-xs font-medium transition-all duration-200"
                >
                    🔄 Refresh
                </button>
                <button
                    onClick={copyMobileLink}
                    className="flex-1 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white rounded-lg px-3 py-2 text-xs font-medium transition-all duration-200 shadow-lg hover:shadow-emerald-500/25"
                >
                    📋 Copy Link
                </button>
            </div>

            {/* Scan Counter */}
            {scanCount > 0 && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-center mt-3 text-zinc-500 text-xs"
                >
                    Refreshed {scanCount} time{scanCount !== 1 ? 's' : ''}
                </motion.div>
            )}
        </div>
    );
};
