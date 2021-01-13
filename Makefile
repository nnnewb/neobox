dev:
	if [ ! -d venv ]; then python3 -m venv venv; fi
	source venv/bin/activate && pip install pip-tools
	source venv/bin/activate && \
		pip-compile requirements-dev.in -o requirements-dev.txt && \
		pip-compile && \
		pip-sync requirements-dev.txt requirements.txt

start:
	source venv/bin/activate && python main.py
