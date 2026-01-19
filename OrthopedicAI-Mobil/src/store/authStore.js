// OrthopedicAI-Mobil/src/store/authStore.js

import { create } from 'zustand';
import * as SecureStore from 'expo-secure-store';
import axios from 'axios'; // We will replace this with our service instance later if needed
// İleride gerekirse bunu kendi servis örneğimizle değiştireceğiz

// Key for SecureStore
// SecureStore için anahtar
const TOKEN_KEY = 'orthopedic_ai_token';

export const useAuthStore = create((set, get) => ({
  user: null,
  token: null,
  isLoading: true, // App starts in loading state checking for token
  // Uygulama, token kontrolü yaparken yükleniyor durumunda başlar

  // Action: Login (Save token and user)
  // Eylem: Giriş Yap (Token ve kullanıcıyı kaydet)
  login: async (token, userData) => {
    try {
      // Save to secure storage
      // Güvenli depolamaya kaydet
      await SecureStore.setItemAsync(TOKEN_KEY, token);
      
      set({ 
        token, 
        user: userData, 
        isLoading: false 
      });
    } catch (error) {
      console.error('Login storage error:', error);
    }
  },

  // Action: Logout (Clear token)
  // Eylem: Çıkış Yap (Tokenı temizle)
  logout: async () => {
    try {
      await SecureStore.deleteItemAsync(TOKEN_KEY);
      set({ 
        token: null, 
        user: null, 
        isLoading: false 
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
  },

  // Action: Check initial auth state on app load
  // Eylem: Uygulama yüklenirken başlangıç kimlik doğrulama durumunu kontrol et
  loadUser: async () => {
    try {
      const storedToken = await SecureStore.getItemAsync(TOKEN_KEY);
      
      if (storedToken) {
        // Here we ideally validate the token with backend or decode it
        // Burada ideal olarak tokenı backend ile doğrularız veya çözeriz
        set({ token: storedToken, isLoading: false });
      } else {
        set({ token: null, isLoading: false });
      }
    } catch (error) {
      console.error('Load user error:', error);
      set({ token: null, isLoading: false });
    }
  }
}));