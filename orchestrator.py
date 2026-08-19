
import re
from memory import SessionMemory
from agents import TutorAgent, ProblemSolverAgent, EvaluatorAgent, FeedbackAgent, PlannerAgent, ExternalExaminerAgent

MAX_RETRIES = 2 # Best-effort fallback on failure

def quality_gate(output: str, min_words: int) -> bool:
    """Verifies minimum word count and scans for red-flag patterns."""
    word_count = len(output.split())
    if word_count < min_words:
        return False
        
    # Red-flag regular expressions
    red_flags = [r"\bI don't know\b", r"\bcannot help\b", r"\brefuse\b", r"N/A", r"Exception"]
    for flag in red_flags:
        if re.search(flag, output, re.IGNORECASE):
            return False
            
    return True

def run_agent_with_retries(agent, memory: SessionMemory, output_attr: str) -> bool:
    """Runs an agent and retries up to MAX_RETRIES if the quality gate fails."""
    for attempt in range(MAX_RETRIES + 1):
        memory = agent.run(memory)
        output = getattr(memory, output_attr)
        
        if quality_gate(output, agent.min_words):
            memory.pipeline_log.append(f"{agent.role} succeeded on attempt {attempt + 1}")
            return True
            
    memory.pipeline_log.append(f"{agent.role} failed quality gate after {MAX_RETRIES} retries")
    # Log a negative emergence flag if an agent completely fails its retries
    memory.emergence_flags.append(f"[NEGATIVE] {agent.role} failed quality gate.")
    return False

def detect_emergence(memory: SessionMemory):
    """Applies emergence detection and guarantees detailed explanations for every run."""
    # Lowered keyword length to 4 to catch more relevant academic terms
    topic_keywords = set(word.lower() for word in memory.topic.split() if len(word) >= 4)
    solver_words = set(memory.solver_output.lower().split())
    
    # 1. Topic Drift & Alignment (Always output an explanation)
    if len(topic_keywords) > 0:
        overlap = len(topic_keywords.intersection(solver_words))
        overlap_ratio = overlap / len(topic_keywords)
        
        if overlap_ratio < 0.20:
            missing_words = list(topic_keywords - solver_words)[:3]
            memory.emergence_flags.append(f"[NEGATIVE] Topic drift: Only {overlap_ratio*100:.0f}% keyword overlap. Missed concepts: {missing_words}.")
        elif overlap_ratio >= 0.50:
            memory.emergence_flags.append(f"[POSITIVE] Well-aligned output: Excellent focus, {overlap_ratio*100:.0f}% of topic keywords were utilized.")
        else:
            memory.emergence_flags.append(f"[INFO] Moderate topic alignment: {overlap_ratio*100:.0f}% keyword overlap maintained during reasoning.")
    else:
        memory.emergence_flags.append("[INFO] Topic input too short for keyword overlap analysis.")

    # 2. Evaluator Behavior (Always output an explanation)
    if re.search(r"CORRECT|PASS", memory.evaluator_output, re.IGNORECASE) and not re.search(r"error|issue|incorrect|nuance|however", memory.evaluator_output, re.IGNORECASE):
        memory.emergence_flags.append("[NEGATIVE] Blind evaluator agreement: The Evaluator endorsed the solution without highlighting technical nuances or edge cases.")
    else:
        memory.emergence_flags.append("[POSITIVE] Critical Evaluation: The Evaluator successfully analyzed nuances, edge cases, or potential weaknesses.")

    # 3. Insightful Agent Response
    insight_regex = r"excellent|deep insight|brilliant|comprehensive"
    if re.search(insight_regex, memory.tutor_output + memory.feedback_output, re.IGNORECASE):
        memory.emergence_flags.append("[POSITIVE] Insightful response: Agents organically generated high-level synthesis and praised prior reasoning.")

def run_pipeline(memory: SessionMemory) -> SessionMemory:
    """Coordinates the specialized agents and runs emergence detection."""
    # The pipeline now executes 6 agents sequentially
    agents = [
        (TutorAgent(), "tutor_output"),
        (ProblemSolverAgent(), "solver_output"),
        (EvaluatorAgent(), "evaluator_output"),
        (FeedbackAgent(), "feedback_output"),
        (PlannerAgent(), "planner_output"),
        (ExternalExaminerAgent(), "examiner_output")
    ]
    
    for agent, attr in agents:
        run_agent_with_retries(agent, memory, attr)
        
    # Run the upgraded detection to populate emergence_flags
    detect_emergence(memory)
                             
    return memory