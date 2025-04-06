from openai import AzureOpenAI 



client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",
)


def gpt_chat(messages):
    completion = client.chat.completions.create(  
        model=deployment,
        messages=messages,
        max_tokens=800,  
        temperature=0.7,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,
        stop=None,  
        stream=False,
    )
    return completion.choices[0].message.content
# chat_prompt = [
#     {
#         "role": "system",
#         "content": "أنت مساعد ذكاء اصطناعي متخصص في الإجابة على أسئلة العملاء عن المنتجات والأسئلة العامة."}
#        ,
#        {
#          "role": "user",
#          "content": "بقولك التي شيرت بتاع ابانوب فين"
#        }
# ]
# print(gpt_chat(chat_prompt))