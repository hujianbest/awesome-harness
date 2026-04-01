type SendEmailRequest = {
  to: string;
  subject: string;
  template: string;
};

export class ProviderClient {
  constructor(private readonly baseUrl: string) {}

  async sendEmail(request: SendEmailRequest) {
    if (!this.baseUrl) {
      throw new Error("missing provider base url");
    }

    return fetch(`${this.baseUrl}/emails`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
  }
}
