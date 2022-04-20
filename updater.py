import asyncio
import os
import shutil
import time
from zipfile import ZipFile

import aiofiles
import loguru
import toml
from aiohttp import ClientSession
from pyarmor.helper import get_platform_name


async def main():
    archive_name = f"{get_platform_name.format_platform()}.zip"
    session = ClientSession()
    response = await session.get(
        f"https://www.lolzdraw.win/builds/{archive_name}", ssl=False
    )
    file = await aiofiles.open(archive_name, "wb+")
    await file.write(await response.read())
    await file.close()
    archive = ZipFile(archive_name)
    folder_name = "cache"
    if folder_name in os.listdir():
        shutil.rmtree(folder_name)
    archive.extractall(folder_name)
    for file_name in os.listdir(folder_name):
        if file_name not in ["pytransform"]:
            if file_name not in os.listdir():
                shutil.copy(f"{folder_name}/{file_name}", file_name)
            else:
                if file_name == "settings.cfg":
                    local_config = toml.load(file_name)
                    remote_config = toml.load(f"{folder_name}/{file_name}")
                    for section in local_config:
                        if section in remote_config:
                            for field in local_config[section]:
                                if field in remote_config[section]:
                                    remote_config[section][field] = local_config[
                                        section
                                    ][field]
                    os.remove(file_name)
                    toml.dump(remote_config, open(file_name, "w+"))
                else:
                    local_file = await aiofiles.open(file_name, "rb")
                    remote_file = await aiofiles.open(
                        f"{folder_name}/{file_name}", "rb"
                    )
                    if await local_file.read() != await remote_file.read():
                        await local_file.close()
                        await remote_file.close()
                        os.remove(file_name)
                        shutil.copy(f"{folder_name}/{file_name}", file_name)
                        if file_name == "requirements.txt":
                            os.system("python -m pip install -r requirements.txt")
        else:
            if file_name in os.listdir():
                shutil.rmtree(file_name)
            shutil.copytree(f"{folder_name}/{file_name}", file_name)
    archive.close()
    os.remove(archive_name)
    await session.close()
    loguru.logger.success("All files have been updated!")
    time.sleep(3)
    exit()


asyncio.get_event_loop().run_until_complete(main())
