from flytekit import task, workflow

from {{cookiecutter.app}}.workflows.hello import get_hello_message


@task
def say_hello() -> str:
    message = get_hello_message()
    print(message)
    return message


@workflow
def my_wf() -> str:
    res = say_hello()
    return res


if __name__ == "__main__":
    print(f"Running my_wf() {my_wf()}")
