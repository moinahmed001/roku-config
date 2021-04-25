import asyncio
import os
import sys

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

EMAIL = os.environ.get('MEROSS_EMAIL') or "moinahmed001@gmail.com"
PASSWORD = os.environ.get('MEROSS_PASSWORD') or "adg123"

async def getStatus(device):

    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve all the MSS210 devices that are registered on this account
    await manager.async_device_discovery()
    plugs = manager.find_devices(device_type="mss210")
    i = 0

    while i < len(plugs):
        dev = plugs[i]
        await dev.async_update()

        if device in dev.name:
            is_on = dev.is_on()
            if is_on:
                print("on", end='')
            else:
                print("off", end='')
        i += 1


    if len(plugs) < 1:
        await asyncio.sleep(5)
        print("Attempting again as I could not find any plugs.")

    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()


if __name__ == '__main__':
    device = sys.argv[1]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getStatus(device))
    loop.close()
