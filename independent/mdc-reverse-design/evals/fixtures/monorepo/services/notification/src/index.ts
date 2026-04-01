import { ApprovalDecisionEvent } from "../../../packages/shared/events";
import { NotificationSender } from "./sender";
import { ProviderClient } from "./providerClient";

const provider = new ProviderClient(process.env.NOTIFY_BASE_URL ?? "");
const sender = new NotificationSender(provider);

export async function handleApprovalDecision(event: ApprovalDecisionEvent) {
  await sender.sendDecisionEmail(event);
}
