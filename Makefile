.PHONY: test run start

test:
	@echo "Running unit tests..."
	cd app && python -m unittest discover tests -v

run:
	@echo "Starting Flask server..."
	python app/app.py

start: test run
