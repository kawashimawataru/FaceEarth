import React, { useEffect, useState, useRef } from "react";
import { useLocation } from "react-router-dom";
import Globe from "react-globe.gl";
import axios from "axios";

/**
 * ResultPage1
 *
 * - 前画面 (QuestionPage) から file (ユーザ画像) + rawText(サーバー返却テキスト) を受け取る
 * - 生テキスト(rawText)をまず画面に表示
 * - テキスト中のJSONを抽出→パースした上で整形表示
 * - 3D地球儀(react-globe.gl)を表示
 * - /google_matched_image に手動送信(ボタン)で画像解析
 */

function ResultPage1() {
  const location = useLocation();

  // 受け取ったデータ
  const file = location.state?.file;
  const rawResponseText = location.state?.rawText;

  // 3D地球儀関連
  const globeRef = useRef(null);
  const [markers, setMarkers] = useState([]);

  // (A) 生テキスト
  const [rawTextDisplay, setRawTextDisplay] = useState("");
  // (B) JSONパース結果
  const [parsedJson, setParsedJson] = useState(null);

  // /google_matched_image 送信関連
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [imageSrc, setImageSrc] = useState(null);
  const timerRef = useRef(null);

  // ----------------------------------
  // 1) ページ初期化
  // ----------------------------------
  useEffect(() => {
    if (!rawResponseText) return;

    // (A) テキストそのまま表示
    setRawTextDisplay(rawResponseText);

    // (B) テキスト中のJSONを抽出
    //   最初の '{' ～ 最後の '}' までを substring
    const startIdx = rawResponseText.indexOf("{");
    const endIdx = rawResponseText.lastIndexOf("}");
    if (startIdx !== -1 && endIdx !== -1 && endIdx > startIdx) {
      const jsonStr = rawResponseText.substring(startIdx, endIdx + 1).trim();
      try {
        const obj = JSON.parse(jsonStr);
        setParsedJson(obj);
      } catch (err) {
        console.error("JSONパース失敗:", err);
      }
    }
  }, [rawResponseText]);

  // 3D地球儀の設定
  useEffect(() => {
    if (!globeRef.current) return;
    globeRef.current.controls().autoRotate = false;
    globeRef.current.controls().enableZoom = true;
  }, []);

  // 例: parsedJson からマーカーを生成する場合
  useEffect(() => {
    if (!parsedJson) return;
    // 例えば parsedJson に "locations" という配列があり
    // "ドバイ:25.2048,55.2708" などが入っている想定なら parse→setMarkers
    // ここでは実装省略 or サンプル
    // setMarkers(...) 
  }, [parsedJson]);

  // ----------------------------------
  // 2) 手動送信: /google_matched_image
  // ----------------------------------
  const handleSendImage = () => {
    if (!file) {
      alert("アップロード画像がありません");
      return;
    }
    setLoading(true);
    setProgress(0);
    setImageSrc(null);

    const formData = new FormData();
    formData.append("image", file);

    timerRef.current = setInterval(() => {
      setProgress((prev) => (prev < 100 ? prev + 1 : 100));
    }, 50);

    axios
      .post("http://127.0.0.1:8000/matched_image", formData, { responseType: "blob" })
      .then((resp) => {
        const blobUrl = URL.createObjectURL(resp.data);
        setProgress(100);
        setImageSrc(blobUrl);
      })
      .catch((err) => {
        console.error("matched_image API error:", err);
        alert("解析送信に失敗");
      })
      .finally(() => {
        setTimeout(() => {
          setLoading(false);
          if (timerRef.current) clearInterval(timerRef.current);
        }, 500);
      });
  };

  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  // ----------------------------------
  // Render
  // ----------------------------------
  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-100 p-4">
      <h2 className="text-2xl font-bold mb-4">ResultPage1</h2>

      {/* 3D Globe */}
      <div className="relative w-full md:w-3/4 h-96 md:h-[600px] bg-white rounded shadow mb-4">
        <Globe
          ref={globeRef}
          width={800}
          height={500}
          backgroundColor="#ffffff"
          globeImageUrl="//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
          bumpImageUrl="//unpkg.com/three-globe/example/img/earth-topology.png"
          showAtmosphere
          atmosphereColor="lightblue"
          atmosphereAltitude={0.25}
          pointsData={markers}
          pointAltitude={0.03}
          pointColor={() => "crimson"}
          pointRadius={0.6}
          pointLabel={(d) => d.name}
        />
      </div>

      {/* 手動送信ボタン */}
      <button
        disabled={loading}
        onClick={handleSendImage}
        className="mb-4 bg-green-600 text-white px-5 py-2 rounded-lg hover:bg-green-700 transition"
      >
        画像を /google_matched_image に送信
      </button>

      {/* スピナー & 進捗バー */}
      {loading ? (
        <div className="flex flex-col items-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500 mb-4" />
          <div className="w-64 bg-gray-300 rounded-full h-4 mb-2">
            <div
              className="bg-blue-500 h-4 rounded-full"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-gray-700">{progress}%</p>
          <p className="text-gray-500 mt-2">解析中...</p>
        </div>
      ) : (
        imageSrc && (
          <div className="flex flex-col items-center">
            <img
              src={imageSrc}
              alt="Result"
              className="w-64 h-auto rounded-lg shadow"
            />
            <p className="mt-4 text-green-600 font-semibold">
              解析結果イメージが返却されました！
            </p>
          </div>
        )
      )}

      {/* (A) 生テキスト表示 */}
      {rawTextDisplay && (
        <div className="bg-white p-4 rounded shadow mt-4 max-w-2xl text-left">
          <h3 className="text-lg font-semibold mb-2">サーバーからの生テキスト:</h3>
          <pre className="text-xs whitespace-pre-wrap">{rawTextDisplay}</pre>
        </div>
      )}

      {/* (B) JSONパース結果 */}
      {parsedJson && (
        <div className="bg-white p-4 rounded shadow mt-4 max-w-2xl text-left">
          <h3 className="text-lg font-semibold mb-2">JSONとして抽出したデータ:</h3>
          <pre className="text-xs whitespace-pre-wrap">
            {JSON.stringify(parsedJson, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default ResultPage1;
