import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { useAuthStore } from '../../store/authStore';

export default function HomeScreen() {
  const logout = useAuthStore(state => state.logout);

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Ana Ekran (Home)</Text>
      <Text>Burada Resim Yükleme Olacak</Text>
      <Button title="Çıkış Yap (Logout)" onPress={logout} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  text: { marginBottom: 20, fontSize: 18, fontWeight: 'bold' }
});