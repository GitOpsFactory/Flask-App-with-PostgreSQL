Python Flask + PostgreSQL + Kubernetes DevOps Project
Project Overview

This project demonstrates a complete DevOps workflow using:

Python Flask application
PostgreSQL database
Docker containerization
GitHub Actions CI/CD
DockerHub image registry
Kubernetes deployment using Minikube

The application provides:

Web dashboard
Store user entries
Fetch user data
PostgreSQL integration
Real-time pod information
Kubernetes deployment practice
Architecture
User Browser
     ↓
Kubernetes Service (NodePort)
     ↓
Flask Python App Pod
     ↓
PostgreSQL Pod

CI/CD Flow:

GitHub Push
     ↓
GitHub Actions
     ↓
Docker Image Build
     ↓
Push to DockerHub
     ↓
Kubernetes Deployment
Technologies Used
Technology	Purpose
Python Flask	Web Application
PostgreSQL	Database
Docker	Containerization
GitHub Actions	CI/CD
DockerHub	Image Registry
Kubernetes	Container Orchestration
Minikube	Local Kubernetes Cluster
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3b9e5927-ec35-4f9a-a544-6e1a0439123d" />

