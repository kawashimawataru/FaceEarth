import React, { useState, useEffect, useRef } from "react";
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

  // ドット操作用 (4択xyプロット)
  const [dotX, setDotX] = useState(0.5); // 0.0 ~ 1.0
  const [dotY, setDotY] = useState(0.5); // 0.0 ~ 1.0
  const [dragging, setDragging] = useState(false);
  const plotRef = useRef(null);

  // 質問データを取得
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/get_random_questions")
      .then((res) => {
        // APIが返すJSONがオブジェクト形式の場合は配列化
        const questionArray = Object.values(res.data);
        setQuestions(questionArray);
      })
      .catch((err) => console.error(err));
  }, []);

  // ボタン形式の回答
  const handleSelectOption = (questionId, option) => {
    setAnswers((prev) => ({ ...prev, [questionId]: option }));
  };

  // スライダー(Yes/No)の回答
  // JSONのoptionsが2つある: [左ラベル, 右ラベル]
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

  // 4択 (XYプロット) のドラッグ開始
  const handleMouseDown = () => {
    setDragging(true);
  };

  // ドラッグ終了
  const handleMouseUp = () => {
    setDragging(false);
  };

  // ドット移動
  const handleMouseMove = (e) => {
    if (!dragging || !plotRef.current) return;
    const currentQuestion = questions[currentQuestionIndex];
    if (!currentQuestion?.options || currentQuestion.options.length !== 4) return;

    // plotRef 左上を基準にした座標を取得
    const rect = plotRef.current.getBoundingClientRect();
    let x = e.clientX - rect.left;
    let y = e.clientY - rect.top;

    // 0 ~ rect.width / 0 ~ rect.height
    x = Math.max(0, Math.min(x, rect.width));
    y = Math.max(0, Math.min(y, rect.height));
    const normX = x / rect.width;
    const normY = y / rect.height;

    setDotX(normX);
    setDotY(normY);

    // corners = [top-left, top-right, bottom-left, bottom-right]
    // options = 4つ
    const corners = [
      { x: 0, y: 0 },
      { x: 1, y: 0 },
      { x: 0, y: 1 },
      { x: 1, y: 1 },
    ];
    let minDist = Infinity;
    let minIndex = 0;

    corners.forEach((corner, i) => {
      const dx = normX - corner.x;
      const dy = normY - corner.y;
      const dist = dx * dx + dy * dy;
      if (dist < minDist) {
        minDist = dist;
        minIndex = i;
      }
    });

    // 最も近い corner に対応する option を回答としてセット
    const chosen = currentQuestion.options[minIndex];
    setAnswers((prev) => ({
      ...prev,
      [currentQuestion.question_id]: chosen,
    }));
  };

  // 次の質問へ
  const nextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
      // 必要ならXYプロットを初期化
      // setDotX(0.5);
      // setDotY(0.5);
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
  let sliderValue = 0;
  if (currentQuestion && currentQuestion.type === "Yes/No") {
    if (answers[currentQuestion.question_id] === currentQuestion?.options?.[1]) {
      sliderValue = 1;
    } else {
      sliderValue = 0;
    }
  }

  // ----- UIの分岐 -----
  // 1) Yes/No → スライダー
  // 2) image → 通常ボタン
  // 3) choice/choice2 → (4択かどうかで分岐)
  //    - 4つなら XYプロット
  //    - それ以外は fallback で通常ボタン
  // 4) その他 → fallback

  const renderQuestionUI = () => {
    if (!currentQuestion) {
      return <p>質問を読み込み中...</p>;
    }

    // ===============================
    // 1) Yes/No (2択) → スライダー
    // ===============================
    if (
      currentQuestion.type === "Yes/No" &&
      currentQuestion.options?.length >= 2
    ) {
      return (
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
            <span className="text-gray-600">{currentQuestion.options[0]}</span>
            <span className="text-gray-600">{currentQuestion.options[1]}</span>
          </div>
        </div>
      );
    }

    // =======================================
    // 2) image → 通常ボタン形式
    // =======================================
    if (currentQuestion.type === "image") {
      return (
        <div className="flex flex-wrap justify-center mb-6">
          {currentQuestion.options?.map((option) => {
            const isSelected = answers[currentQuestion.question_id] === option;
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
      );
    }

    // ======================================
    // 3) choice / choice2 → XY プロット or ボタン
    // ======================================
    if (currentQuestion.type === "choice" || currentQuestion.type === "choice2") {
      // XYプロット (4択のみ)
      if (currentQuestion.options?.length === 4) {
        return (
          <div
            ref={plotRef}
            className="relative bg-gray-100 border border-gray-400 mx-auto mb-6"
            style={{ width: "300px", height: "300px" }}
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
          >
            {/* 4隅にラベル */}
            <div className="absolute top-0 left-0 m-1 text-sm font-bold text-gray-700">
              {currentQuestion.options[0]}
            </div>
            <div className="absolute top-0 right-0 m-1 text-sm font-bold text-gray-700">
              {currentQuestion.options[1]}
            </div>
            <div className="absolute bottom-0 left-0 m-1 text-sm font-bold text-gray-700">
              {currentQuestion.options[2]}
            </div>
            <div className="absolute bottom-0 right-0 m-1 text-sm font-bold text-gray-700">
              {currentQuestion.options[3]}
            </div>

            {/* ドット */}
            <div
              className="absolute w-4 h-4 bg-blue-500 rounded-full shadow"
              style={{
                left: `${dotX * 100}%`,
                top: `${dotY * 100}%`,
                transform: "translate(-50%, -50%)",
                cursor: "grab",
              }}
            />
          </div>
        );
      } else {
        // 4択以外 → 通常ボタン
        return (
          <div className="flex flex-wrap justify-center mb-6">
            {currentQuestion.options?.map((option) => {
              const isSelected = answers[currentQuestion.question_id] === option;
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
        );
      }
    }

    // ============================
    // 4) fallback → 通常ボタン
    // ============================
    return (
      <div className="flex flex-wrap justify-center mb-6">
        {currentQuestion.options?.map((option) => {
          const isSelected = answers[currentQuestion.question_id] === option;
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
    );
  };

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

        {/* 質問文 */}
        {currentQuestion ? (
          <>
            <h2 className="text-xl font-semibold mb-4">
              {currentQuestion.question_text}
            </h2>
            {/* 質問タイプに応じたUI */}
            {renderQuestionUI()}
          </>
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
