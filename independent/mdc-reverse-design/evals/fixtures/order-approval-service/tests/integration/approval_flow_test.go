package integration

import (
	"testing"

	"orderapproval/internal/repository"
	"orderapproval/internal/service"
)

type fakeNotifier struct {
	sent bool
}

func (n *fakeNotifier) SendApprovalNotification(applicationID string, applicant string) error {
	n.sent = true
	return nil
}

func TestApproveApplicationSendsNotification(t *testing.T) {
	repo := repository.NewMemoryApprovalRepository()
	notifier := &fakeNotifier{}
	approvals := service.NewApprovalService(repo, notifier)

	if err := approvals.CreateApplication("APP-1", "alice"); err != nil {
		t.Fatalf("create failed: %v", err)
	}

	if err := approvals.ApproveApplication("APP-1", "manager-1"); err != nil {
		t.Fatalf("approve failed: %v", err)
	}

	if !notifier.sent {
		t.Fatal("expected approval notification to be sent")
	}
}
