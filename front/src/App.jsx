import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./components/Home";
import UploadPage from "./components/UploadPage";
import QuestionPage from "./components/QuestionPage";
import ResultPage1 from "./components/ResultPage1";
import ResultPage2 from "./components/ResultPage2";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/questions" element={<QuestionPage />} />
        <Route path="/result1" element={<ResultPage1 />} />
        <Route path="/result2" element={<ResultPage2 />} />
      </Routes>
    </Router>
  );
}

export default App;
