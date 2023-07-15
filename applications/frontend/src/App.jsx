import React from "react";
import { BrowserRouter, Routes, Route} from "react-router-dom";
import { ModeSelection } from "./pages/ModeSelection";
import { Result } from "./pages/Result";
import { Solve } from "./pages/Solve";
import { StartPage } from "./pages/StartPage";
import { WordLevel } from "./pages/WordLevel";
import { NoMatch } from "./pages/NoMatch";

import './App.css';

function App() {
  return (
    // <AppProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<StartPage />} />
          <Route path="/mode" element={<ModeSelection />} />
          <Route path="/wordlevel" element={<WordLevel />} />
          <Route path="/solve" element={<Solve />} />
          <Route path="/result" element={<Result />} />
          <Route path="*" element={<NoMatch />} />
        </Routes>
      </BrowserRouter>
    // </AppProvider>
  );
}

export default App;