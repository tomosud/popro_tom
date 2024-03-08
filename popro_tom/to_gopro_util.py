
import asyncio
from open_gopro import WirelessGoPro, Params

async def main():
    async with WirelessGoPro() as gopro:
        #await gopro.ble_setting.resolution.set(Params.Resolution.RES_4K)
        #await gopro.ble_setting.fps.set(Params.FPS.FPS_30)


        await gopro.ble_command.set_shutter(shutter=Params.Toggle.ENABLE)
        await asyncio.sleep(2) # Record for 2 seconds
        await gopro.ble_command.set_shutter(shutter=Params.Toggle.DISABLE)

        # Download all of the files from the camera
        #media_list = (await gopro.http_command.get_media_list()).data.files
        #for item in media_list:
        #    await gopro.http_command.download_file(camera_file=item.filename)

asyncio.run(main())


