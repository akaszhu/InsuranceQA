from openai import OpenAI
from dotenv import load_dotenv
from fastapi import HTTPException
import os
load_dotenv()


def openai_response(messages,model="gpt-4o-mini",max_tokens=250,temperature=0.1,stream=False):
    try:

        api_key = os.getenv(f"OPENAI_API_KEY")
        client=OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream
        )
        if not stream:

            return response.choices[0].message.content
        
        for chunk in response:

            current_content = chunk.choices[0].delta.content
            if current_content:
                yield current_content
         
        
    except Exception as e:
        raise HTTPException(detail=f"Error from openai:{e}",status_code=403)
    


def non_stream_get_response_openai(messages,model="gpt-4o-mini",max_tokens=250,temperature=0.1,stream=False):
    try:
        api_key = os.getenv(f"OPENAI_API_KEY")
        client=OpenAI(api_key=api_key)
        result = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=0.0001,
            max_tokens=max_tokens,

        )
        messages = [choice.message.content for choice in result.choices]

        return {"response": messages[0]}
    except Exception as e:
        # print("Error in creating campaigns from openAI:", str(e))
        raise HTTPException(503)
    
def non_stream_get_response_openai_preview(messages,model="gpt-4o-mini",max_tokens=250,temperature=0.1,stream=False):
    try:
        api_key = os.getenv(f"OPENAI_API_KEY")
        client=OpenAI(api_key=api_key)
        result = client.chat.completions.create(
            model=model,
            messages=messages
            # temperature=temperature,
            # top_p=0.0001,
            # max_tokens=max_tokens,

        )


        return {"response": result.choices[0].message.content}
    except Exception as e:
        # print("Error in creating campaigns from openAI:", str(e))
        raise HTTPException(503)
    

def openai_response_structured(messages,model="gpt-4o-mini",max_tokens=250,temperature=0.1,stream=False,output_model=None):
    try:

        api_key = os.getenv(f"OPENAI_API_KEY")
        client=OpenAI(api_key=api_key)
        response = client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=output_model,
        )

        return response.choices[0].message.parsed
    except Exception as e:
        raise HTTPException(detail=f"Error from openai:{e}",status_code=403)