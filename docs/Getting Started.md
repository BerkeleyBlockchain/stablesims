# Getting Started

## Setting up the environment
0. If you don't have Python 3 on your machine, [install it](https://www.python.org/downloads/)
1. Clone the repo & enter the project root:
    ```bash
    git clone https://github.com/akirillo/bab-stablesims.git
    cd bab-stablesims
    ```
1. Create a virtual environment (at the project root) and activate it using:
    ```bash
    python3 -m venv venv
    . ./venv/bin/activate
    ```
    - You'll want to be sure that the virtual environment is activated any time you try to run any code
2. [Install poetry](https://python-poetry.org/docs/#installation)
    - Poetry is the package manager we use (think `yarn` or `npm` for Python)
3. Install dependencies:
    ```bash
    poetry install
    ```