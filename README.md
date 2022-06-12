# Flyte template

Template for creating [Flyte](https://flyte.org/) workflows.

Run `cookiecutter https://github.com/RobinKa/flyte-template.git` to instantiate.

Parameters:

| Name                        | Description                                                                                                                     | Default                    |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| `app`                       | Name of the directory and project that will be created. Must only contain characters for valid Python modules (eg. no hyphens). | `app`                      |
| `default_project`           | Default Flyte project for commands if none is passed.                                                                           | `flytesnacks`              |
| `default_domain`            | Default Flyte domain for commands if none is passed.                                                                            | `development`              |
| `default_docker_registry` | Default Docker registry to push images to if none is passed. Can be empty string for local only.                              | `localhost:5000`           |
| `console_url`               | Url to the Flyte console without trailing slash. Shown when executing workflows.                                                | `http://localhost/console` |
