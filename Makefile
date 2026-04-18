# Makefile for DevOps automation
.PHONY: setup run build test clean

setup:
	pip install -r requirements.txt

run:
	python -m streamlit run app.py

build:
	docker build -t devops-quickcart:latest .

test:
	@echo "Running tests..."
	flake8 app.py || true

clean:
	rm -rf __pycache__
	docker rm -f quickcart-container || true
