import openai

API_KEY = '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'

openai.api_key = API_KEY

response = openai.Image.create(
    prompt="person talking underwater holding an orange juice",
    n=1,
    size="1024x1024"
)
image_url = response['data'][0]['url']
print(image_url)
