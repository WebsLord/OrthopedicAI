import React, { useEffect } from 'react';
import { StyleSheet, Text, View, ActivityIndicator } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { useTranslation } from 'react-i18next';

// Config imports
// Yapılandırma içe aktarımları
import './src/locales/i18n'; 
import { useAuthStore } from './src/store/authStore';

export default function App() {
  const { t } = useTranslation();
  
  // Get actions and state from store
  // Store'dan eylemleri ve durumu al
  const loadUser = useAuthStore((state) => state.loadUser);
  const isLoading = useAuthStore((state) => state.isLoading);

  useEffect(() => {
    // Check for stored token on app launch
    // Uygulama başlatıldığında saklanan tokenı kontrol et
    loadUser();
  }, []);

  // Show loading spinner while checking auth state
  // Kimlik doğrulama durumu kontrol edilirken yükleme çarkını göster
  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2563EB" />
      </View>
    );
  }

  return (
    <SafeAreaProvider>
      <View style={styles.container}>
        {/* Temporary text to test i18n - Navigation will replace this */}
        {/* i18n testi için geçici metin - Navigasyon bunun yerini alacak */}
        <Text style={styles.text}>{t('home.welcome')}</Text>
        <StatusBar style="auto" />
      </View>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  text: {
    fontSize: 20,
    fontWeight: 'bold',
  }
});