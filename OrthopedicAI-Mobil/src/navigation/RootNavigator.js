import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { useAuthStore } from '../store/authStore';
import AuthStack from './AuthStack';
import MainDrawer from './MainDrawer';

export default function RootNavigator() {
  // Store'dan kullanıcı durumunu dinle
  const token = useAuthStore((state) => state.token);

  return (
    <NavigationContainer>
      {token ? <MainDrawer /> : <AuthStack />}
    </NavigationContainer>
  );
}