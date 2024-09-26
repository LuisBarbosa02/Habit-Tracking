# Habit Tracking

A program that helps create, control, and maintain relevant information about habits.

## Table of Contents
1. [Prerequisites](#prerequisites)
2.  [Installation](#installation)
3. [Usage](#usage)
4. [Troubleshooting](#troubleshooting)
5. [License](#license)

## Prerequisites

- **Python version**: ensure you have Python `3.12` or higher installed.
- **Standard Dependencies**: standard libraries used by the program:
	- `python-dateutil`
- **Dev Dependencies**: dev libraries used by the program:
	- `pytest`

If already installed, your Python version can be checked by running:
```bash
Python --version
```
If not, Python can be downloaded here [here](https://www.python.org/downloads/).

## Installation

1. Clone the repository (or download the ZIP file):
```bash
git clone https://github.com/LuisBarbosa02/Habit-Tracking.git
cd Habit-Tracking
```
2. Set up a virtual environment (Recommended):
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```
3. Install dependecies:
- For standard use run:
```bash
pip install -r requirements.txt
```
- For dev use run:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Usage

To run the program:
```bash
python main.py
```
As a result, the main menu of the program is shown.

## Troubleshooting

- If "Module not found", ensure the dependencies are properly installed:
```bash
pip install -r requirements.txt
# or
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## License
This project is licensed under the terms of the MIT license. See the LICENSE file for details.