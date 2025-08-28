# AI Skill Gap Analysis Tool (Starter Monorepo)

## Run locally (Docker)
1. `cp .env.example .env` (optional)
2. `make build`
3. `make run`
4. Test health:
   - Gateway: http://localhost:8080/health
   - Diagnose: POST http://localhost:8080/diagnose
   - Curriculum: POST http://localhost:8080/curriculum
   - Predict: POST http://localhost:8080/predict

## Sample Requests
POST /diagnose
{
  "student_profile": {"id": "s-123", "locale": "en-US"},
  "context": {"subject": "math", "taxonomy_version": "v3", "window_days": 28},
  "responses": [{"item_id":"i123","type":"msq","answer":["A","C"],"time_sec":45}]
}

POST /curriculum
{
  "mastery_vector": [{"skill_id":"skill:fractions.add","score":0.56}],
  "constraints": {"pace_minutes_per_day": 30, "modality": ["video","practice"]}
}

POST /predict
{
  "student_profile": {"id": "s-123"},
  "context": {"subject": "math"}
}
