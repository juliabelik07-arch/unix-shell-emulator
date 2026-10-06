.PHONY: run test clean

run:
	python src/praka1.py --vfs vfs.json

test:
	python src/praka1.py --vfs vfs.json --script tests/test_vfs.txt

clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__