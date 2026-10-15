"""One C1 (original evidence) call with forced structured output via Converse tool use."""
import json

import boto3

from smoke_test import MODEL_ID, PRICE_IN_PER_M, PRICE_OUT_PER_M, PROFILE, REGION

QUESTION = "What year did Marie Curie receive her second Nobel Prize?"

# D1 holds the target fact; D2 and D3 are distractors. Fixed order for this one-off call.
DOCS = [
    ("D1", "Marie Curie received her second Nobel Prize in 1911."),
    ("D2", "Marie Curie was born in Warsaw in 1867 and moved to Paris in 1891 to study physics."),
    ("D3", "The Nobel Prizes are awarded annually; the ceremonies for most categories take place in Stockholm."),
]

INSTRUCTION = (
    "Answer the question below. Give a concise answer: just the value (for example, a year or a name). "
    "Some documents are provided, each with an ID. "
    "If you cite any documents, list their IDs. Submit your response with the submit_answer tool."
)

TOOL_NAME = "submit_answer"
TOOL_CONFIG = {
    "tools": [{
        "toolSpec": {
            "name": TOOL_NAME,
            "description": "Submit the final structured response.",
            "inputSchema": {"json": {
                "type": "object",
                "properties": {
                    "answer": {"type": "string", "description": "Concise answer to the question."},
                    "cited_doc_ids": {
                        "type": "array", "items": {"type": "string"},
                        "description": "IDs of cited documents; empty if none.",
                    },
                    "abstained": {"type": "boolean", "description": "True if you decline to give an answer."},
                    "conflict_noted": {
                        "type": "boolean",
                        "description": "True if you noticed a conflict between sources or with what you know.",
                    },
                },
                "required": ["answer", "cited_doc_ids", "abstained", "conflict_noted"],
            }},
        }
    }],
    "toolChoice": {"tool": {"name": TOOL_NAME}},
}


def build_prompt():
    docs = "\n".join(f"[{doc_id}] {text}" for doc_id, text in DOCS)
    return f"{INSTRUCTION}\n\nDocuments:\n{docs}\n\nQuestion: {QUESTION}"


def main():
    prompt = build_prompt()
    print("--- prompt sent ---")
    print(prompt)

    client = boto3.Session(profile_name=PROFILE, region_name=REGION).client("bedrock-runtime")
    response = client.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"temperature": 0, "maxTokens": 300},
        toolConfig=TOOL_CONFIG,
    )

    blocks = response["output"]["message"]["content"]
    tool_use = next(b["toolUse"] for b in blocks if "toolUse" in b)
    usage = response["usage"]
    cost = (usage["inputTokens"] * PRICE_IN_PER_M + usage["outputTokens"] * PRICE_OUT_PER_M) / 1e6

    print("--- parsed output ---")
    print(json.dumps(tool_use["input"], indent=2))
    print(f"stop_reason: {response['stopReason']}")
    print(f"tokens: in={usage['inputTokens']} out={usage['outputTokens']}")
    print(f"est. cost: ${cost:.6f}")


if __name__ == "__main__":
    main()
