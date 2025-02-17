import React from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <h1 className="text-2xl font-bold mb-6">画像解析アプリ</h1>
      <button
        className="bg-blue-500 text-white px-6 py-3 rounded-lg shadow-lg hover:bg-blue-700 transition"
        onClick={() => navigate("/upload")}
      >
        開始する
      </button>
    </div>
  );
}

export default Home;
