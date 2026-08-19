# 🎓 Multi-Agent Educational AI System

![Architecture](https://img.shields.io/badge/Architecture-Blackboard_Pattern-blue)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Framework](https://img.shields.io/badge/FastAPI_&_Streamlit-Deployed-success)
![LLM](https://img.shields.io/badge/Groq_API-LLaMA_3.3_70B-orange)

## 📌 Project Overview
The **Multi-Agent Educational AI System** is a full-stack, instrumented educational tutoring pipeline. Instead of relying on a single Large Language Model (LLM) prompt, this system orchestrates a sequence of six highly specialized AI personas to tackle complex engineering and technical queries. 

Crucially, this system treats **emergent behaviors**—the unprogrammed coordination or failure patterns that arise when AI agents interact—as a measurable, auditable property. It utilizes a deterministic detection layer to systematically identify whether the agents are synergizing effectively or breaking down into algorithmic echo chambers.

## 🚀 Key Features
*   **Blackboard Architecture:** All agents read from and write to a centralized `SessionMemory` state, ensuring every interaction is explicitly observable.
*   **Role Specialization:** Six distinct agents with optimized temperature settings and minimum-word quality gates:
    *   **Tutor:** Provides theoretical context.
    *   **Problem Solver:** Generates deterministic, step-by-step technical solutions.
    *   **Evaluator:** Critiques the solver's logic and identifies edge cases.
    *   **Feedback:** Synthesizes upstream interactions into constructive guidance.
    *   **Planner:** Creates a forward-looking study plan.
    *   **External Examiner:** Issues a strict PASS/FAIL university-level verdict.
*   **Zero-Cost Emergence Detection:** A programmatic orchestration layer that uses mathematical keyword overlap and regex scanning to detect:
    *   `[POSITIVE]` Well-aligned reasoning and insightful synthesis.
    *   `[NEGATIVE]` Topic drift, blind evaluator agreement (rubber-stamping), and quality gate failures.
*   **Decoupled Deployment:** Frontend hosted on Streamlit Community Cloud and backend APIs hosted on Render.

## 🛠️ Technology Stack
*   **Frontend:** Streamlit
*   **Backend:** Python, FastAPI, Uvicorn, Pydantic
*   **LLM Inference:** Groq API (LLaMA 3.3 70B Versatile)
*   **Detection Engine:** Custom Python Rule-Based Regex & Math Scanners

## 📁 Repository Structure
```text
📦 emergent-ai-system
 ┣ 📜 app.py               # Streamlit frontend UI & JSON parser
 ┣ 📜 main.py              # FastAPI backend router & endpoints
 ┣ 📜 orchestrator.py      # Pipeline logic, quality gates, & emergence detection
 ┣ 📜 agents.py            # BaseAgent class and the 6 specialized agent personas
 ┣ 📜 memory.py            # SessionMemory dataclass (The Blackboard)
 ┣ 📜 backbone.py          # Groq API inference wrapper
 ┗ 📜 requirements.txt     # Project dependencies
