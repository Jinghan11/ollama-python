from ollama import Client

# cluster A100
# client = Client(host='http://10.64.86.xxx:3060')

# cluster RTX 3090
client = Client(host='http://10.64.86.xxx:3060')

# cluster RTX 4060Ti
# client = Client(host='http://10.64.193.xxx:3060')

# response = client.generate(model='llama3', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])

response = client.generate(model='llama3', prompt=
    'Why is the sky blue?',
)

print(f"{response['response']}\nResponse Speed is  {(response['eval_count'] / response['eval_duration']) * 10**9} token/sec")