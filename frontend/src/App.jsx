import ClerkProviderWithRoutes from "./auth/ClerkProviderWithRoutes.jsx"
import {Routes, Route} from "react-router-dom"
import {Layout} from "./layout/Layout.jsx"
import {ChallengeGenerator} from "./challenges/ChallengeGenerator.jsx";
import {HistoryPanel} from "./history/HistoryPanel.jsx";
import {AuthPage} from "./auth/AuthPage.jsx";
import './App.css'

function App() {
    return <ClerkProviderWithRoutes>
        <Routes>
            <Route path="/sign-in/*" element={<AuthPage />} />
            <Route path="/sign-up" element={<AuthPage />} />
            <Route element={<Layout />}>
                <Route path="/" element={<ChallengeGenerator />}/>
                <Route path="/history" element={<HistoryPanel />}/>
            </Route>
        </Routes>
    </ClerkProviderWithRoutes>
}

export default App