// こちらは
// http://localhost:3000/
// JavaScript (React)

import React, { useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [imageSrc, setImageSrc] = useState(null);
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

  // 画像を /matched_image に送信して、処理された画像を受け取る
  const uploadAndFetchImage = () => {
    if (!selectedFile) {
      alert("画像を選択してください");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    axios
      .post(`${url}/matched_image`, formData, {
        responseType: "blob", // 画像データをそのまま取得する
      })
      .then((response) => {
        // 受け取ったBlobデータをURL化して表示
        const imageUrl = URL.createObjectURL(response.data);
        setImageSrc(imageUrl);
      })
      .catch((err) => console.error(err));
  };

  return (
    <div>
      <div>画像アップロードして解析を実行します</div>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <div>
        <button onClick={analyze}>解析</button>
        <button onClick={uploadAndFetchImage}>画像送信して結果を表示</button>
      </div>
      {data && (
        <div>
          <div>Similarity: {data.similarity}</div>
          <div>Latitude: {data.latitude}</div>
          <div>Longitude: {data.longitude}</div>
        </div>
      )}
      {imageSrc && (
        <div>
          <div>結果画像:</div>
          <img src={imageSrc} alt="Result" style={{ maxWidth: "100%" }} />
        </div>
      )}
    </div>
  );
}

export default App;
