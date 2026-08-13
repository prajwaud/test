.PHONY: help install capture tune list dry-run send check clean

help:
	@echo "WCP OS - daily brief"
	@echo ""
	@echo "  make install    install dependencies"
	@echo "  make check      syntax and import check, no credentials needed"
	@echo ""
	@echo "  make capture    snapshot today's live data to fixtures/"
	@echo "  make tune       replay latest fixture through prompts/system.md"
	@echo "  make list       list prompt variants"
	@echo "  make compare A=system B=tighter"
	@echo ""
	@echo "  make dry-run    read live data, print the brief, send nothing"
	@echo "  make send       read, synthesize, and actually send"
	@echo ""
	@echo "Iteration loop: make capture, edit prompts/system.md, make tune"

install:
	pip install -r requirements.txt

check:
	python -m py_compile src/*.py
	python -c "import src.daily_brief, src.tune, src.capture, src.prompt_loader; print('imports ok')"

capture:
	python -m src.capture

tune:
	python -m src.tune

list:
	python -m src.tune --list

compare:
	@test -n "$(A)" -a -n "$(B)" || (echo "usage: make compare A=system B=variant"; exit 1)
	python -m src.tune --compare $(A),$(B)

dry-run:
	python -m src.daily_brief --dry-run

send:
	python -m src.daily_brief

clean:
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
