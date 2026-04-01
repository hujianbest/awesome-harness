package notify

type WebhookClient struct {
	baseURL string
}

func NewWebhookClient(baseURL string) *WebhookClient {
	return &WebhookClient{baseURL: baseURL}
}

func (c *WebhookClient) SendApprovalNotification(applicationID string, applicant string) error {
	return nil
}
