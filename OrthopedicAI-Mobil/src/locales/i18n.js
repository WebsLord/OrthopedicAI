// OrthopedicAI-Mobil/src/locales/i18n.js

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import { getLocales } from 'expo-localization';

import en from './en.json';
import tr from './tr.json';

// Get device language
// Cihaz dilini al
const deviceLanguage = getLocales()[0]?.languageCode;

i18n.use(initReactI18next).init({
  compatibilityJSON: 'v3', // Required for Android
  resources: {
    en: { translation: en },
    tr: { translation: tr },
  },
  // Set language based on device or default to English
  // Dili cihaza göre ayarla veya varsayılan olarak İngilizce yap
  lng: deviceLanguage === 'tr' ? 'tr' : 'en', 
  fallbackLng: 'en',
  
  interpolation: {
    escapeValue: false, // React already safe from XSS
  },
});

export default i18n;