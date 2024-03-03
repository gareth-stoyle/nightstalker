.PHONY: test record server dashboard

test:
	@echo "Running unit tests..."
	python -m unittest discover -v .

record: test
	@echo "Recording sleep..."
	python -u src/main.py 2>&1 | tee record_log.txt

server:
	@echo "Starting Flask server..."
	python -u app/app.py 2>&1 | tee server_log.txt

dashboard: test server
