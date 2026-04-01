package http

import (
	stdhttp "net/http"

	"orderapproval/internal/service"
)

type router struct {
	approvals *service.ApprovalService
}

func NewRouter(approvals *service.ApprovalService) stdhttp.Handler {
	r := &router{approvals: approvals}

	mux := stdhttp.NewServeMux()
	mux.HandleFunc("POST /applications", r.handleCreateApplication)
	mux.HandleFunc("POST /applications/approve", r.handleApproveApplication)

	return mux
}

func (r *router) handleCreateApplication(w stdhttp.ResponseWriter, req *stdhttp.Request) {}

func (r *router) handleApproveApplication(w stdhttp.ResponseWriter, req *stdhttp.Request) {}
