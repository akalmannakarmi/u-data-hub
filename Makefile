install:
	pip install -r requirements.txt

run:
	python main.py

clean:
	rm -r -f instance
	rm -r -f logs

clear:
	rm -r -f logs