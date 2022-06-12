# {{ cookiecutter.app }}

Workflow scripts are in `{{cookiecutter.app}}/`. Run commands with `commands.py` to build and execute them.

## Prerequisites

- Docker
- Python 3.8+
- [FlyteCTL](https://github.com/flyteorg/flytectl) (configured for your remote)

## Setup

Run `pip install -r requirements.txt -r dev-requirements.txt`

## Commands

Run `python commands.py --help`

Examples:

- `python commands.py build --version v1`
- `python commands.py execute --version v1`
- `python commands.py build-execute --version v1`
