#!/usr/bin/python3

import os
import sys
import git
import re
import yaml
import docker
import argparse
from difflib import ndiff
from collections import defaultdict

class DiffImageLists():
    """
    """
    def __init__(self, local_images, remote_images):
        self.local_images = local_images
        self.remote_images = remote_images

    def parse_image(self, image):
        # Gibt ('registry/namespace/image', 'tag') zurück
        if ':' in image:
            name, tag = image.rsplit(':', 1)
        else:
            name, tag = image, 'latest'
        return name, tag

    def basename(self, image_name):
        """Extracts image name without registry or namespace."""
        parts = image_name.split('/')
        return parts[-1]

    def normalize_image_list(self, image_list):
        return dict(self.parse_image(img) for img in image_list)

    def normalize_image_list_with_basename(self, image_list):
        """Returns a dict of full_name -> tag and a dict base:tag -> list of full names."""
        full_map = {}
        base_map = defaultdict(list)
        for img in image_list:
            name, tag = self.parse_image(img)
            base_id = f"{self.basename(name)}:{tag}"
            full_map[name] = tag
            base_map[base_id].append(name)
        return full_map, base_map

    def image_diff(self):

        local_dict = self.normalize_image_list(self.local_images)
        remote_dict = self.normalize_image_list(self.remote_images)

        output_lines = []
        header = f"{'Image':<40} | {'Local Tag':<15} | {'Remote Tag':<15}"
        output_lines.append(header)
        output_lines.append("=" * len(header))

        all_names = sorted(set(local_dict.keys()) | set(remote_dict.keys()))

        # header = f"{'Image':<40} | {'Local Tag':<15} | {'Remote Tag':<15}"
        # print(header)
        # print("="* len(header))

        for name in all_names:
            local_tag = local_dict.get(name, "")
            remote_tag = remote_dict.get(name, "")
            tag_note = ""

            if local_tag != remote_tag:
                tag_note = " <-- different" if local_tag and remote_tag else " <-- added/removed"

            output_lines.append(f"{name:<40} | {local_tag:<15} | {remote_tag:<15}{tag_note}")

        print("\n".join(output_lines))

    def image_and_registry_diff(self):
        local_map, local_base = self.normalize_image_list_with_basename(self.local_images)
        remote_map, remote_base = self.normalize_image_list_with_basename(self.remote_images)

        output_lines = []
        header = f"{'Image':<40} | {'Local Tag':<15} | {'Remote Tag':<15} | Note"
        output_lines.append(header)
        output_lines.append("=" * len(header))

        all_base_ids = set(local_base.keys()) | set(remote_base.keys())

        for base_id in sorted(all_base_ids):
            local_names = local_base.get(base_id, [])
            remote_names = remote_base.get(base_id, [])

            # Falls image:tag nur lokal oder nur remote ist
            if not remote_names:
                for name in local_names:
                    output_lines.append(f"{name:<40} | {local_map[name]:<15} | {'':<15} | added/removed")
                continue
            if not local_names:
                for name in remote_names:
                    output_lines.append(f"{name:<40} | {'':<15} | {remote_map[name]:<15} | added/removed")
                continue

            # Jetzt: image:tag existiert auf beiden Seiten, ggf. unterschiedliche registries
            for local_name in local_names:
                for remote_name in remote_names:
                    local_tag = local_map.get(local_name, "")
                    remote_tag = remote_map.get(remote_name, "")
                    note = ""

                    if local_tag != remote_tag:
                        note = "container update"
                    elif local_name != remote_name:
                        note = "registry change"
                    else:
                        # Gleiches image und Tag, keine Änderung
                        continue

                    combined_name = f"{local_name} ⇄ {remote_name}" if local_name != remote_name else local_name
                    output_lines.append(f"{combined_name:<40} | {local_tag:<15} | {remote_tag:<15} | {note}")

        print("\n".join(output_lines))


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
        self.update_url = self.args.git_url
        self.update_branch = self.args.branch
        self.dry_run = self.args.dry_run

        if self.compose_file is None and self.compose_dir is None:
            print("please use '--compose' or '--compose-dir'")
            sys.exit(1)

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
            default=None
        )

        # TODO
        # support compose.d directory
        p.add_argument(
            "--compose-dir",
            required=False,
            help="directory with many compose files",
            default=None
        )

        p.add_argument(
            "-G",
            "--git-url",
            required=False,
            help="git urls for update",
            default="https://github.com/mailcow/mailcow-dockerized.git"
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

        added_images, removed_images = self.compare_images(
            compose_data = compose_data,
            local_file_path = self.compose_file,
            remote_url = self.update_url,
            branch = self.update_branch
        )

        if len(added_images) > 0:
            if not self.dry_run:
                self.pull_new_container(added_images)

    def read_compose_dir(self):
        """
        """
        data = dict()
        data["services"] = dict()
        for compose_file in os.listdir(self.compose_dir):
            _file = os.path.join(self.compose_dir, compose_file)
            try:
                with open(_file) as f:
                    d = yaml.safe_load(f)
                    service = d.get("services")
                    data["services"].update(service)

            except Exception as e:
                print(f"⚠️ Errors when reading {compose_file}: {e}")

        return data

    def get_images_from_docker_compose_file(self, compose_data, file_path):
        """
        Liest die docker-compose.yml Datei und extrahiert alle Image-Namen.
        """
        # print("local images ...")

        if not compose_data:
            with open(file_path, 'r') as file:
                docker_compose_content = yaml.safe_load(file)
        else:
            docker_compose_content = compose_data

        # Suche nach allen Image-Referenzen
        images = []
        if isinstance(docker_compose_content, dict):
            images = [conf.get("image") for service, conf in docker_compose_content.get('services', {}).items()]

        images = sorted(images)

        # print(f"  - {images}")

        return images

    def get_images_from_remote_docker_compose(self, remote_url=None, repo_path="/tmp/mailcow", branch="master"):

        # print("remote images ...")

        if os.path.exists(os.path.join(repo_path, ".git")):
            # Repository existiert bereits – öffne es und mache ein Pull
            repo = git.Repo(repo_path)
            origin = repo.remotes.origin
            origin.pull()
        else:
            # Repository existiert noch nicht – klone es
            repo = git.Repo.clone_from(remote_url, repo_path)

        repo = git.Repo(repo_path)

        # Holen der Datei aus dem angegebenen Branch
        docker_compose_content = repo.git.show(f"origin/{branch}:docker-compose.yml")

        # Regex für das Extrahieren der "image:"-Zeilen
        images = re.findall(r"image:\s*(\S+)", docker_compose_content)

        images = sorted(images)

        # print(f"  - {images}")

        return images

    def pull_new_container(self, images):
        """
        """
        client = docker.from_env()

        for image in images:
            try:
                print(f"pull container image: {image}")
                client.images.pull(image)
                # print(f"Erfolgreich: {image}")
            except docker.errors.APIError as e:
                print(f"Error when pulling the image {image}: {str(e)}")

    def side_by_side_diff(self, local_images, remote_images):
        """
        """
        def split_image(image):
            if ':' in image:
                name, tag = image.split(':', 1)
            else:
                name, tag = image, 'latest'
            return name, tag

        # Indexiere beide Listen nach dem Image-Namen
        local_dict = {split_image(img)[0]: img for img in local_images}
        remote_dict = {split_image(img)[0]: img for img in remote_images}

        all_keys = sorted(set(local_dict.keys()) | set(remote_dict.keys()))

        print("{:<40} | {:<40}".format("Local Images", "Remote Images"))
        print("=" * 85)

        for key in all_keys:
            local = local_dict.get(key, "")
            remote = remote_dict.get(key, "")
            print("{:<40} | {:<40}".format(local, remote))

    def compare_images(self, compose_data, local_file_path, remote_url, branch):
        """
        Vergleicht die Image-Namen der lokalen und der Remote docker-compose.yml.
        """
        local_images = self.get_images_from_docker_compose_file(compose_data, local_file_path)
        remote_images = self.get_images_from_remote_docker_compose(remote_url=remote_url, repo_path="/tmp/mailcow", branch=branch)

        # print(local_images)

        diff = DiffImageLists(local_images, remote_images)
        diff.image_diff()
        print("\n")
        diff.image_and_registry_diff()
        print("\n")

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

        if removed_images:
            print("Removed images (local vs. remote):")
            for image in removed_images:
                print(f"  - {image}")

        return (added_images, removed_images)


def main(requirements_file="collections.yml"):
    """
    """
    updater = MailcowUpdater()
    updater.run()


if __name__ == "__main__":
    main()
