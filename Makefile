.PHONY: test record server dashboard

test:
	@echo "Running unit tests..."
	python -m unittest discover -v .

record:
	@echo "Recording sleep..."
	python src/record.py

server:
	@echo "Starting Flask server..."
	cd app && python app.py

dashboard: test server
