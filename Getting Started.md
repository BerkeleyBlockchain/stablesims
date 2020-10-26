# Getting Started

## Setting up the environment
1. If you don't have Python 3 on your machine, [install it](https://www.python.org/downloads/)
2. Clone the repo & enter the project root:
    ```bash
    git clone https://github.com/akirillo/bab-stablesims.git
    cd bab-stablesims
    ```
3. Create a virtual environment (at the project root) and activate it using:
    ```bash
    python3 -m venv venv
    . ./venv/bin/activate
    ```
    - You'll want to be sure that the virtual environment is activated any time you try to run some code
4. Install `poetry` (our package manager, think `yarn` or `npm` for Python):
    ```bash
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
    ```
5. Install dependencies:
    ```bash
    poetry install
    ```
6. Activate `autohooks`, which we use for pre-commit git hooks (formatting & linting):
    ```bash
    poetry run autohooks activate
    ```

## Helpful resources
- [Maker DAO Black Thursday post-mortem](https://blog.makerdao.com/the-market-collapse-of-march-12-2020-how-it-impacted-makerdao/)
- [Maker Protocol 101 slide deck](https://drive.google.com/file/d/1bEOlNk2xUXgwy0I_UlB_8tPPZ8mH1gy9/view)
- [Maker Protocol FAQs](https://github.com/makerdao/community/tree/master/faqs)
- [Maker Protocol docs](https://docs.makerdao.com/)
    - Specifically, the [smart contracts glossary](https://docs.makerdao.com/other-documentation/system-glossary) and [general glossary](https://github.com/makerdao/community/blob/master/faqs/glossary.md)
- [Maker Protocol source code](https://github.com/makerdao/dss)
    - I suggest enabling [annotations](https://docs.makerdao.com/other-documentation/smart-contract-annotations) for this (you can just prepend https://via.hypothes.is/ to any URL in the repo, like [this](https://via.hypothes.is/https://github.com/makerdao/dss/blob/master/src/vat.sol))
