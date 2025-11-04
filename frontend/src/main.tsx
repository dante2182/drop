import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './style/global.css'
import { ThemeProvider } from '@/components/theme-provider'
import Footer from './components/layout/footer'
import Header from './components/layout/header'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <Header />
      <App />
      <Footer />
    </ThemeProvider>
  </StrictMode>
)
