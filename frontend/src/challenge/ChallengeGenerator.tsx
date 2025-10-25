import { useState } from "react";
import MCQChallenge from "./MCQChallenge";
import type { TChallenge, TDifficulty, TQuota } from "./type";

function ChallengeGenerator() {
  const [challenge, setChallenge] = useState<TChallenge | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [difficulty, setDifficulty] = useState<TDifficulty>("easy");
  const [quota, setQuota] = useState<TQuota | null>(null);

  const fetchQuota = async () => {};
  const generateChallenge = async () => {};
  const getNextResetTime = () => {};

  return (
    <>
      <div className="challenge-container">
        <h2>Coding Challenge Generator</h2>

        <div className="quota-display">
          <p>Challenge remaining today:{quota?.quota_remaining}</p>
          {quota?.quota_remaining === 0 && <p>Next reset :{0}</p>}
        </div>

        <div className="difficulty-selector">
          <label htmlFor="difficulty">Select Difficulty:</label>
          <select
            id="difficulty"
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value as TDifficulty)}
            disabled={isLoading}
          >
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>
        <button
          onClick={generateChallenge}
          disabled={isLoading || quota?.quota_remaining === 0}
          className="generate-button"
        >
          {isLoading ? "Generating" : "Generate Challenge"}
        </button>
      </div>
      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {challenge && <MCQChallenge challenge={challenge} />}
    </>
  );
}

export default ChallengeGenerator;
