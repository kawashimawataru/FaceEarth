import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";

function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedImage, setUploadedImage] = useState(null);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      setSelectedFile(file);
      setUploadedImage(URL.createObjectURL(file));
    }
  };

  const handleSelectFile = () => {
    fileInputRef.current.click();
  };

  const handleNext = () => {
    if (!selectedFile) {
      alert("画像をアップロードしてください！");
      return;
    }
    navigate("/questions", { state: { file: selectedFile, imageUrl: uploadedImage } });
  };

  return (
    <div className="flex flex-col md:flex-row items-center justify-center h-screen bg-gray-100 p-4 space-y-6 md:space-y-0 md:space-x-8">
      {/* 左側 */}
      <div className="flex flex-col items-center space-y-4">
        <h2 className="text-2xl font-bold">画像アップロード</h2>
        <button
          className="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition"
          onClick={handleSelectFile}
        >
          画像を選択
        </button>
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          ref={fileInputRef}
          hidden
        />

        {uploadedImage && (
          <button
            className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition"
            onClick={handleNext}
          >
            次へ
          </button>
        )}
      </div>

      {/* 右側: プレビュー */}
      <div className="max-w-xs">
        {uploadedImage && (
          <img
            src={uploadedImage}
            alt="Uploaded preview"
            className="w-full h-auto rounded-lg shadow"
          />
        )}
      </div>
    </div>
  );
}

export default UploadPage;
