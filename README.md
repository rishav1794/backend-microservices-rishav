# backend-microservices-rishav

Personal Playground for backend microservices 

## Services

### user-service

- Stack: Python 3.12, FastAPI, Uvicorn
- Path: `services/user_service`

#### First-time setup in Codespaces

```bash
cd services/user_service
python -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001