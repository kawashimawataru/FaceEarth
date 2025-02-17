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

  // 質問データを取得
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/get_random_questions")
      .then((res) => {
        // APIが返すJSONはオブジェクト形式 { question_yesno: {...}, question_choice: {...}, ... } の場合
        // 配列化してまとめる
        const questionArray = Object.values(res.data);
        setQuestions(questionArray);
      })
      .catch((err) => console.error(err));
  }, []);

  // ボタン形式の回答
  const handleSelectOption = (questionId, option) => {
    setAnswers((prev) => ({ ...prev, [questionId]: option }));
  };

  // スライダーの回答 (Yes/No 質問用)
  // JSONのoptionsが 2つある: [左ラベル, 右ラベル]
  const handleSlider = (question, value) => {
    const val = parseFloat(value);
    const threshold = 0.5;
    const [leftOption, rightOption] = question.options || [];
    if (!leftOption || !rightOption) return;

    // value < 0.5 → leftOption, >= 0.5 → rightOption
    const chosenOption = val < threshold ? leftOption : rightOption;

    setAnswers((prev) => ({
      ...prev,
      [question.question_id]: chosenOption,
    }));
  };

  // 次の質問へ
  const nextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
    } else {
      // 最後の質問なら結果画面へ
      navigate("/result", { state: { file, answers } });
    }
  };

  // 前の質問へ
  const prevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
    }
  };

  // 現在の質問
  const currentQuestion = questions[currentQuestionIndex];
  const totalQuestions = questions.length;

  // プログレスバー (％表示)
  const progressPercent = totalQuestions
    ? Math.floor(((currentQuestionIndex + 1) / totalQuestions) * 100)
    : 0;

  // スライダー表示用の値 (0 or 1)
  // すでに回答があれば、それを反映
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

        {/* 質問表示 */}
        {currentQuestion ? (
          <div className="text-center mb-6">
            <h2 className="text-xl font-semibold mb-4">
              {currentQuestion.question_text}
            </h2>

            {currentQuestion.type === "Yes/No" &&
            currentQuestion.options?.length >= 2 ? (
              // スライダーUI (2択)
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
              // その他 (4択など) → ボタンで回答
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

        {/* 戻る/次へ ボタン */}
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
