import React, { useState, useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [data, setData] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [imageSrc, setImageSrc] = useState(null);
  const [uploadedImage, setUploadedImage] = useState(null); // ← アップロードした画像用
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);
  const url = "http://127.0.0.1:8000";

  // ファイルが選択されたとき
  const handleFileChange = (event) => {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      setSelectedFile(file);
      setUploadedImage(URL.createObjectURL(file)); // ← プレビュー用URLを作成
    }
  };

  // ドラッグ＆ドロップでファイルを選択
  const handleDrop = (event) => {
    event.preventDefault();
    setDragOver(false);
    if (event.dataTransfer.files.length > 0) {
      const file = event.dataTransfer.files[0];
      setSelectedFile(file);
      setUploadedImage(URL.createObjectURL(file)); // ← プレビュー用URLを作成
    }
  };

  // アップロードエリアをクリックしたら `input` を開く
  const handleClick = () => {
    fileInputRef.current.click();
  };

  // 画像を送信して解析
  const analyze = () => {
    if (!selectedFile) {
      alert("画像を選択してください");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);
    formData.append("api_key", "your_api_key");
    formData.append("location", "Tokyo");

    axios
      .post(`${url}/analyze`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((res) => setData(res.data))
      .catch((err) => console.error(err));
  };

  // 画像を送信して結果画像を取得
  const uploadAndFetchImage = () => {
    if (!selectedFile) {
      alert("画像を選択してください");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    axios
      .post(`${url}/matched_image`, formData, { responseType: "blob" })
      .then((response) => {
        const imageUrl = URL.createObjectURL(response.data);
        setImageSrc(imageUrl);
      })
      .catch((err) => console.error(err));
  };

  return (
    <div className="App">
      <div className="App-container">
        <h2>画像アップロード</h2>

        {/* クリック or ドラッグ&ドロップエリア */}
        <div
          className={`Upload-area ${dragOver ? "dragover" : ""}`}
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={handleClick}
        >
          <p>ここにドラッグ＆ドロップするか、クリックして選択</p>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            ref={fileInputRef}
            hidden
          />
        </div>

        {/* アップロードされた画像とファイル名を表示 */}
        {uploadedImage && (
          <div className="Uploaded-image">
            <p>アップロードした画像: {selectedFile?.name}</p>
            <img src={uploadedImage} alt="Uploaded preview" />
          </div>
        )}

        <div>
          <button onClick={analyze}>解析</button>
          <button onClick={uploadAndFetchImage}>画像送信して結果を表示</button>
        </div>

        {data && (
          <div>
            <h3>解析結果</h3>
            <p>Similarity: {data.similarity}</p>
            <p>Latitude: {data.latitude}</p>
            <p>Longitude: {data.longitude}</p>
          </div>
        )}

        {imageSrc && (
          <div>
            <h3>結果画像:</h3>
            <img src={imageSrc} alt="Result" style={{ maxWidth: "100%" }} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
