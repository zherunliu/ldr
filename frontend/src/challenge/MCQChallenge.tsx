import { useState } from "react";
import { type TChallenge } from "./type";
import { useLocation } from "react-router-dom";
import { UseApi } from "../utils/api";

function MCQChallenge({
  challenge,
  fetchHistory,
  showExplanation = false,
}: {
  challenge: TChallenge;
  fetchHistory?: () => Promise<void>;
  showExplanation?: boolean;
}) {
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [shouldShowExplanation, setShouldShowExplanation] =
    useState<boolean>(showExplanation);
  const location = useLocation();
  const { makeRequest } = UseApi();

  const options: string[] =
    typeof challenge.options === "string"
      ? JSON.parse(challenge.options)
      : challenge.options;

  const handleOptionSelect = (index: number) => {
    if (selectedOption === null) {
      setSelectedOption(index);
      setShouldShowExplanation(true);
    }
  };

  const getOptionClass = (index: number) => {
    if (selectedOption === null) return "option";
    if (index === challenge.correct_answer_id) {
      return "option correct";
    }
    if (index === selectedOption && index !== challenge.correct_answer_id) {
      return "option incorrect";
    }
    return "option";
  };

  const handleChallengeDelete = async (id: number) => {
    try {
      const data = await makeRequest(`history-delete/${id}`);
      console.log(data, id);
      fetchHistory?.();
    } catch (err) {
      console.error("Error Delete challenge:", err);
    }
  };

  return (
    <>
      <div className="challenge-display">
        <div className="flex justify-between items-center mb-2">
          <p>
            <strong>Difficulty</strong>: {challenge.difficulty}
          </p>
          {location?.pathname === "/history" && (
            <button
              onClick={() => {
                handleChallengeDelete(challenge.id);
              }}
              className="rounded-lg h-8 w-15 bg-red-500 hover:scale-105 hover:bg-red-600 text-white"
            >
              Delete
            </button>
          )}
        </div>
        <p className="challenge-title">{challenge.title}</p>
        <div className="options">
          {options.map((option, index) => (
            <div
              className={getOptionClass(index)}
              key={index}
              onClick={() => handleOptionSelect(index)}
            >
              {option}
            </div>
          ))}
        </div>
        {shouldShowExplanation && selectedOption !== null && (
          <div className="explanation">
            <h3>Explanation</h3>
            <p>{challenge.explanation}</p>
          </div>
        )}
      </div>
    </>
  );
}

export default MCQChallenge;
