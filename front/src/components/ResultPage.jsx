import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";

function ResultPage() {
  const location = useLocation();
  const [imageSrc, setImageSrc] = useState(null);
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(0); // 0% -> 100% に疑似的に進行
  const file = location.state?.file; // 解析対象

  useEffect(() => {
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    // 疑似的な進捗を実装: 5秒で100%まで
    const timer = setInterval(() => {
      setProgress((prev) => (prev < 100 ? prev + 1 : 100));
    }, 50);

    axios
      .post("http://127.0.0.1:8000/matched_image", formData, {
        responseType: "blob",
      })
      .then((response) => {
        const imgUrl = URL.createObjectURL(response.data);
        // 画像が取得できたら100%にし、ロード完了
        setProgress(100);
        setImageSrc(imgUrl);
      })
      .catch((err) => console.error(err))
      .finally(() => {
        setTimeout(() => {
          setLoading(false);
          clearInterval(timer);
        }, 500);
      });

    return () => clearInterval(timer);
  }, [file]);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100 p-4">
      <h2 className="text-2xl font-bold mb-4">解析結果</h2>

      {loading ? (
        <div className="flex flex-col items-center">
          {/* ローディングスピナー */}
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500 mb-4"></div>
          {/* 進捗バー */}
          <div className="w-64 bg-gray-300 rounded-full h-4 mb-2">
            <div
              className="bg-blue-500 h-4 rounded-full"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <p className="text-gray-700">{progress}%</p>
        </div>
      ) : (
        <div className="flex flex-col items-center">
          {imageSrc && (
            <img
              src={imageSrc}
              alt="Result"
              className="w-64 h-auto rounded-lg shadow"
            />
          )}
          <p className="mt-4 text-green-600 font-semibold">解析が完了しました！</p>
        </div>
      )}
    </div>
  );
}

export default ResultPage;
