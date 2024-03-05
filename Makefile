install:
	pip install -r requirements.txt

run:
	python main.py

clean:
	rm example.db
	rm instance/mydb.db