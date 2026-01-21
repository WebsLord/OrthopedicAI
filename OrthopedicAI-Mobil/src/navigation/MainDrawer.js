import React from 'react';
import { createDrawerNavigator } from '@react-navigation/drawer';
import HomeScreen from '../features/analysis/HomeScreen';
import { useTranslation } from 'react-i18next';

const Drawer = createDrawerNavigator();

export default function MainDrawer() {
  const { t } = useTranslation();

  return (
    <Drawer.Navigator 
      screenOptions={{ 
        headerShown: true,
        drawerType: 'slide', // İstediğin "Kayarak açılma" efekti
        overlayColor: 'rgba(0,0,0,0.5)', // Arka plan karartma
      }}
    >
      <Drawer.Screen 
        name="Home" 
        component={HomeScreen} 
        options={{ title: t('home.welcome') || 'Home' }} 
      />
      {/* İleride History, Settings gibi ekranları buraya ekleyeceğiz */}
    </Drawer.Navigator>
  );
}