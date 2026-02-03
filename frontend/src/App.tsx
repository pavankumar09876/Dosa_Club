import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import { ConfigProvider, theme, App as AntApp } from 'antd';
import { UserProvider } from './context/UserContext';
import { antdTheme } from './theme/antd-theme';
import { AmbientBackground } from './components/AmbientBackground';
import { Hero } from './components/Hero';
import { UserEntryScreen } from './features/UserEntry/UserEntryScreen';
import { QuestionnaireScreen } from './features/Questionnaire/QuestionnaireScreen';
import { ProcessingScreen } from './features/Processing/ProcessingScreen';
import { RecommendationScreen } from './features/Recommendation/RecommendationScreen';
import { MenuExplorerScreen } from './features/MenuExplorer/MenuExplorerScreen';
import { ModeSelectionScreen } from './features/ModeSelection/ModeSelectionScreen';
import { AdminDashboardScreen } from './features/Admin/AdminDashboardScreen';
import { GuestQuestionnaireScreen } from './features/Guest/GuestQuestionnaireScreen';
import { GuestRecommendationScreen } from './features/Guest/GuestRecommendationScreen';

import { MobileQuestionnaireScreen } from './features/Mobile/MobileQuestionnaireScreen';
import { MobileRecommendationScreen } from './features/Mobile/MobileRecommendationScreen';

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Hero />} />
        <Route path="/mode-selection" element={<ModeSelectionScreen />} />
        <Route path="/start" element={<UserEntryScreen />} />
        <Route path="/questions" element={<QuestionnaireScreen />} />
        <Route path="/processing" element={<ProcessingScreen />} />
        <Route path="/recommendation" element={<RecommendationScreen />} />
        <Route path="/explore" element={<MenuExplorerScreen />} />
        <Route path="/admin" element={<AdminDashboardScreen />} />

        <Route path="/guest/questions" element={<GuestQuestionnaireScreen />} />
        <Route path="/guest/recommendation" element={<GuestRecommendationScreen />} />

        {/* Mobile Routes */}
        <Route path="/mobile/quiz" element={<MobileQuestionnaireScreen />} />
        <Route path="/mobile/recommendation" element={<MobileRecommendationScreen />} />
      </Routes>
    </AnimatePresence>
  );
}

function App() {
  return (
    <ConfigProvider
      theme={{
        ...antdTheme,
        algorithm: theme.darkAlgorithm,
      }}
    >
      <AntApp>
        <UserProvider>
          <BrowserRouter>
            <div className="relative min-h-screen bg-black text-white">
              {/* Ambient background (always present) */}
              <AmbientBackground />

              {/* Animated routes */}
              <AnimatedRoutes />
            </div>
          </BrowserRouter>
        </UserProvider>
      </AntApp>
    </ConfigProvider>
  );
}

export default App;
