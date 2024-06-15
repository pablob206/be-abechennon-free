## Command utilities
```bash
git merge main --allow-unrelated-histories

python3 -m venv venv
source venv/bin/activate
touch .env  # build .env/copy .env.sample
pip install -r requirements.txt
pip install -r requirements_dev.txt
pip install -r requirements_test.txt
uvicorn main:app --reload

# black
black .
# flake8
flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
# pre-commit
pre-commit run --all-files
# bandit
python -m bandit -r test

# pytest
pytest -v
```
