response = client.images.generate(
    model="openai/dall-e-3",   # вместо просто "dall-e-3"
    prompt="test cat",
    n=1,
    size="1024x1024"
)