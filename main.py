
import os  
import base64
from openai import AzureOpenAI  
import helper


# Initialize Azure OpenAI Service client with key-based authentication    
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",
)

def append_message(messages, role, content):
    messages.append({
        "role": role,
        "content": content
    })
    
def add_to_file( content,role):
    with open("chat.txt", "a",encoding="utf-8") as file:
        file.write(role + " : " + content + "\n\n\n")
# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

#Prepare the chat prompt 
chat_prompt = [
    {
        "role": "system",
        "content": "أنت مساعد ذكاء اصطناعي متخصص في الإجابة على أسئلة العملاء عن المنتجات والأسئلة العامة."}
      # ,
      # {
      #   "role": "user",
      #   "content": "عاوز اعرف سعر موبيل ساامسونج s32"
      # },
      # {
      #   "role": "assistant",
      #   "content": "السعر التقريبي لموبايل سامسونج Galaxy S23 هو 25,000 جنيه مصري [doc1]."}
      # ,
      # {
      #   "role": "user",
      #   "content": "عندك حاجه ارخص من كدا"
      # }
      # ,
      # {
      #   "role": "assistant",
      #   "content": "السعر التقريبي لموبايل سامسونج Galaxy A54 هو 11,000 جنيه مصري، وهو أرخص من Galaxy S23 [doc1]."
      # },

      # {
      #   "role": "user",
      #   "content": "دا اوبشن جميل اوي"
      # }
]
    
# Include speech result if speech is enabled  
messages = chat_prompt  


def get_search_results(search_query):
  # Generate the completion  
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
      extra_body={
        "data_sources": [{
            "type": "azure_search",
            "parameters": {
              "endpoint": f"{search_endpoint}",
              "index_name": "vector-1742297530826",
              "semantic_configuration": "vector-1742297530826-semantic-configuration",
              "query_type": "vector_semantic_hybrid",
              "fields_mapping": {},
              "in_scope": True,
              "role_information": "You are an AI assistant that helps people find information.",
              "filter": None,
              "strictness": 3,
              "top_n_documents": 5,
              "authentication": {
                "type": "api_key",
                "key": f"{search_key}"
              },
              "embedding_dependency": {
                "type": "deployment_name",
                "deployment_name": "text-embedding-3-large"
              }
            }
          }]
      }
  )
  return completion.choices[0].message.content



while True:
  user_input = input("You: ")
  append_message(messages, "user", user_input)
  add_to_file(user_input,"user")
  response = get_search_results(user_input)
  x = "المعلومات المطلوبة غير متوفرة في البيانات المسترجعة. يرجى تجربة استفسار أو موضوع آخر."
  y = "The requested information is not found in the retrieved data. Please try another query or topic."

  if y == response or x == response:

    print("yessss1")
    response = helper.gpt_chat(messages)

     
  append_message(messages, "assistant", response)
  add_to_file(response,"assistant")

  print("Assistant:", response)

#"المعلومات المطلوبة غير متوفرة في البيانات المسترجعة. يرجى تجربة استفسار أو موضوع آخر."