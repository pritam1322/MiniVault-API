from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from model import generate_response, get_model_pipeline
from datetime import datetime
from pathlib import Path
import json
import torch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str
    model: str 

@app.post("/generate")
async def generate_text(data: PromptRequest):
    try:
        response = generate_response(data.prompt, data.model)
    except ValueError as e:
        return {"error": str(e)}


    log_path = Path("logs/log.jsonl")
    log_path.parent.mkdir(exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "prompt": data.prompt,
            "model": data.model,
            "response": response
        }) + "\n")

    return {"response": response}

@app.post("/generate/stream")
async def stream_tokens(data: PromptRequest):
    try:
        components = get_model_pipeline(data.model)
        tokenizer = components["tokenizer"]
        model = components["model"]
    except ValueError as e:
        return {"error": str(e)}

    prompt = data.prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs["input_ids"]

    max_tokens = 50
    full_response = []

    def stream_response():
        nonlocal input_ids
        output_ids = input_ids

        for _ in range(max_tokens):
            output = model.generate(
                output_ids,
                max_new_tokens=1,
                do_sample=True
            )
            new_token_id = output[0, -1].unsqueeze(0)
            token_text = tokenizer.decode(new_token_id, skip_special_tokens=True)
            full_response.append(token_text)  # <-- collect for logging
            yield token_text
            output_ids = torch.cat([output_ids, new_token_id.unsqueeze(0)], dim=1)


    async def wrapped_stream():
        for chunk in stream_response():
            yield chunk

        log_path = Path("logs/log.jsonl")
        log_path.parent.mkdir(exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "prompt": data.prompt,
                "model": data.model,
                "response": "".join(full_response)
            }) + "\n")

    return StreamingResponse(wrapped_stream(), media_type="text/plain")
