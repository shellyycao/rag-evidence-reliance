"""Frozen prompt template, tool schema and inference settings. Any change requires a new PROMPT_VERSION."""

PROMPT_VERSION = "v1"

INSTRUCTION = (
    "Answer the question below. Give a concise answer: just the value (for example, a year or a name). "
    "If you use any documents, cite their IDs. "
    "Submit your response with the submit_answer tool."
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
                        "description": "IDs of cited documents, for example \"Doc 1\"; empty if none.",
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

# Fixed for every call; extended thinking is not enabled.
INFERENCE_CONFIG = {"temperature": 0, "maxTokens": 300}


def build_prompt(question, docs):
    """docs: list of {"display_id": "Doc 1", "text": ...} in display order; empty for C0."""
    parts = [INSTRUCTION]
    if docs:
        parts.append("Documents:\n" + "\n".join(f"[{d['display_id']}] {d['text']}" for d in docs))
    parts.append(f"Question: {question}")
    return "\n\n".join(parts)
