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

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <h2 className="text-xl font-bold mb-4">画像アップロード</h2>
      <input type="file" accept="image/*" onChange={handleFileChange} ref={fileInputRef} hidden />
      <button className="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition" onClick={() => fileInputRef.current.click()}>
        画像を選択
      </button>

      {uploadedImage && (
        <div className="mt-4">
          <img src={uploadedImage} alt="Uploaded preview" className="w-48 h-auto rounded-lg shadow" />
          <button className="mt-4 bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition" onClick={() => navigate("/questions", { state: { file: selectedFile, imageUrl: uploadedImage } })}>
            次へ
          </button>
        </div>
      )}
    </div>
  );
}

export default UploadPage;
