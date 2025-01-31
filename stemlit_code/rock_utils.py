# from openai import OpenAI
# from dotenv import load_dotenv
# from fastapi import HTTPException
# import os
# load_dotenv()


# def openai_response(messages,model="gpt-4o-mini",max_tokens=250,temperature=0.1,stream=False):
#     try:

#         api_key = os.getenv(f"OPENAI_API_KEY")
#         client=OpenAI(api_key=api_key)
#         response = client.chat.completions.create(
#             model=model,
#             messages=messages,
#             temperature=temperature,
#             max_tokens=max_tokens,
#             stream=stream
#         )
#         if not stream:

#             return response.choices[0].message.content
        
#         for chunk in response:

#             current_content = chunk.choices[0].delta.content
#             if current_content:
#                 yield current_content
         
        
#     except Exception as e:
#         raise HTTPException(detail=f"Error from openai:{e}",status_code=403)
    


# def non_stream_get_response_openai(messages,model="gpt-4o-mini",max_tokens=250,temperature=0.1,stream=False):
#     try:
#         api_key = os.getenv(f"OPENAI_API_KEY")
#         client=OpenAI(api_key=api_key)
#         result = client.chat.completions.create(
#             model=model,
#             messages=messages,
#             temperature=temperature,
#             top_p=0.0001,
#             max_tokens=max_tokens,

#         )
#         messages = [choice.message.content for choice in result.choices]

#         return {"response": messages[0]}
#     except Exception as e:
#         # print("Error in creating campaigns from openAI:", str(e))
#         raise HTTPException(503)
    
# def non_stream_get_response_openai_preview(messages,model="gpt-4o-mini",max_tokens=250,temperature=0.1,stream=False):
#     try:
#         api_key = os.getenv(f"OPENAI_API_KEY")
#         client=OpenAI(api_key=api_key)
#         result = client.chat.completions.create(
#             model=model,
#             messages=messages
#             # temperature=temperature,
#             # top_p=0.0001,
#             # max_tokens=max_tokens,

#         )


#         return {"response": result.choices[0].message.content}
#     except Exception as e:
#         # print("Error in creating campaigns from openAI:", str(e))
#         raise HTTPException(503)
    

# def openai_response_structured(messages,model="gpt-4o-mini",max_tokens=250,temperature=0.1,stream=False,output_model=None):
#     try:

#         api_key = os.getenv(f"OPENAI_API_KEY")
#         client=OpenAI(api_key=api_key)
#         response = client.beta.chat.completions.parse(
#             model=model,
#             messages=messages,
#             temperature=temperature,
#             max_tokens=max_tokens,
#             response_format=output_model,
#         )

#         return response.choices[0].message.parsed
#     except Exception as e:
#         raise HTTPException(detail=f"Error from openai:{e}",status_code=403)

import boto3
import json
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

def bedrock_client():
    
    return boto3.client(
         
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        region_name= "us-east-1"
    )

def claude_response(messages, model_id="anthropic.claude-3-sonnet-20240229-v1:0", max_tokens=2000, temperature=0.1, stream=False):
    try:
        client = bedrock_client()
        payload = {
           "anthropic_version": "bedrock-2023-05-31",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
         
            # "stream": True
        }

        response = client.invoke_model_with_response_stream(
            body=json.dumps(payload),
            modelId=model_id
        )
        # response_body = json.loads(response["body"].read().decode("utf-8"))
        for event in response["body"]:
            chunk = json.loads(event["chunk"]["bytes"])
            if chunk["type"] == "content_block_delta":
                print(chunk["delta"].get("text", ""), end="")
                yield chunk["delta"].get("text", "")
        # if stream:
        #     for chunk in response_body:
        #         current_content = chunk.get("delta", {}).get("content", "")
        #         if current_content:
        #             yield current_content
        #             print(current_content)
        # else:
        #     return response_body["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(detail=f"Error from Bedrock: {e}", status_code=403)

def non_stream_get_response_bedrock(messages, model_id="anthropic.claude-3-sonnet-20240229-v1:0", max_tokens=250, temperature=0.1):
    try:
        client = boto3.client(
         
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        region_name= "us-east-1"
    )   
        # print("Client:", client)
        # models = client.list_models()
        # print(models)
        # # Extract and print model IDs
        # model_ids = [model['id'] for model in models]
        # print("Model IDs:", model_ids)
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        response = client.invoke_model(
            body=json.dumps(payload),
            modelId=model_id,
        )
        response_body = json.loads(response["body"].read().decode("utf-8"))
        print(response_body,response_body.get('content', ''))
        result = response_body.get('content', '')
        print(result[0]["text"],type(result[0]["text"]),"⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡")
        return result[0]["text"]
        # messages = [choice["message"]["content"] for choice in response_body["choices"]]
        # return {"response": messages[0]}
    except Exception as e:
        print(e,"-----------\n")
        raise HTTPException(status_code=503, detail=f"Error from Bedrock: {e}")

def non_stream_get_response_bedrock_preview(messages, model_id="anthropic.claude-3-sonnet-20240229-v1:0", max_tokens=250):
    try:
        client = bedrock_client()
        payload = {
            "model": model_id,
            "messages": messages
        }

        response = client.invoke_model(
            body=json.dumps(payload),
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response["body"].read().decode("utf-8"))
        return {"response": response_body["choices"][0]["message"]["content"]}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error from Bedrock: {e}")

def claude_response_structured(messages, model_id="anthropic.claude-3-sonnet-20240229-v1:0", max_tokens=250, temperature=0.1, output_model=None):
    try:
        client = bedrock_client()
        payload = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "response_format": output_model
        }

        response = client.invoke_model(
            body=json.dumps(payload),
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response["body"].read().decode("utf-8"))
        return response_body["choices"][0]["message"]["parsed"]
    except Exception as e:
        raise HTTPException(detail=f"Error from Bedrock: {e}", status_code=403)

prompt = "write about atria"
message=[{"role": "user", "content": "You are a helpful assistant that creates concise difference tables for pharmaceutical products"},
                    {"role": "assistant", "content": "How can i help you today"},
                    {"role": "user", "content": f"{prompt}"}]
messages=[
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
        },
        {
            "role": "assistant",
            "content": [{"type": "text", "text": prompt}],
        }
    ]

data = non_stream_get_response_bedrock(messages=message)
print(data)
import boto3
import json
from typing import List, Optional
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
load_dotenv()

import os
def get_bedrock_client():
    """Initialize Bedrock client"""
    print(os.getenv("AWS_ACCESS_KEY"))
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        region_name='us-east-1'  # Replace with your region
    )
    return bedrock

def create_pydantic_prompt(query: str, model: BaseModel):
    """Create a assistant prompt based on Pydantic model structure"""
    
    # Get the model's schema
    schema = model.model_json_schema()
    
    # Create a assistant prompt that describes the required structure
    assistant_prompt = f"""You are a helpful assistant that provides structured analysis.
        Your response must be a valid JSON object that matches exactly this schema:
        {json.dumps(schema, indent=2)}
        
        All fields are required and must match the specified types and constraints.
        Provide factual, well-researched information that fits this structure.
        """
    
    human_prompt = f"Analyze the following and provide response in the specified structure: {query}"
    
    return {
        "assistant": assistant_prompt,
        "human": human_prompt
    }

def invoke_claude_with_model(max_tokens:int, query:str, temprature:int, model: BaseModel) -> BaseModel:
    """Invoke Claude and return a validated Pydantic model instance"""
    client = get_bedrock_client()
    prompt = create_pydantic_prompt(query, model)
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": [
             {
                "role": "user",
                "content": prompt["human"]
            },
            {
                "role": "assistant",
                "content": prompt["assistant"]
            }
        ],
        "temperature": temprature  # Low temperature for consistent structured output
    }
    
    try:
        response = client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        response_text = response_body['content'][0]['text']
        
        # Parse the response text as JSON and validate with Pydantic
        response_dict = json.loads(response_text)
        validated_response = model.model_validate(response_dict)
        data=string_to_dict(validated_response.model_dump_json(indent=2))
        return data
        
    except Exception as e:
        print(f"Error processing response: {str(e)}")
        return None

import ast
def string_to_dict(dict_string):
    try:
        # Use ast.literal_eval to safely evaluate the string as a dictionary
        result_dict = ast.literal_eval(dict_string)
        if isinstance(result_dict, dict):
            return result_dict
        else:
            raise ValueError("The provided string does not represent a dictionary.")
    except (SyntaxError, ValueError) as e:
        print(f"Error converting string to dictionary: {e}")
        return None
