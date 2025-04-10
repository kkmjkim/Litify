import uuid
from pprint import pprint

from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from api.state import (
    session_store,
    state_mapping,
    StatuteState,
    Context,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# class Prompt(BaseModel):
#     session_id: str = None
#     state: str = None
#     utterance: str

@app.get("/healthy")
async def healthy():
    return {"status": "OK"}


@app.post("/prompt")
async def prompt(data: Request):
    data = await data.json()
    print(data)
    session_id = data.get("session_id", "")
    state_name = data.get("state", "")
    utterance = data.get('utterance')

    if 'utterance' not in data:
        raise HTTPException(status_code=400, detail="Utterance cannot be None.")

    # Validate the provided state_name
    # if state_name not in state_mapping:
    #     return JSONResponse({"error": "Invalid state name provided."}, status_code=400)

    # If session_id is not provided, generate a new one
    if session_id not in session_store:
        session_id = str(uuid.uuid4())
        initial_state = state_mapping.get(state_name, StatuteState)
        context = Context(session_id, initial_state(), data.get('utterance'))

        session_store[session_id] = context
    else:
        # Use the existing context if session_id already exists
        context = session_store[session_id]
        context.transition_to(state_mapping[state_name]())
        print("==============context=================")
        pprint(context.context_data)

    context.context_data['utterance'] = utterance.replace('\n', '<br/>')
    context.context_data['utterance'] = context.context_data['utterance']
    context = context.handle()

    print(context.context_data)

    return context.context_data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
