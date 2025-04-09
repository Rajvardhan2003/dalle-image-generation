import os
import sys
import argparse
import openai

defaults = {
    "api_key": os.getenv('OPENAI_API_KEY'),
    "model": "dall-e-3",
    "size": "1024x1024",
    "quality": "standard",
    "number": "1",
}

def validate_and_parse_args(parser):
    args = parser.parse_args()

    for key, value in vars(args).items():
        if not value:
            args.__dict__[key] = parser.get_default(key)

    if not args.api_key:
        parser.error('The --api-key argument is required if OPENAI_API_KEY is not set.')
        if not args.prompt:
    # Try reading from stdin
            if not sys.stdin.isatty():
                args.prompt = sys.stdin.read().strip()

    if not args.prompt:
    # Try from environment variable as last resort
        args.prompt = os.getenv("PROMPT")
    if not args.prompt:
        parser.error('The --prompt argument is required.')
    if not args.number.isdigit():
        parser.error('The --number argument must be a number.')

    args.number = int(args.number)
    return args

def main():
    parser = argparse.ArgumentParser(description="CLI for image generation using DALL-E.")
    parser.add_argument('-k', '--api-key', type=str, default=defaults["api_key"])
    parser.add_argument('-p', '--prompt', type=str)  # <-- NOT REQUIRED HERE
    parser.add_argument('-m', '--model', type=str, default=defaults["model"])
    parser.add_argument('-s', '--size', type=str, default=defaults["size"])
    parser.add_argument('-q', '--quality', type=str, default=defaults["quality"])
    parser.add_argument('-n', '--number', type=str, default=defaults["number"])

    args = validate_and_parse_args(parser)

    client = openai.OpenAI(api_key=args.api_key)

    try:
        response = client.images.generate(
            model=args.model,
            prompt=args.prompt,
            size=args.size,
            quality=args.quality,
            n=args.number
        )
        print([image.url for image in response.data])
    except openai.OpenAIError as e:
        print(f"Image generation error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
