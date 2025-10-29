import { useEffect, useState } from "react";
import MCQChallenge from "./MCQChallenge";
import type { TChallenge, TDifficulty, TQuota } from "./type";
import { UseApi } from "../utils/api";

function ChallengeGenerator() {
  const [challenge, setChallenge] = useState<TChallenge | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [difficulty, setDifficulty] = useState<TDifficulty>("easy");
  const [quota, setQuota] = useState<TQuota | null>(null);
  const { makeRequest } = UseApi();

  useEffect(() => {
    fetchQuota();
  }, []);

  const fetchQuota = async () => {
    try {
      const data = await makeRequest("quota");
      setQuota(data);
    } catch (err) {
      console.error("Error fetching quota:", err);
    }
  };
  const generateChallenge = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await makeRequest("generate-challenge", {
        method: "POST",
        body: JSON.stringify({ difficulty }),
      });
      setChallenge(data);
      fetchQuota();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to generate challenge"
      );
    } finally {
      setIsLoading(false);
    }
  };
  const getNextResetTime = () => {
    if (!quota?.last_reset_date) return null;
    const resetDate = new Date(quota.last_reset_date);
    resetDate.setHours(resetDate.getHours() + 24);
    return resetDate;
  };

  return (
    <>
      <div className="challenge-container">
        <h2>Coding Challenge Generator</h2>

        <div className="quota-display">
          <p>Challenge remaining today:{quota?.quota_remaining}</p>
          {quota?.quota_remaining === 0 && (
            <p>Next reset :{getNextResetTime()?.toLocaleString()}</p>
          )}
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

      {challenge && !isLoading && <MCQChallenge challenge={challenge} />}

      {/* {challenge && !isLoading ? <MCQChallenge challenge={challenge} /> : null} */}
    </>
  );
}

export default ChallengeGenerator;
