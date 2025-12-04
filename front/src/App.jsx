// こちらは
// http://localhost:3000/
// JavaScript (React)

import React, { useState } from "react";
import axios from "axios";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import Hero from "./components/Hero";
import UploadSection from "./components/UploadSection";
import AnalysisView from "./components/AnalysisView";
import ResultPage from "./components/ResultPage";

function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const navigate = useNavigate();
  const url = "http://127.0.0.1:8000";  // APIエンドポイント

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const analyze = () => {
    if (!selectedFile) {
      alert("画像を選択してください");
      return;
    }

    setIsAnalyzing(true);

    const formData = new FormData();
    formData.append("image", selectedFile);
    formData.append("api_key", "your_api_key");
    formData.append("location", "Tokyo");

    axios
      .post(`${url}/analyze`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) => {
        // Wait a bit to show the cool animation
        setTimeout(() => {
          setIsAnalyzing(false);
          navigate('/result', { state: { candidates: res.data } });
        }, 2000);
      })
      .catch((err) => {
        console.error(err);
        setIsAnalyzing(false);
        alert("An error occurred during analysis.");
      });
  };

  return (
    <div className="container">
      <Hero />

      {!isAnalyzing ? (
        <>
          <UploadSection
            onFileChange={handleFileChange}
            selectedFile={selectedFile}
          />

          <div style={{ marginBottom: '40px' }}>
            <button
              className="cyber-btn"
              onClick={analyze}
              disabled={!selectedFile}
              style={{ opacity: !selectedFile ? 0.5 : 1 }}
            >
              INITIATE CONNECTION
            </button>
          </div>
        </>
      ) : (
        <AnalysisView isAnalyzing={true} />
      )}

      <footer style={{ marginTop: '100px', padding: '20px', borderTop: '1px solid #333', color: '#666', fontSize: '0.8rem' }}>
        <p>FACE EARTH PROJECT // 2024</p>
        <p style={{ marginTop: '10px', fontStyle: 'italic' }}>
          "What connects us to the land? Is it time? Is it memory? Or is it a hidden resemblance?"
        </p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/result" element={<ResultPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
