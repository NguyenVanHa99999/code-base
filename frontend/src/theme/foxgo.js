import { definePreset } from '@primeuix/themes'
import Aura from '@primeuix/themes/aura'

export const FoxgoTheme = definePreset(Aura, {
    semantic: {
        primary: {
            50: '#FFF8ED',
            100: '#FFEED5',
            200: '#FFDCAA',
            300: '#FFCB80',
            400: '#FFB955',
            500: '#FFA82B',
            600: '#FF9600',
            700: '#D98000',
            800: '#B36900',
            900: '#8C5300',
            1000: '#663C00'
        },
        warning: {
            50: '#FFFBED',
            100: '#FFF6D5',
            200: '#FFEDAA',
            300: '#FFE380',
            400: '#FFDA55',
            500: '#FFD12B',
            600: '#FFC800',
            700: '#D9AA00',
            800: '#B38C00',
            900: '#8C6E00',
            1000: '#665000'
        },
        success: {
            50: '#F7FEEF',
            100: '#EBFBD8',
            200: '#D8F6B1',
            300: '#C4F28A',
            400: '#B1EE64',
            500: '#9DEA3D',
            600: '#89E219',
            700: '#74C015',
            800: '#609E12',
            900: '#4B7C0E',
            1000: '#375B0A'
        },
        danger: {
            50: '#FFF0F0',
            100: '#FFD2D2',
            200: '#FFA5A5',
            300: '#FF7878',
            400: '#FF4B4B',
            500: '#FF2525',
            600: '#FE0000',
            700: '#D80000',
            800: '#B20000',
            900: '#8C0000',
            1000: '#660000'
        },
        info: {
            50: '#EFF8FF',
            100: '#D2EFFD',
            200: '#A4DFFB',
            300: '#77D0FA',
            400: '#49C0F8',
            500: '#1CB0F6',
            600: '#099FE5',
            700: '#0887C3',
            800: '#066FA1',
            900: '#05587F',
            1000: '#04405D'
        },
        neutral: {
            50: '#FAFAFA',
            100: '#F5F5F5',
            200: '#E6E6E6',
            300: '#CCCCCC',
            400: '#B3B3B3',
            500: '#8C8C8C',
            600: '#6E6E6E',
            700: '#5E5E5E',
            800: '#474747',
            900: '#333333',
            1000: '#262626'
        }
    },
    components: {
        inputtext: {
            root: {
                borderRadius: '12px'
            }
        }
    },
});
