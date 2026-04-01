package service

type ApprovalRepository interface {
	SavePending(applicationID string, applicant string) error
	MarkApproved(applicationID string, approver string) error
	Load(applicationID string) (*Application, error)
}

type ApprovalNotifier interface {
	SendApprovalNotification(applicationID string, applicant string) error
}

type Application struct {
	ID        string
	Applicant string
	Status    string
}

type ApprovalService struct {
	repo     ApprovalRepository
	notifier ApprovalNotifier
}

func NewApprovalService(repo ApprovalRepository, notifier ApprovalNotifier) *ApprovalService {
	return &ApprovalService{
		repo:     repo,
		notifier: notifier,
	}
}

func (s *ApprovalService) CreateApplication(applicationID string, applicant string) error {
	return s.repo.SavePending(applicationID, applicant)
}

func (s *ApprovalService) ApproveApplication(applicationID string, approver string) error {
	if err := s.repo.MarkApproved(applicationID, approver); err != nil {
		return err
	}

	application, err := s.repo.Load(applicationID)
	if err != nil {
		return err
	}

	return s.notifier.SendApprovalNotification(application.ID, application.Applicant)
}
