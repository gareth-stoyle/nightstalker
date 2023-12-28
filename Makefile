.PHONY: test record server dashboard

test:
	@echo "Running unit tests..."
	python -m unittest discover -v .

record:
	@echo "Recording sleep..."
	python src/record.py 2>&1 | tee outputs/record_log.txt

server:
	@echo "Starting Flask server..."
	python app/app.py 2>&1 | tee outputs/server_log.txt

dashboard: test server
