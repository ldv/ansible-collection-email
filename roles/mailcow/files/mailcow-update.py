#!/usr/bin/python3

import git
import os
import re
import yaml
import docker
import argparse

class MailcowUpdater():
    """
    """
    def __init__(self):
        """
        """
        self.args = {}
        self.parse_args()

        self.compose_file = self.args.compose
        self.compose_dir = self.args.compose_dir
        self.update_branch = self.args.branch
        self.dry_run = self.args.dry_run

    def parse_args(self):
        """
            parse arguments
        """
        p = argparse.ArgumentParser(description='update mailcow container.')

        p.add_argument(
            "-C",
            "--compose",
            required=False,
            help="compose file",
            default="mailcow-compose.conf"
        )

        # TODO
        # support compose.d directory
        p.add_argument(
            "--compose-dir",
            required=False,
            help="directory with many compose files",
            default="docker-compose.d"
        )

        p.add_argument(
            "-B",
            "--branch",
            required=False,
            help="update againt branch ...",
            default="master"
        )

        p.add_argument(
            "--dry-run",
            required=False,
            help="do nothing.",
            action='store_true',
            default=False
        )

        self.args = p.parse_args()

    def run(self):
        """
        """
        compose_data = None
        if self.compose_dir:
            compose_data = self.read_compose_dir()

        self.compare_images(
            compose_data = compose_data,
            local_file_path = self.compose_file,
            remote_url = None,
            branch = self.update_branch
        )

    def read_compose_dir(self):
        """
        """
        data = dict()
        data["services"] = dict()
        for compose_file in os.listdir(self.compose_dir):
            print(compose_file)

            _file = os.path.join(self.compose_dir, compose_file)
            try:
                with open(_file) as f:
                    d = yaml.safe_load(f)

                    service = d.get("services")

                    print(service)

                    data["services"].update(service)

            except Exception as e:
                print(f"⚠️ Errors when reading {compose_file}: {e}")

        print(data)

        return data

    def get_images_from_docker_compose_file(self, compose_data, file_path):
        """
        Liest die docker-compose.yml Datei und extrahiert alle Image-Namen.
        """
        print("local images ...")

        if not compose_data:
            with open(file_path, 'r') as file:
                docker_compose_content = yaml.safe_load(file)
        else:
            docker_compose_content = compose_data

        # Suche nach allen Image-Referenzen
        image_lines = []
        if isinstance(docker_compose_content, dict):
            # services = docker_compose_content.get('services', {})
            image_lines = [conf.get("image") for service, conf in docker_compose_content.get('services', {}).items()]

            # Hier wird das Dictionary durchlaufen
            #for service, config in docker_compose_content.get('services', {}).items():
            #    image = config.get('image')
            #    if image:
            #        image_lines.append(image)

        # print(f"  - {image_lines}")

        return image_lines

    def get_images_from_remote_docker_compose(self, remote_url=None, repo_path=".", branch="master"):

        print("remote images ...")

        if remote_url is not None:
            # Klonen des Remote-Repositorys in ein temporäres Verzeichnis
            repo = git.Repo.clone_from(remote_url, "/tmp")

        if repo_path:
            repo = git.Repo(repo_path)

        # Holen der Datei aus dem angegebenen Branch
        docker_compose_content = repo.git.show(f"origin/{branch}:docker-compose.yml")

        # Regex für das Extrahieren der "image:"-Zeilen
        image_lines = re.findall(r"image:\s*(\S+)", docker_compose_content)

        # print(f"  - {image_lines}")

        return image_lines

    def docker_pull_with_dockerpy(self, images):
        """
        Verwendet docker-py, um das Docker-Image zu ziehen.
        """
        client = docker.from_env()

        for image in images:
            try:
                print(f"pull container image: {image}")
                client.images.pull(image)
                # print(f"Erfolgreich: {image}")
            except docker.errors.APIError as e:
                print(f"Error when pulling the image {image}: {str(e)}")

    def compare_images(self, compose_data, local_file_path, remote_url, branch):
        """
        Vergleicht die Image-Namen der lokalen und der Remote docker-compose.yml.
        """
        local_images = self.get_images_from_docker_compose_file(compose_data, local_file_path)
        remote_images = self.get_images_from_remote_docker_compose(remote_url=None, repo_path=".", branch="master")

        # Finden von Unterschieden zwischen den Images
        local_set = set(local_images)
        remote_set = set(remote_images)

        added_images = remote_set - local_set
        removed_images = local_set - remote_set

        if added_images or removed_images:
            print("Differences in the container images:")
        else:
            print("No differences in the container images.")

        if added_images:
            print("Added images (remote vs. local):")
            for image in added_images:
                print(f"  - {image}")

            if not self.dry_run:
                self.docker_pull_with_dockerpy(added_images)

        if removed_images:
            print("Removed images (local vs. remote):")
            for image in removed_images:
                print(f"  - {image}")

# local_file_path = "./docker-compose.yml"
# remote_url = None # "https://github.com/username/repository.git"  # URL des Remote-Repositorys
# repo_path="."
# branch = "master"  # Hier kannst du den Branchnamen anpassen
#
# compare_images(local_file_path, remote_url, branch)


def main(requirements_file="collections.yml"):
    """
    Hauptfunktion: prüft installierte vs. benötigte Collections und installiert bei Bedarf.
    """
    updater = MailcowUpdater()
    updater.run()


if __name__ == "__main__":
    main()
