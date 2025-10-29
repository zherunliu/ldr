import { useEffect, useState } from "react";
import MCQChallenge from "../challenge/MCQChallenge";
import { type TChallenge } from "../challenge/type";
import { UseApi } from "../utils/api";

function HistoryPanel() {
  const [history, setHistory] = useState<TChallenge[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const { makeRequest } = UseApi();

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await makeRequest("my-history");
      setHistory(data.challenges);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load history");
    } finally {
      setIsLoading(false);
    }
  };
  if (isLoading) {
    return <div className="loading">Loading history...</div>;
  }
  if (error) {
    return (
      <div className="error-message">
        <p>{error}</p>
        <button onClick={fetchHistory}>Retry</button>
      </div>
    );
  }

  return (
    <>
      <div className="history-panel">
        <h2>History</h2>
        {history.length === 0 ? (
          <p>No challenge history</p>
        ) : (
          <div className="history-list">
            {history.map((challenge) => {
              return (
                <MCQChallenge
                  challenge={challenge}
                  key={challenge.id}
                  showExplanation
                  fetchHistory={fetchHistory}
                />
              );
            })}
          </div>
        )}
      </div>
    </>
  );
}

export default HistoryPanel;
