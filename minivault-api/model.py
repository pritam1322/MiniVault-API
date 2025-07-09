from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from typing import Dict

# Cache to avoid reloading models
PIPELINE_CACHE: Dict[str, dict] = {}

def get_model_pipeline(model_name: str):
    if model_name in PIPELINE_CACHE:
        return PIPELINE_CACHE[model_name]

    model_map = {
        "phi": "microsoft/phi-2",
        "mistral": "mistralai/Mistral-7B-Instruct-v0.1",
        "falcon": "tiiuae/falcon-7b-instruct",
    }

    if model_name not in model_map:
        raise ValueError(f"Unsupported model: {model_name}")

    model_id = model_map[model_name]

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)

    # Create pipeline
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    # Cache all 3
    PIPELINE_CACHE[model_name] = {
        "pipe": pipe,
        "tokenizer": tokenizer,
        "model": model
    }

    return PIPELINE_CACHE[model_name]

def generate_response(prompt: str, model_name: str) -> str:
    components = get_model_pipeline(model_name)
    pipe = components["pipe"]

    result = pipe(prompt, max_new_tokens=128, do_sample=True, temperature=0.7)
    return result[0]['generated_text'].strip()
