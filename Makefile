all:
	@echo 'Use "make venv" for install dependencies or "make run" for profiling.'
.PHONY: all


venv:
	rm -rf venv
	python3 -m venv venv
	./venv/bin/pip install wheel
	./venv/bin/pip install -r requirements.txt
.PHONY: venv


input.txt:
	@echo "Creating dummy text file from random text"
	@./venv/bin/python3 lorem_text_gen.py --sentences=10000 > input.txt


run: input.txt
	@echo "Starting measurements: 3-gram, words -------------------------------"
	@./venv/bin/python3 ngram.py -i input.txt -n 3 -u words
	@echo "Starting measurements: 3-gram, characters --------------------------"
	@./venv/bin/python3 ngram.py -i input.txt -n 3 -u characters
	@echo "Starting measurements: 5-gram, words -------------------------------"
	@./venv/bin/python3 ngram.py -i input.txt -n 5 -u words
	@echo "Starting measurements: 5-gram, characters --------------------------"
	@./venv/bin/python3 ngram.py -i input.txt -n 5 -u characters
.PHONY: run


clean:
	@ echo "Cleaning up"
	@rm -rf venv input.txt
.PHONY: clean
