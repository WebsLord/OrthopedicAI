import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { useAuthStore } from '../../store/authStore';

export default function LoginScreen({ navigation }) {
  // Test için geçici giriş fonksiyonu
  const login = useAuthStore(state => state.login);

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Login Screen</Text>
      <Button title="Giriş Yap (Test)" onPress={() => login('fake-token', { name: 'Efe' })} />
      <Button title="Kayıt Ol'a Git" onPress={() => navigation.navigate('Register')} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  text: { marginBottom: 20, fontSize: 18 }
});