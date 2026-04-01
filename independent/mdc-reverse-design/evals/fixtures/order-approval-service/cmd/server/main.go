package main

import (
	"log"
	"net/http"

	approvalhttp "orderapproval/internal/http"
	"orderapproval/internal/notify"
	"orderapproval/internal/repository"
	"orderapproval/internal/service"
)

func main() {
	repo := repository.NewMemoryApprovalRepository()
	notifier := notify.NewWebhookClient("http://notification.example")
	approvalService := service.NewApprovalService(repo, notifier)

	mux := approvalhttp.NewRouter(approvalService)

	log.Fatal(http.ListenAndServe(":8080", mux))
}
