import Clerk from "./auth/Clerk";
import { Routes, Route } from "react-router-dom";
import AuthenticationPage from "./auth/AuthenticationPage";
import Layout from "./layout/Layout";
import ChallengeGenerator from "./challenge/ChallengeGenerator";
import HistoryPanel from "./history/HistoryPanel";
import "./App.css";

function App() {
  return (
    <>
      <Clerk>
        <Routes>
          <Route path="/sign-in/*" element={<AuthenticationPage />} />
          <Route path="/sign-up" element={<AuthenticationPage />} />
          <Route element={<Layout />}>
            <Route path="/" element={<ChallengeGenerator />} />
            <Route path="/history" element={<HistoryPanel />} />
          </Route>
        </Routes>
      </Clerk>
    </>
  );
}

export default App;
