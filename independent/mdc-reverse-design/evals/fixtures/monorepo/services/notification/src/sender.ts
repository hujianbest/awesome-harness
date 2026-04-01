import { ApprovalDecisionEvent } from "../../../packages/shared/events";
import { ProviderClient } from "./providerClient";

export class NotificationSender {
  constructor(private readonly provider: ProviderClient) {}

  async sendDecisionEmail(event: ApprovalDecisionEvent) {
    const subject =
      event.decision === "approved" ? "Application approved" : "Application rejected";

    await this.provider.sendEmail({
      to: event.applicantEmail,
      subject,
      template: "approval-decision",
    });
  }
}
