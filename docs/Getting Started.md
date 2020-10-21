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
    - You'll want to be sure that the virtual environment is activated any time you try to run some code
2. [Install poetry](https://python-poetry.org/docs/#installation)
    - Poetry is the package manager we use (think `yarn` or `npm` for Python)
3. Install dependencies:
    ```bash
    poetry install
    ```
4. Activate our pre-commit hooks (formatting & linting):
    ```bash
    poetry run autohooks activate
    ```

## Helpful resources
- [Maker Protocol 101 slide deck](https://drive.google.com/file/d/1bEOlNk2xUXgwy0I_UlB_8tPPZ8mH1gy9/view)
- [Maker Protocol FAQs](https://github.com/makerdao/community/tree/master/faqs)
- [Maker Protocol docs](https://docs.makerdao.com/)
    - Specifically, the [smart contracts glossary](https://docs.makerdao.com/other-documentation/system-glossary) and [general glossary](https://github.com/makerdao/community/blob/master/faqs/glossary.md)
- [Maker Protocol source code](https://github.com/makerdao/dss)
    - I suggest enabling [annotations](https://docs.makerdao.com/other-documentation/smart-contract-annotations) for this (you can just prepend https://via.hypothes.is/ to any URL in the repo, like [this](https://via.hypothes.is/https://github.com/makerdao/dss/blob/master/src/vat.sol))
