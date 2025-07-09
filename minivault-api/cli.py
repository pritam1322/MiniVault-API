import requests
import argparse

def main():
    parser = argparse.ArgumentParser(description="MiniVault Prompt Generator")
    parser.add_argument("prompt", type=str, help="Prompt to send to the API")
    parser.add_argument("--model", type=str, default="phi", help="Model to use: phi, mistral, falcon")
    parser.add_argument("--stream", action="store_true", help="Stream output token-by-token")
    args = parser.parse_args()

    url = "http://localhost:8000/generate"
    if args.stream:
        url += "/stream"

    payload = {
        "prompt": args.prompt,
        "model": args.model
    }

    headers = {"Content-Type": "application/json"}

    print(f"\n🔍 Sending prompt to {url} using model: {args.model}...\n")

    if args.stream:
        response = requests.post(url, json=payload, stream=True)
        for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
            print(chunk, end="", flush=True)
        print()
    else:
        response = requests.post(url, json=payload)
        print("✅ Response:\n", response.json()["response"])

if __name__ == "__main__":
    main()
