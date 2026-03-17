.PHONY: setup-backend setup-frontend dev dev-backend dev-frontend test test-backend

setup-backend:
	cd backend && uv sync

setup-frontend:
	cd frontend && npm install

dev:
	@echo "Starting backend and frontend..."
	@make dev-backend & make dev-frontend

dev-backend:
	cd backend && uv run uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

test: test-backend

test-backend:
	cd backend && uv run pytest tests/ -v
