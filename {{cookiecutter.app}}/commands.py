import os
import subprocess
import re
from typing import Optional

import typer

app = typer.Typer()

DEFAULT_PROJECT = os.getenv("FLYTE_DEFAULT_PROJECT", "{{cookiecutter.default_project}}")
DEFAULT_DOMAIN = os.getenv("FLYTE_DEFAULT_DOMAIN", "{{cookiecutter.default_domain}}")
DEFAULT_WORKFLOW = os.getenv(
    "FLYTE_DEFAULT_WORKFLOW", "{{cookiecutter.app}}.workflows.example.my_wf"
)
DEFAULT_DOCKER_NAME = os.getenv("FLYTE_DEFAULT_DOCKER_NAME", "{{cookiecutter.app}}")
DEFAULT_DOCKER_REGISTRY = os.getenv(
    "FLYTE_DEFAULT_DOCKER_REGISTRY", "{{cookiecutter.default_docker_registry}}"
)
FLYTE_CONSOLE_URL = os.getenv("FLYTE_CONSOLE_URL", "{{cookiecutter.console_url}}")


def run(command: str, capture: bool = False) -> Optional[str]:
    if capture:
        captured = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        ).stdout
        print(captured)
        return captured
    else:
        subprocess.run(command, shell=True, check=True)
        return None


@app.command()
def build(
    registry: str = typer.Option(DEFAULT_DOCKER_REGISTRY, help="Docker registry"),
    name: str = typer.Option(DEFAULT_DOCKER_NAME, help="Docker image name"),
    version: str = typer.Option(..., help="Docker image and Flyte workflow version"),
    project: str = typer.Option(DEFAULT_PROJECT, help="Flyte project"),
    domain: str = typer.Option(DEFAULT_DOMAIN, help="Flyte domain"),
):
    tag = f"{name}:{version}"
    if registry:
        tag = f"{registry}/{tag}"

    run(f"docker build -t {tag} .")
    if registry:
        run(f"docker push {tag}")
    run(f"pyflyte --config flytekit.config package --image {tag} -f")
    run(
        f"flytectl register files --archive flyte-package.tgz --version {version} --project {project} --domain {domain}"
    )


@app.command()
def execute(
    workflow: str = typer.Option(DEFAULT_WORKFLOW, help="Workflow name"),
    version: Optional[str] = typer.Option(
        None,
        help="Docker image and Flyte workflow version. If not specified uses the latest.",
    ),
    project: str = typer.Option(DEFAULT_PROJECT, help="Flyte project"),
    domain: str = typer.Option(DEFAULT_DOMAIN, help="Flyte domain"),
):
    exec_spec_path = "exec_spec.yaml"
    if os.path.exists(exec_spec_path):
        os.remove(exec_spec_path)

    version_parameter = f"--version {version}" if version else "--latest"
    run(
        f"flytectl get launchplan --project {project} --domain {domain} {workflow} {version_parameter} --execFile {exec_spec_path}"
    )
    execution_result = run(
        f"flytectl create execution --project {project} --domain {domain} --execFile {exec_spec_path}",
        capture=True,
    )

    execution_name = re.search(r'name:"(.+)"', execution_result).group(1)

    print(
        "View the execution at",
        f"{FLYTE_CONSOLE_URL}/projects/{project}/domains/{domain}/executions/{execution_name}",
    )


@app.command()
def build_execute(
    registry: str = typer.Option(DEFAULT_DOCKER_REGISTRY, help="Docker registry"),
    name: str = typer.Option(DEFAULT_DOCKER_NAME, help="Docker image name"),
    version: str = typer.Option(..., help="Docker image and Flyte workflow version"),
    project: str = typer.Option(DEFAULT_PROJECT, help="Flyte project"),
    domain: str = typer.Option(DEFAULT_DOMAIN, help="Flyte domain"),
    workflow: str = typer.Option(DEFAULT_WORKFLOW, help="Workflow name"),
):
    build(
        registry=registry,
        name=name,
        version=version,
        project=project,
        domain=domain,
    )
    execute(workflow=workflow, version=version, project=project, domain=domain)


if __name__ == "__main__":
    app()
