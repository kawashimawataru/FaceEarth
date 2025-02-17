import React from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold mb-6">画像解析アプリ</h1>
      <p className="mb-10 text-gray-700 text-center">
        画像をアップロードして質問に回答すると、最後に解析結果が表示されます。
      </p>
      <button
        className="bg-blue-500 text-white px-8 py-4 rounded-lg shadow-lg hover:bg-blue-600 transition text-lg"
        onClick={() => navigate("/upload")}
      >
        はじめる
      </button>
    </div>
  );
}

export default Home;
