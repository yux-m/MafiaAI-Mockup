venv:
	python3 -m venv venv
	@echo "Virtual environment created."

install:
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt
	@echo "Requirements installed."

run-mafia-bot: venv install
	python3 mafiabot.py
	@echo "Bot server is running."

run-narrator-bot: venv install
	python3 narrator_gm.py
	@echo "Bot server is running."

all: venv install run-bot

.PHONY: venv install run-bot