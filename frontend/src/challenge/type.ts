export type TChallenge = {
  id: number;
  difficulty: TDifficulty;
  date_created: Date;
  created_by: string;
  title: string;
  options: string[];
  correct_answer_id: number;
  explanation: string;
};

export type TQuota = {
  id: number;
  user_id: string;
  quota_remaining: number;
  last_reset_date: Date;
};

export type TDifficulty = "easy" | "medium" | "hard";
