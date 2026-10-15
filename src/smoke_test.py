"""Smoke test: one question, one Bedrock Converse call, print answer + token usage."""
import boto3

PROFILE = "xai-bedrock"
REGION = "us-east-1"
# Inference profile: the plain ID fails with on-demand throughput.
MODEL_ID = "us.anthropic.claude-sonnet-4-6"
QUESTION = "What year did Marie Curie receive her second Nobel Prize?"

# USD per million tokens, us. inference profile (~10% above the $3/$15 base rate).
# Source: AWS Bedrock pricing page, as checked by the user.
PRICE_IN_PER_M = 3.30
PRICE_OUT_PER_M = 16.50


def call(client, model_id):
    return client.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": QUESTION}]}],
        inferenceConfig={"temperature": 0, "maxTokens": 200},
    )


def main():
    session = boto3.Session(profile_name=PROFILE, region_name=REGION)
    client = session.client("bedrock-runtime")

    response = call(client, MODEL_ID)

    answer = response["output"]["message"]["content"][0]["text"]
    usage = response["usage"]
    cost = (usage["inputTokens"] * PRICE_IN_PER_M + usage["outputTokens"] * PRICE_OUT_PER_M) / 1e6

    print(f"model:  {MODEL_ID}")
    print(f"answer: {answer}")
    print(f"tokens: in={usage['inputTokens']} out={usage['outputTokens']}")
    print(f"est. cost: ${cost:.6f}")


if __name__ == "__main__":
    main()
