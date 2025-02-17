import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

function QuestionPage() {
  const location = useLocation();
  const navigate = useNavigate();

  // アップロード情報
  const file = location.state?.file;
  const imageUrl = location.state?.imageUrl;

  // 質問関連
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({}); // question_id => answer

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/get_random_questions")
      .then((res) => {
        // 取得したオブジェクトを配列化
        const questionArray = Object.values(res.data);
        setQuestions(questionArray);
      })
      .catch((err) => console.error(err));
  }, []);

  const handleSelectOption = (questionId, option) => {
    setAnswers((prev) => ({ ...prev, [questionId]: option }));
  };

  const handleSlider = (questionId, value) => {
    // 0 → No, 1 → Yes など文字変換したい場合
    const answerText = value === "0" ? "いいえ" : "はい";
    setAnswers((prev) => ({ ...prev, [questionId]: answerText }));
  };

  const nextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
    } else {
      // 最終質問 → 結果画面へ
      navigate("/result", { state: { file, answers } });
    }
  };

  const prevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
    }
  };

  // 現在の質問
  const currentQuestion = questions[currentQuestionIndex];
  const totalQuestions = questions.length;

  // プログレス（0～100%）
  const progressPercent = totalQuestions
    ? Math.floor(((currentQuestionIndex + 1) / totalQuestions) * 100)
    : 0;

  return (
    <div className="flex flex-col md:flex-row items-center justify-center h-screen bg-gray-100 p-4">
      {/* 左側: 質問/操作 */}
      <div className="flex flex-col items-center bg-white p-6 rounded-lg shadow-lg w-full md:w-1/2 max-w-xl">
        {/* プログレスバー */}
        <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
          <div
            className="bg-blue-500 h-4 rounded-full"
            style={{ width: `${progressPercent}%` }}
          ></div>
        </div>

        {/* 質問番号 */}
        <p className="text-sm text-gray-500 mb-2">
          質問 {currentQuestionIndex + 1} / {totalQuestions}
        </p>

        {/* 質問文 */}
        {currentQuestion ? (
          <div className="text-center mb-6">
            <h2 className="text-xl font-semibold mb-2">{currentQuestion.question_text}</h2>

            {/* Yes/No → スライダー */}
            {currentQuestion.type === "yesno" ? (
              <div className="flex flex-col items-center">
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="1"
                  className="w-64"
                  value={
                    answers[currentQuestion.question_id] === "はい"
                      ? 1
                      : answers[currentQuestion.question_id] === "いいえ"
                      ? 0
                      : 0
                  }
                  onChange={(e) =>
                    handleSlider(currentQuestion.question_id, e.target.value)
                  }
                />
                <div className="flex justify-between w-64 mt-1">
                  <span className="text-gray-600">いいえ</span>
                  <span className="text-gray-600">はい</span>
                </div>
              </div>
            ) : (
              // それ以外 → ボタン
              <div className="flex flex-wrap justify-center">
                {currentQuestion.options.map((option) => {
                  const isSelected = answers[currentQuestion.question_id] === option;
                  return (
                    <button
                      key={option}
                      className={`m-2 px-6 py-3 rounded-lg transition ${
                        isSelected
                          ? "bg-blue-500 text-white"
                          : "bg-gray-300 hover:bg-gray-400"
                      }`}
                      onClick={() => handleSelectOption(currentQuestion.question_id, option)}
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

        {/* ボタン類 */}
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
            {currentQuestionIndex < totalQuestions - 1 ? "次へ" : "解析へ"}
          </button>
        </div>
      </div>

      {/* 右側: アップロード画像プレビュー（常に表示） */}
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
