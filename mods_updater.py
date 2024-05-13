import os
import aioftp
import asyncio
import shutil
from pathlib import Path


ftp_host = os.environ.get("nitrado_ftp_host")
ftp_user = os.environ.get("nitrado_ftp_user")
ftp_password = os.environ.get("nitrado_ftp_password")
ftp_port = os.environ.get("nitrado_ftp_port")

assert ftp_host is not None
assert ftp_user is not None
assert ftp_password is not None
assert ftp_port is not None

NITRADO_MODS_DIR = "7daystodie/Mods"
LOCAL_7D2D_DIR = os.environ.get("PATH_7D2D")
LOCAL_MODS_DIR = Path(LOCAL_7D2D_DIR, "Mods")


def parse_local_path(source: str):
    """
    TODOC
    """
    relative_path = Path(source).relative_to(NITRADO_MODS_DIR)

    print(relative_path)

    return Path(LOCAL_MODS_DIR, relative_path)


def clear_and_backup_mods():
    """
    TODOC
    """
    BACKUP_PATH = Path(LOCAL_MODS_DIR, "backup")

    os.makedirs(BACKUP_PATH, exist_ok=True)

    for path in os.listdir(LOCAL_MODS_DIR):

        absolute_path = Path(LOCAL_MODS_DIR, path)

        if absolute_path == BACKUP_PATH:
            continue

        if absolute_path.is_file():
            continue

        shutil.copytree(absolute_path, Path(BACKUP_PATH, absolute_path.name), dirs_exist_ok=True)
        shutil.rmtree(absolute_path)


async def fetch_mods():
    """
    TODOC
    """
    clear_and_backup_mods()

    async with aioftp.Client.context(
        ftp_host,
        ftp_port,
        ftp_user,
        ftp_password,
    ) as client:

        nitrado_files = await client.list(recursive=True)

        for server_path, infos in nitrado_files:

            if infos["type"] != "file":
                continue

            if not str(server_path).startswith(NITRADO_MODS_DIR):
                continue

            local_path = parse_local_path(server_path)

            os.makedirs(local_path.parent, exist_ok=True)

            await client.download(
                server_path,
                destination=local_path.parent,
            )


if __name__ == "__main__":
    asyncio.run(fetch_mods())
