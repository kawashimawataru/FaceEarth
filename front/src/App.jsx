// こちらは
// http://localhost:3000/
// JavaScript (React)

import React, { useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const url = "http://127.0.0.1:8000";  // APIエンドポイント

  // ファイルが選択されたときに状態を更新
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // 画像をフォームデータとして送信
  const analyze = () => {
    if (!selectedFile) {
      alert("画像を選択してください");
      return;
    }
    // FormDataを使ってmultipart/form-data形式で送る
    const formData = new FormData();
    formData.append("image", selectedFile);     // ← ここでファイルを追加
    formData.append("api_key", "your_api_key");
    formData.append("location", "Tokyo");

    axios
      .post(`${url}/analyze`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) => {
        setData(res.data);
      })
      .catch((err) => console.error(err));
  };

  return (
    <div>
      <div>画像アップロードして解析を実行します</div>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={analyze}>解析</button>
      {data && (
        <div>
          <div>Similarity: {data.similarity}</div>
          <div>Latitude: {data.latitude}</div>
          <div>Longitude: {data.longitude}</div>
        </div>
      )}
    </div>
  );
}

export default App;
