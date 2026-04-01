export type ApprovalDecisionEvent = {
  applicationId: string;
  applicantEmail: string;
  decision: "approved" | "rejected";
};
