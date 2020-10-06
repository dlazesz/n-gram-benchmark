all:
	@echo 'Use "make venv" for install dependencies or "make run" for profiling.'
.PHONY: all


venv:
	rm -rfv venv
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
	./venv/bin/pip freeze
.PHONY: venv


run:
	@./venv/bin/python3 ngram.py
.PHONY: run