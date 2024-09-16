from openai import OpenAI

client = OpenAI()

image1 = "https://link.mybestautoglassco.com/conversations-assets/location/LNR9nBoI1U6Hvs31hDgv/contact/GiEIRLji8TsjzGplQSRf/ME1f9256c8a5df1d42598169ddf767e69b.jpeg"
image2 = "https://storage.googleapis.com/msgsndr/LNR9nBoI1U6Hvs31hDgv/media/66c1787ae7142402c533d331.jpeg"
image3 = "https://storage.googleapis.com/msgsndr/LNR9nBoI1U6Hvs31hDgv/media/66c1771766f58d54c2d87af2.jpeg"
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "extract vin from the image and return accurate VIN number only",
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image3
                    },
                }
            ],
        },
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format={"type": "text"},
)

print(response.choices[0].message.content)
