package repository

import (
	"fmt"

	"orderapproval/internal/service"
)

type MemoryApprovalRepository struct {
	applications map[string]*service.Application
}

func NewMemoryApprovalRepository() *MemoryApprovalRepository {
	return &MemoryApprovalRepository{
		applications: map[string]*service.Application{},
	}
}

func (r *MemoryApprovalRepository) SavePending(applicationID string, applicant string) error {
	r.applications[applicationID] = &service.Application{
		ID:        applicationID,
		Applicant: applicant,
		Status:    "pending",
	}
	return nil
}

func (r *MemoryApprovalRepository) MarkApproved(applicationID string, approver string) error {
	application, ok := r.applications[applicationID]
	if !ok {
		return fmt.Errorf("application %s not found", applicationID)
	}

	application.Status = "approved"
	return nil
}

func (r *MemoryApprovalRepository) Load(applicationID string) (*service.Application, error) {
	application, ok := r.applications[applicationID]
	if !ok {
		return nil, fmt.Errorf("application %s not found", applicationID)
	}

	return application, nil
}
