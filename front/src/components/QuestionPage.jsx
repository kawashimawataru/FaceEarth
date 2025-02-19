import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

function QuestionPage() {
  const location = useLocation();
  const navigate = useNavigate();

  // アップロードされた画像ファイル & プレビュー用URL
  const file = location.state?.file;
  const imageUrl = location.state?.imageUrl;

  // 質問配列
  const [questions, setQuestions] = useState([]);
  // 現在の質問インデックス
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  // ユーザーの回答 (question_id => answer)
  const [answers, setAnswers] = useState({});
  // エラーメッセージ
  const [errorMessage, setErrorMessage] = useState("");

  // 送信しようとした JSON を画面表示 (デバッグ)
  const [finalPayload, setFinalPayload] = useState(null);

  // 質問取得
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/get_random_questions")
      .then((res) => {
        const questionArray = Object.values(res.data);
        setQuestions(questionArray);
      })
      .catch((err) => console.error(err));
  }, []);

  // ボタン形式の回答
  const handleSelectOption = (questionId, option) => {
    setAnswers((prev) => ({ ...prev, [questionId]: option }));
    setErrorMessage(""); // エラー解除
  };

  // Yes/No (スライダー) 質問
  const handleSlider = (question, value) => {
    const val = parseFloat(value);
    const threshold = 0.5;
    const [leftOption, rightOption] = question.options || [];
    if (!leftOption || !rightOption) return;
    const chosenOption = val < threshold ? leftOption : rightOption;

    setAnswers((prev) => ({
      ...prev,
      [question.question_id]: chosenOption,
    }));
    setErrorMessage("");
  };

  // 前の質問へ
  const prevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
      setErrorMessage("");
      setFinalPayload(null);
    }
  };

  // 次 or 送信
  const nextQuestion = async () => {
    const currentQ = questions[currentQuestionIndex];
    if (!currentQ) return;

    // 回答されていない場合 → エラー
    const userAnswer = answers[currentQ.question_id];
    if (!userAnswer) {
      setErrorMessage("※ 質問に回答してください。");
      return;
    }

    if (currentQuestionIndex < questions.length - 1) {
      // 次の質問へ
      setCurrentQuestionIndex((prev) => prev + 1);
      setErrorMessage("");
      setFinalPayload(null);
    } else {
      // 最終 → サーバーに送信
      const payload = questions.map((q) => {
        const answer = answers[q.question_id];
        let score = {};
        if (q.scoring && answer && q.scoring[answer]) {
          score = q.scoring[answer];
        }
        return {
          question_id: q.question_id,
          question_text: q.question_text,
          answer,
          score,
        };
      });

      setFinalPayload(payload);

      try {
        // サーバーに JSON を送信し、レスポンス(テキスト)を受け取る
        const response = await axios.post(
          "http://127.0.0.1:8000/map_generate",
          payload,
          {
            headers: { "Content-Type": "application/json" },
            // 返り値をテキストで受け取る
            responseType: "text",
          }
        );
        const serverText = response.data; // 返却されたテキスト

        // 次のページへ: fileと一緒に rawText も渡す
        navigate("/result1", {
          state: {
            file,
            rawText: serverText, // ここでサーバー応答の生テキストを送る
          },
        });
      } catch (err) {
        console.error(err);
        setErrorMessage("送信に失敗しました。再度お試しください。");
      }
    }
  };

  // 現在の質問
  const currentQuestion = questions[currentQuestionIndex];
  const totalQuestions = questions.length;

  // プログレスバー
  const progressPercent = totalQuestions
    ? Math.floor(((currentQuestionIndex + 1) / totalQuestions) * 100)
    : 0;

  // スライダー (Yes/No) の値
  let sliderValue = 0;
  if (currentQuestion && currentQuestion.type === "Yes/No") {
    if (answers[currentQuestion.question_id] === currentQuestion?.options?.[1]) {
      sliderValue = 1;
    } else {
      sliderValue = 0;
    }
  }

  return (
    <div className="flex flex-col md:flex-row items-center justify-center h-screen bg-gray-100 p-4">
      {/* 左側: 質問UI */}
      <div className="flex flex-col items-center bg-white p-6 rounded-lg shadow-lg w-full md:w-1/2 max-w-xl">
        {/* プログレスバー */}
        <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
          <div
            className="bg-blue-500 h-4 rounded-full"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        {/* 質問番号 */}
        <p className="text-sm text-gray-500 mb-2">
          質問 {currentQuestionIndex + 1} / {totalQuestions}
        </p>

        {currentQuestion ? (
          <div className="text-center mb-6">
            <h2 className="text-xl font-semibold mb-4">
              {currentQuestion.question_text}
            </h2>
            {/* エラーメッセージ */}
            {errorMessage && (
              <p className="text-red-500 font-bold mb-2">{errorMessage}</p>
            )}

            {/* Yes/No → スライダー */}
            {currentQuestion.type === "Yes/No" &&
            currentQuestion.options?.length >= 2 ? (
              <div className="flex flex-col items-center mb-6">
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={sliderValue}
                  className="w-64"
                  onChange={(e) => handleSlider(currentQuestion, e.target.value)}
                />
                <div className="flex justify-between w-64 mt-1">
                  <span className="text-gray-600">
                    {currentQuestion.options[0]}
                  </span>
                  <span className="text-gray-600">
                    {currentQuestion.options[1]}
                  </span>
                </div>
              </div>
            ) : (
              // その他 → ボタン
              <div className="flex flex-wrap justify-center mb-6">
                {currentQuestion.options?.map((option) => {
                  const isSelected =
                    answers[currentQuestion.question_id] === option;
                  return (
                    <button
                      key={option}
                      className={`m-2 px-6 py-3 rounded-lg transition ${
                        isSelected
                          ? "bg-blue-500 text-white"
                          : "bg-gray-300 hover:bg-gray-400"
                      }`}
                      onClick={() =>
                        handleSelectOption(currentQuestion.question_id, option)
                      }
                    >
                      {option}
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        ) : (
          <p>質問を読み込み中...</p>
        )}

        {/* ボタン(戻る/次へ) */}
        <div className="flex space-x-4">
          {currentQuestionIndex > 0 && (
            <button
              className="bg-gray-400 text-white px-4 py-2 rounded-lg hover:bg-gray-500 transition"
              onClick={prevQuestion}
            >
              戻る
            </button>
          )}
          <button
            className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition"
            onClick={nextQuestion}
          >
            {currentQuestionIndex < totalQuestions - 1 ? "次へ" : "送信"}
          </button>
        </div>

        {/* 送信するJSONを画面表示 (デバッグ用) */}
        {finalPayload && (
          <div className="mt-6 p-4 bg-gray-100 w-full text-left rounded shadow">
            <h3 className="text-lg font-bold mb-2 text-gray-700">送信JSON:</h3>
            <pre className="text-xs text-gray-800">
              {JSON.stringify(finalPayload, null, 2)}
            </pre>
          </div>
        )}
      </div>

      {/* 右側: アップロード画像プレビュー */}
      <div className="flex items-center justify-center mt-8 md:mt-0 md:ml-8 w-full md:w-1/2">
        {imageUrl && (
          <img
            src={imageUrl}
            alt="Uploaded preview"
            className="max-w-xs w-full h-auto rounded-lg shadow"
          />
        )}
      </div>
    </div>
  );
}

export default QuestionPage;
