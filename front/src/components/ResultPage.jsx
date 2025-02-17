import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";

function ResultPage() {
  const location = useLocation();
  const [imageSrc, setImageSrc] = useState(null);
  const [loading, setLoading] = useState(true);
  const file = location.state?.file;

  useEffect(() => {
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    axios.post("http://127.0.0.1:8000/matched_image", formData, { responseType: "blob" })
      .then((response) => {
        setImageSrc(URL.createObjectURL(response.data));
        setLoading(false);
      })
      .catch((err) => console.error(err));
  }, [file]);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <h2 className="text-lg font-bold mb-4">解析結果</h2>
      {loading ? <div className="animate-spin border-t-4 border-blue-500 border-solid rounded-full w-12 h-12"></div> : <img src={imageSrc} alt="Result" className="w-64 h-auto rounded-lg shadow" />}
    </div>
  );
}

export default ResultPage;
