import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

function QuestionPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answer, setAnswer] = useState(null);
  const file = location.state?.file;

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/get_random_questions")
      .then((res) => setQuestions(Object.values(res.data)))
      .catch((err) => console.error(err));
  }, []);

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      navigate("/result", { state: { file } });
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <h2 className="text-lg font-bold mb-4">{questions[currentQuestionIndex]?.question_text}</h2>

      {questions[currentQuestionIndex]?.type === "Yes/No" ? (
        <input type="range" min="0" max="1" step="0.01" className="w-64" onChange={(e) => setAnswer(e.target.value)} />
      ) : (
        questions[currentQuestionIndex]?.options.map((option) => (
          <button key={option} className={`m-2 px-6 py-3 rounded-lg transition ${answer === option ? "bg-blue-500 text-white" : "bg-gray-300 hover:bg-gray-400"}`} onClick={() => setAnswer(option)}>
            {option}
          </button>
        ))
      )}

      <button className="mt-4 bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition" onClick={handleNext}>
        次へ
      </button>
    </div>
  );
}

export default QuestionPage;
