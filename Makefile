create-venv:
	python3 -m venv venv
	@echo "Virtual environment created."

install-requirements: create-venv
	./venv/bin/pip install -r requirements.txt
	@echo "Requirements installed."

run-bot-server: install-requirements
	./venv/bin/python3 mafiabot.py
	@echo "Bot server is running."

.PHONY: create-venv install-requirements run-bot-server