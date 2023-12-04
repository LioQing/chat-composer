import logging
from typing import Optional

import docker
from docker.errors import NotFound
from docker.models.containers import Container

from config.containment import containment_config
from core import models


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
    ) -> str:
        """Run a command in a container"""
        env = {
            "PYTHONUNBUFFERED": "1",
        }
        if pipeline:
            env["PATH"] = (
                f"{containment_config.base_directory}/"
                f"{pipeline.get_containment_directory()}/"
                f"{containment_config.python_venv}/bin:$PATH"
            )

        self.logger.debug(
            f"Running command in container {container.name}: {command}"
        )

        result = container.exec_run(
            command,
            workdir=workdir,
            environment=env,
        )

        output: str = result.output.decode("utf-8")

        if result.exit_code != 0:
            self.logger.error(
                f"Exit code {result.exit_code} when running command {command}"
            )
            self.logger.error(f"Output: {output}")

            raise RuntimeError(
                f"Unable to run command {command} in container"
                f" {container.name}"
            )

        self.logger.debug(f"Output: {output}")

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

    def create_user_containers(self):
        """Create containers for all users"""
        for user in models.User.objects.all():
            self.create_user_container(user)

    def create_user_container(self, user: models.User):
        """Create a container for the given user"""
        self.logger.info(f"Creating container for user {user.username}")

        # Remove container if it exists
        if self.user_has_container(user):
            self.delete_user_container(user)

        # Create container
        container = self.client.containers.run(
            containment_config.image,
            detach=True,
            tty=True,
            name=user.get_containment_name(),
        )

        # Create composer directory
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

        self.logger.info(
            f"Creating directory for pipeline {pipeline.name} "
            f"for user {pipeline.user.username} under {workdir}"
        )

        # Make directory
        self.container_exec_run(
            container,
            f"mkdir {workdir}",
        )

        # Create python environment
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

    def run_pipeline(self, pipeline: models.Pipeline):
        """Run the given pipeline"""
        container = self.get_user_container(pipeline.user)

        workdir = (
            f"{containment_config.base_directory}/"
            f"{pipeline.get_containment_directory()}"
        )

        # Run pipeline
        self.container_exec_run(
            container,
            "python -c \"print('Hello world')\"",
            workdir=workdir,
            pipeline=pipeline,
        )


containment = Containment()
