import os
import aioftp
import asyncio
import datetime
from pathlib import Path


ftp_host = os.environ.get("nitrado_ftp_host")
ftp_user = os.environ.get("nitrado_ftp_user")
ftp_password = os.environ.get("nitrado_ftp_password")
ftp_port = 21

assert ftp_host is not None
assert ftp_user is not None
assert ftp_password is not None
assert ftp_port is not None

SERVER_SAVE = "7daystodie/Saves/Rusuxo County/Rusuxo County"


def str_now():
    return str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"))


def parse_address(source: str, directory: Path):
    """
    TODOC
    """
    return Path(directory, source).parent


async def main():
    """
    TODOC
    """

    async with aioftp.Client.context(
        ftp_host,
        ftp_port,
        ftp_user,
        ftp_password,
    ) as client:
        files = await client.list(recursive=True)

        datas = [
            (file, parse_address(file, Path(f"backup/save_{str_now()}")))
            for file, infos in files
            if infos["type"] == "file"
        ]

        for server_path, local_path in datas:
            if not str(server_path).startswith(SERVER_SAVE):
                continue

            print(local_path)

            await client.download(
                server_path,
                destination=local_path,
            )


if __name__ == "__main__":
    asyncio.run(main())
