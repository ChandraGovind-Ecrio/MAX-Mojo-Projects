# MAX structured incident copilot

This project demonstrates a credible application pattern for MAX: an application sends a bounded incident record to a local model server and expects a **structured triage response**, not open-ended chatbot prose. The result is designed to help an on-call engineer quickly see customer impact, probable subsystem, evidence, confidence, and safe next actions.

## What the project does

`incident_copilot.py` reads a JSON incident record, builds a constrained prompt, calls MAX's OpenAI-compatible `/v1/chat/completions` endpoint, and validates that the response contains the required JSON fields. The included [sample incident](sample_incident.json) represents a rise in packet loss and jitter for a media region.

```bash
# Inspect the request without downloading a model or calling a server.
python3 incident_copilot.py --dry-run
```

The dry run lets security, reliability, and product teams review exactly what leaves the application boundary before an LLM is introduced.

## Why MAX is involved

Python owns the product workflow: read input, construct the request, apply a timeout, validate the response, and decide what to display or persist. MAX owns the costly model-execution path: model loading, tensor execution, memory management, scheduling, and hardware backend selection. This separation avoids embedding GPU/kernel work in application code.

| Layer | Responsibility |
|---|---|
| `incident_copilot.py` | Input validation, prompt construction, HTTP request, response-schema validation, and safe failure messages. |
| MAX server | Runs the model and exposes an OpenAI-compatible API. |
| Model | Converts evidence into a proposed, structured triage assessment. |
| Human/on-call system | Reviews the assessment and performs any operational action. |

The model is not granted access to production systems and cannot remediate an incident. Treat its response as a draft for review, not an authoritative diagnosis.

## Run against MAX

This project has no model installed yet—models are large and the right choice depends on available memory and policy. When you are ready, use a model supported by MAX from Modular's [supported-model list](https://docs.modular.com/max/model-formats).

```bash
# In this folder, create the isolated MAX environment once.
../.tooling/pixi/pixi init .
../.tooling/pixi/pixi add modular

# Terminal 1: choose a supported model appropriate for this machine.
../.tooling/pixi/pixi run max serve --model modularai/Llama-3.1-8B-Instruct-GGUF

# Terminal 2: submit the included incident record.
python3 incident_copilot.py
```

The client assumes MAX is reachable on `http://127.0.0.1:8000`. Set `MAX_URL` or `MAX_MODEL` in the environment to override the endpoint or model name.

## Why this is more than a chatbot demo

The company-relevant pieces are the contract and safeguards: a bounded input record, a response schema, deterministic validation, timeouts, a dry-run review mode, and a clear human-approval boundary. Natural next steps include adding redaction, audit logs, retrieval over approved runbooks, evaluation cases, and integration with an incident-management system.

## Plain English: what is the point, and what does MAX add?

When a service has a problem, engineers may have a pile of metrics and notes to read. This project sends a small incident summary to an AI model and asks it to organize the evidence into a consistent report: how serious it may be, which area to inspect, and what safe checks could come next. MAX is the engine that loads and runs the AI model; the Python file is the small program that sends the request and checks the answer.

This can help an engineer get oriented, but the model can be wrong. The sample is fictional, and this project has not yet run a model or connected to MAX; its dry-run only shows the request. MAX's practical benefit is that it provides a model-serving runtime and can use supported hardware backends without the application author writing GPU kernels. This example does not compare MAX's speed or cost with another inference server. In a company, real incident data should only be sent after privacy, access, retention, and model-quality requirements are reviewed, and a person should verify any suggested action.
