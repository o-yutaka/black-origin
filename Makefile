PYTHON ?= python3

.PHONY: install run test lint loop

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) -m uvicorn BLACK_ORIGIN.ui.api:app --host 0.0.0.0 --port 8000

loop:
	$(PYTHON) -m BLACK_ORIGIN.kernel.main

test:
	$(PYTHON) -m BLACK_ORIGIN.kernel.main --cycles 1

lint:
	$(PYTHON) -m compileall BLACK_ORIGIN
