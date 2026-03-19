.PHONY: setup-backend setup-frontend dev dev-backend dev-frontend test test-backend \
       release prod-setup prod-start prod-stop prod-backup

# === Development ===

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

# === Release ===

RELEASE_DIR = release/beanbrain

release: test
	@echo "Building release..."
	rm -rf release/
	mkdir -p $(RELEASE_DIR)/backend $(RELEASE_DIR)/frontend
	# Backend: source + deps spec
	cp -r backend/app $(RELEASE_DIR)/backend/
	cp backend/pyproject.toml backend/uv.lock $(RELEASE_DIR)/backend/
	# Frontend: build
	cd frontend && npm run build
	cp -r frontend/build $(RELEASE_DIR)/frontend/
	cp frontend/package.json frontend/package-lock.json $(RELEASE_DIR)/frontend/
	# Top-level files
	cp Makefile $(RELEASE_DIR)/
	# Package
	cd release && tar czf beanbrain-release.tar.gz beanbrain/
	@echo "Release built: release/beanbrain-release.tar.gz"

# === Production (runs on target machine) ===

prod-setup:
	cd backend && uv sync --frozen --no-dev
	cd frontend && npm ci --omit=dev

prod-start:
	@echo "Starting BeanBrain..."
	@cd backend && uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 &
	@cd frontend && PORT=3000 HOST=127.0.0.1 node build &
	@echo "Backend: http://127.0.0.1:8000  Frontend: http://127.0.0.1:3000"

prod-stop:
	@-pkill -f "uvicorn app.main:app" 2>/dev/null
	@-pkill -f "node build" 2>/dev/null
	@echo "Stopped."

prod-backup:
	@mkdir -p backups
	@cp backend/beanbrain.db backups/beanbrain-$$(date +%F-%H%M%S).db
	@echo "Backup: backups/beanbrain-$$(date +%F-%H%M%S).db"
	@find backups/ -name "*.db" -mtime +30 -delete 2>/dev/null; true
