#CREATED BY @o_OKarma
#API CREDITS: @Qewertyy
#PROVIDED BY https://github.com/Team-ProjectCodeX

#IMPORTS
import httpx, base64
from pyrogram import filters

#BOT FILE IMPORTS
#Name -> Your Bots File Name (Eg. From Liaa import pbot as app)
from Name import pbot as app


@app.on_message(filters.reply & filters.command("upscale"))
async def upscale_image(client, message):
    try:
        # Check if the replied message contains a photo
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.reply_text("Please reply to an image to upscale it.")
            return

        # Access the image file_id from the replied message
        image = message.reply_to_message.photo.file_id
        file_path = await client.download_media(image)

        with open(file_path, "rb") as image_file:
            f = image_file.read()

        b = base64.b64encode(f).decode("utf-8")

        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(
                "https://api.qewertyy.me/upscale", data={"image_data": b}, timeout=None
            )

        # Save the upscaled image
        with open("upscaled_image.png", "wb") as output_file:
            output_file.write(response.content)

        # Send the upscaled image as a PNG file
        await client.send_document(
            message.chat.id,
            document="upscaled_image.png",
            caption="Here is the upscaled image!",
        )

    except Exception as e:
        print(f"Failed to upscale the image: {e}")
        await message.reply_text("Failed to upscale the image. Please try again later.")
        # You may want to handle the error more gracefully here
