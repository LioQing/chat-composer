import logging
import os
import tarfile
from enum import Enum, StrEnum
from pathlib import Path
from typing import Dict, Optional, Tuple

import docker
from docker.errors import NotFound
from docker.models.containers import Container
from rest_framework_simplejwt.tokens import RefreshToken

from config.containment import containment_config
from config.web import web_config
from core import models


class ContainmentFileSpecializer:
    """Specialize the containment files.

    This class provides functionality for specializing the containment files.
    """

    class __SpecializerState(Enum):
        """The state of the specializer."""

        NONE = 0
        NOT_CONTAINED = 1
        CONTAINED = 2

    class __SpecializerMarker(StrEnum):
        """The markers in the files."""

        CONTAINED = "# containment: contained"
        NOT_CONTAINED = "# containment: not contained"
        ELSE = "# containment: else"
        END = "# containment: end"
        COMPONENTS = "# containment: components"
        PIPELINE = "# containment: pipeline"

    tmp_dir_name: str
    pipeline: models.Pipeline

    def __init__(
        self, pipeline: models.Pipeline, tmp_dir_name: str = "containment_tmp"
    ):
        """Initialize the specializer."""
        self.tmp_dir_name = tmp_dir_name
        self.pipeline = pipeline

    def __enter__(self):
        """Enter the context.

        Generates a temporary directory containing the specialized
        files. The files are specialized from the current directory.
        """
        dir = Path(__file__).resolve().parent
        dir_tmp = dir / self.tmp_dir_name

        if not dir_tmp.exists():
            dir_tmp.mkdir()
            dir_tmp.chmod(0o777)

        for file in dir.iterdir():
            if file.name == self.tmp_dir_name:
                continue

            self.specialize(file)

        self.generate_components()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context.

        Deletes the temporary directory.
        """
        dir = Path(__file__).resolve().parent
        dir_tmp = dir / self.tmp_dir_name

        # Remove dir
        def rmdir(path: Path):
            """Remove the given directory."""
            for file in path.iterdir():
                if file.is_dir():
                    rmdir(file)
                else:
                    file.unlink()
            path.rmdir()

        rmdir(dir_tmp)

        # Remove tar
        tar_path = dir / f"{self.tmp_dir_name}.tar.gz"

        if tar_path.exists():
            tar_path.unlink()

    def specialize(self, path: Path):
        """Specialize the given file or directory.

        Give the path relative to the current directory.
        """
        dir = Path(__file__).resolve().parent
        dir_tmp = dir / self.tmp_dir_name
        dir_tmp_path = dir_tmp / path.relative_to(dir)

        if path.name == "__pycache__":
            return

        if path == Path(__file__).resolve():
            return

        if path.is_dir():
            if not dir_tmp_path.exists():
                dir_tmp_path.mkdir()
                dir_tmp_path.chmod(0o777)

            for file in path.iterdir():
                self.specialize(file)

            return

        if dir_tmp_path.exists():
            dir_tmp_path.unlink()

        with open(path, "r") as file:
            content = file.read()

        content = self.specialize_content(content, path)

        with open(dir_tmp_path, "w") as file:
            file.write(content)

    def specialize_content(
        self, content: str, path: Optional[Path] = None
    ) -> str:
        """Specialize the given content."""
        state = self.__SpecializerState.NONE
        comment_indent = 0

        lines = content.split("\n")

        for i, line in enumerate(lines.copy()):
            stripped_line = line.strip()

            if stripped_line == self.__SpecializerMarker.CONTAINED:
                state = self.__SpecializerState.CONTAINED
                comment_indent = len(line) - len(line.lstrip())
            elif stripped_line == self.__SpecializerMarker.NOT_CONTAINED:
                state = self.__SpecializerState.NOT_CONTAINED
                comment_indent = len(line) - len(line.lstrip())
            elif stripped_line == self.__SpecializerMarker.ELSE:
                if state == self.__SpecializerState.CONTAINED:
                    state = self.__SpecializerState.NOT_CONTAINED
                elif state == self.__SpecializerState.NOT_CONTAINED:
                    state = self.__SpecializerState.CONTAINED
                else:
                    raise RuntimeError(
                        "Cannot use else marker without contained or not"
                        f" contained marker in line {i}"
                        f" of file {path}"
                        if path
                        else ""
                    )
            elif stripped_line == self.__SpecializerMarker.END:
                if state != self.__SpecializerState.NONE:
                    state = self.__SpecializerState.NONE
                else:
                    raise RuntimeError(
                        "Cannot use end marker without contained, not"
                        f" contained, or else marker in line {i}"
                        f" of file {path}"
                        if path
                        else ""
                    )
            elif stripped_line == self.__SpecializerMarker.COMPONENTS:
                imports = [
                    "from modules.composer import init_component,"
                    " init_pipeline"
                ]
                for component in self.pipeline.get_components():
                    fn = component.function_name
                    imports.append(f"from .{fn} import {fn}")

                lines[i] = "\n".join(imports)
            elif stripped_line == self.__SpecializerMarker.PIPELINE:
                statements = []
                for component in self.pipeline.get_components():
                    fn = component.function_name

                    # Generate arguments
                    arguments = "\n".join(
                        [f"{' ' * 16}{l}" for l in component.get_arguments()]
                    )

                    # Generate arg for record
                    arg_assigns = models.Component.get_json_arguments(
                        component.arguments
                    )
                    arg_assigns[0] = f"{fn}.arg = {arg_assigns[0]}"
                    arg_assigns = "\n".join(
                        [f"{' ' * 12}{l}" for l in arg_assigns]
                    )

                    # Generate function call
                    statements.append(
                        f"        # {component.name}\n"
                        f"        with init_component({component.id}):\n"
                        f"{arg_assigns}\n"
                        f"{' ' * 12}{fn}.ret = {fn}(\n"
                        f"{arguments}\n"
                        f"{' ' * 12})"
                    )

                statements.append(
                    # fmt: off
                    "        # Response\n"
                    "        pipeline_helper.set_response"
                    f"({self.pipeline.response})"
                    # fmt: on
                )

                lines[i] = (
                    f"    with init_pipeline({self.pipeline.id},"
                    " user_message) as pipeline_helper:\n"
                )
                lines[i] += "\n\n".join(statements)
            else:
                if state == self.__SpecializerState.CONTAINED:
                    if stripped_line.startswith("# "):
                        lines[i] = line.replace("# ", "", 1)
                elif state == self.__SpecializerState.NOT_CONTAINED:
                    if stripped_line != "":
                        indent = len(line) - len(line.lstrip())
                        if indent < comment_indent:
                            lines[i] = indent * " " + "# " + line.lstrip()
                        else:
                            lines[i] = (
                                comment_indent * " "
                                + "# "
                                + line[comment_indent:]
                            )

        return "\n".join(lines)

    def generate_components(self):
        """Generate the components file."""
        dir = Path(__file__).resolve().parent
        dir_tmp = dir / self.tmp_dir_name / "pipeline"

        # Delete old components file
        for file in os.listdir(dir_tmp):
            if file != "__init__.py":
                os.remove(dir_tmp / file)

        for component in self.pipeline.get_components():
            component_path = dir_tmp / f"{component.function_name}.py"

            with open(component_path, "w") as file:
                file.write(component.code)

    def to_tar(self) -> bytes:
        """Convert the temporary directory to a tar file."""
        dir = Path(__file__).resolve().parent
        dir_tmp = dir / self.tmp_dir_name

        if not dir_tmp.exists():
            raise RuntimeError("Temporary directory does not exist")

        tar_path = dir / f"{self.tmp_dir_name}.tar.gz"

        with tarfile.open(tar_path, "w:gz") as tar:
            for file in os.listdir(dir_tmp):
                tar.add(dir_tmp / file, arcname=file)

        with open(tar_path, "rb") as tar:
            return tar.read()


class Containment:
    """Containment class for Docker containers"""

    client: docker.DockerClient
    logger: logging.Logger

    def __init__(self):
        """Initialize the containers"""
        self.logger = logging.getLogger(__name__)
        self.client = docker.from_env()

    def container_exec_run(
        self,
        container: Container,
        command: str,
        workdir: Optional[str] = None,
        pipeline: Optional[models.Pipeline] = None,
        env: Optional[Dict[str, str]] = None,
        raise_for_exit_code: bool = True,
        return_exit_code: bool = False,
    ) -> str | Tuple[str, int]:
        """Run a command in a container"""
        env_ = {
            "PYTHONUNBUFFERED": "1",
        }

        if pipeline:
            env_["PATH"] = (
                f"{containment_config.base_directory}/"
                f"{pipeline.get_containment_directory()}/"
                f"{containment_config.python_venv}/bin:$PATH"
            )

        if env:
            env_.update(env)

        self.logger.debug(
            f"Running command in container {container.name}: {command}"
        )

        result = container.exec_run(
            command,
            workdir=workdir,
            environment=env_,
        )

        output: str = result.output.decode("utf-8")

        if result.exit_code != 0 and raise_for_exit_code:
            self.logger.error(
                f"Exit code {result.exit_code} when running command {command}"
            )
            self.logger.error(f"Output: {output}")

            raise RuntimeError(
                f"Unable to run command {command} in container"
                f" {container.name}"
            )

        self.logger.debug(f"Output: {output}")

        if return_exit_code:
            return output, result.exit_code

        return output

    def get_user_container(self, user: models.User) -> Container:
        """Get the container for the given user"""
        return self.client.containers.get(user.get_containment_name())

    def user_has_container(self, user: models.User) -> bool:
        """Check if the given user has a container"""
        try:
            self.get_user_container(user)
            return True
        except NotFound:
            return False

    def user_container_is_running(self, user: models.User) -> bool:
        """Check if the given user's container is running"""
        container = self.get_user_container(user)
        return container.status == "running"

    def create_user_containers(self):
        """Create containers for all users"""
        for user in models.User.objects.all():
            self.create_user_container(user)

    def create_user_container(self, user: models.User):
        """Create a container for the given user"""
        # Create container
        if not self.user_has_container(user):
            self.logger.info(f"Creating container for user {user.username}")
            self.client.containers.run(
                containment_config.image,
                detach=True,
                tty=True,
                name=user.get_containment_name(),
            )

        container = self.get_user_container(user)

        # Run container
        if not self.user_container_is_running(user):
            self.logger.info(f"Starting container for user {user.username}")
            container.start()

        # Create composer directory
        result = container.exec_run(
            f"test -d {containment_config.base_directory}"
        )
        if result.exit_code != 0:
            self.container_exec_run(
                container, f"mkdir {containment_config.base_directory}"
            )

        # Create all pipeline directories
        for pipeline in user.pipeline_set.all():
            self.create_pipeline_directory(pipeline)

    def create_pipeline_directory(self, pipeline: models.Pipeline):
        """Create a directory for the given pipeline"""
        container = self.get_user_container(pipeline.user)

        workdir = (
            f"{containment_config.base_directory}/"
            f"{pipeline.get_containment_directory()}"
        )

        # Make directory
        result = container.exec_run(f"test -d {workdir}")
        if result.exit_code != 0:
            self.logger.info(
                f"Creating directory for pipeline {pipeline.name} "
                f"for user {pipeline.user.username} under {workdir}"
            )
            self.container_exec_run(
                container,
                f"mkdir {workdir}",
            )

        # Create python environment
        result = self.container_exec_run(
            container,
            "python --version",
        )

        if "python 3.11" not in result.lower():
            self.container_exec_run(
                container,
                f"python3 -m venv {containment_config.python_venv}",
                workdir=workdir,
            )

    def delete_user_container(self, user: models.User):
        """Delete the container for the given user"""
        container = self.get_user_container(user)

        container.remove(force=True)

    def delete_pipeline_directory(self, pipeline: models.Pipeline):
        """Delete the directory for the given pipeline"""
        container = self.get_user_container(pipeline.user)

        self.container_exec_run(
            container,
            "rm -rf"
            f" {containment_config.base_directory}/"
            f"{pipeline.get_containment_directory()}",
        )

    def run_pipeline(
        self,
        pipeline: models.Pipeline,
        user_message: str,
        refresh: RefreshToken,
    ):
        """Run the given pipeline"""
        container = self.get_user_container(pipeline.user)

        workdir = (
            f"{containment_config.base_directory}/"
            f"{pipeline.get_containment_directory()}"
        )

        # Specialize files
        with ContainmentFileSpecializer(pipeline) as specializer:
            # Remove old files except containment_config.python_venv
            self.container_exec_run(
                container,
                "find . -mindepth 1 -maxdepth 1 -not -name"
                f" {containment_config.python_venv} -exec rm -rf {{}} +",
                workdir=workdir,
            )

            # Put archive in container
            if not container.put_archive(workdir, specializer.to_tar()):
                raise RuntimeError("Unable to copy files to container")

        # Install dependencies
        self.container_exec_run(
            container,
            "pip install -r requirements.txt",
            workdir=workdir,
            pipeline=pipeline,
        )

        # Run pipeline
        sanitized_user_message = user_message.replace("'", r"'\''")
        self.container_exec_run(
            container,
            f"python -m main '{sanitized_user_message}'",
            workdir=workdir,
            pipeline=pipeline,
            env={
                "CHAT_COMPOSER_ACCESS_TOKEN": refresh.access_token,
                "CHAT_COMPOSER_REFRESH_TOKEN": str(refresh),
                "CHAT_COMPOSER_PORT": web_config.port,
            },
        )


containment = Containment()
