VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

.PHONY: all clean venv compile install test

all: venv compile install

venv:
	@echo "Creating virtual environment..."
	@python3 -m venv $(VENV_DIR)
	@echo "Update pip,,,"
	@$(PIP) install --upgrade pip
	@echo "Installing packages..."
	@$(PIP) install Faker
	@$(PIP) install ujson
	@echo "Activating virtual environment..."
	. $(VENV_DIR)/bin/activate

compile:
	@echo "Compiling the code..."
	@$(PYTHON) setup.py build

install:
	@echo "Installing the module..."
	@$(PYTHON) setup.py install
 
test: all
	@echo "Running perfomance test..."
	@$(PYTHON) perfomance_test.py
	@echo "Running unit tests..."
	@$(PYTHON) -m unittest discover -s .

clean:
	@echo "Cleaning up..."
	@rm -rf build
	@rm -rf $(VENV_DIR)
