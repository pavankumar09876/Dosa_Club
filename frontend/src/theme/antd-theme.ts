import { ThemeConfig } from 'antd';

export const antdTheme: ThemeConfig = {
    token: {
        colorPrimary: '#FFA500', // Light orange/gold
        colorSuccess: '#FFB347', // Light orange
        colorWarning: '#FF8C00', // Darker orange
        colorError: '#ff4d4f',
        colorInfo: '#FFD700', // Gold

        // Border radius
        borderRadius: 12,
        borderRadiusLG: 16,
        borderRadiusSM: 8,

        // Font
        fontFamily: 'Inter, system-ui, sans-serif',
        fontSize: 16,

        // Dark mode
        colorBgBase: '#000000',
        colorBgContainer: '#0a0a0a',
        colorBgElevated: '#141414',
        colorText: '#ffffff',
        colorTextSecondary: '#a1a1a1',
        colorBorder: '#2a2a2a',
    },
    components: {
        Input: {
            borderRadius: 12,
            controlHeight: 56,
            fontSize: 18,
        },
        Button: {
            borderRadius: 8,
            controlHeight: 40,
            fontSize: 14,
            fontWeight: 500,
            colorPrimary: '#FFA500', // Light orange/gold
            colorPrimaryHover: '#FFB347', // Lighter orange
            colorPrimaryActive: '#FF8C00', // Darker orange
        },
        Select: {
            borderRadius: 12,
            controlHeight: 56,
        },
        Card: {
            borderRadiusLG: 16,
        },
    },
};
