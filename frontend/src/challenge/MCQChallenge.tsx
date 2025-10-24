import { useState } from "react";

type TChallenge = {
  difficulty: string;
  title: string;
  options: string[];
  correct_answer_id: number;
  explanation: string;
};

function MCQChallenge({
  challenge,
  showExplanation = false,
}: {
  challenge: TChallenge;
  showExplanation?: boolean;
}) {
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [shouldShowExplanation, setShouldShowExplanation] =
    useState<boolean>(showExplanation);
  const options: string[] =
    typeof challenge.options === "string"
      ? JSON.parse(challenge.options)
      : challenge.options;
  const handleOptionSelect = (index: number) => {
    if (!selectedOption) {
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
  return (
    <>
      <div className="challenge-display">
        <p>
          <strong>Difficulty</strong>:{challenge.difficulty}
        </p>
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
