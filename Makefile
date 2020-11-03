all:
	@echo 'Use "make venv" for install dependencies or "make run" for profiling.'
.PHONY: all


venv:
	rm -rfv venv
	python3 -m venv venv
	./venv/bin/pip install wheel
	./venv/bin/pip install -r requirements.txt
.PHONY: venv


run:
	@echo "Creating dummy text file"
	@./venv/bin/python3 lorem_text_gen.py --words=100000 > input.txt
	@echo "Starting measurements"
	@./venv/bin/python3 ngram.py -i input.txt -n 3
.PHONY: run