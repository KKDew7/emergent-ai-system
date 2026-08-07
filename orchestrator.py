# import re
# from memory import SessionMemory
# from agents import TutorAgent, ProblemSolverAgent, EvaluatorAgent, FeedbackAgent, PlannerAgent

# MAX_RETRIES = 2 # As specified in the methodology

# def quality_gate(output: str, min_words: int) -> bool:
#     """Verifies minimum word count and scans for red-flag patterns."""
#     word_count = len(output.split())
#     if word_count < min_words:
#         return False
        
#     # Red-flag regular expressions
#     red_flags = [r"\bI don't know\b", r"\bcannot help\b", r"\brefuse\b", r"N/A", r"Exception"]
#     for flag in red_flags:
#         if re.search(flag, output, re.IGNORECASE):
#             return False
            
#     return True

# def run_agent_with_retries(agent, memory: SessionMemory, output_attr: str) -> bool:
#     """Runs an agent and retries up to MAX_RETRIES if the quality gate fails."""
#     for attempt in range(MAX_RETRIES + 1):
#         memory = agent.run(memory)
#         output = getattr(memory, output_attr)
        
#         if quality_gate(output, agent.min_words):
#             memory.pipeline_log.append(f"{agent.role} succeeded on attempt {attempt + 1}")
#             return True
            
#     memory.pipeline_log.append(f"{agent.role} failed quality gate after {MAX_RETRIES} retries")
#     memory.emergence_negative.append("Agent quality gate failure") # Negative emergence
#     return False

# def detect_emergence(memory: SessionMemory):
#     """Applies rule-based emergence detection covering behavioural patterns."""
#     topic_keywords = set(word.lower() for word in memory.topic.split() if len(word) >= 5)
    
#     # 1. Topic Drift (Negative) & Well-aligned solver (Positive)
#     solver_words = set(memory.solver_output.lower().split())
#     overlap = len(topic_keywords.intersection(solver_words))
#     if len(topic_keywords) > 0:
#         overlap_ratio = overlap / len(topic_keywords)
#         if overlap_ratio < 0.20:
#             memory.emergence_negative.append("Topic drift")
#         elif overlap_ratio >= 0.50:
#             memory.emergence_positive.append("Well-aligned solver output")

#     # 2. Blind evaluator agreement (Negative)
#     if re.search(r"CORRECT", memory.evaluator_output) and not re.search(r"error|issue|incorrect", memory.evaluator_output, re.IGNORECASE):
#         memory.emergence_negative.append("Blind evaluator agreement")

#     # 3. Insightful agent response (Positive)
#     insight_regex = r"excellent|deep insight|brilliant"
#     if re.search(insight_regex, memory.tutor_output + memory.feedback_output, re.IGNORECASE):
#         memory.emergence_positive.append("Insightful agent response")

# def run_pipeline(memory: SessionMemory) -> SessionMemory:
#     """Coordinates the 5 specialized agents and runs emergence detection."""
#     agents = [
#         (TutorAgent(), "tutor_output"),
#         (ProblemSolverAgent(), "solver_output"),
#         (EvaluatorAgent(), "evaluator_output"),
#         (FeedbackAgent(), "feedback_output"),
#         (PlannerAgent(), "planner_output")
#     ]
    
#     for agent, attr in agents:
#         run_agent_with_retries(agent, memory, attr)
        
#     detect_emergence(memory)
    
#     # Compile final flags combining positive and negative behaviors
#     memory.emergence_flags = [f"[POSITIVE] {flag}" for flag in memory.emergence_positive] + \
#                              [f"[NEGATIVE] {flag}" for flag in memory.emergence_negative]
                             
#     return memory

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
    memory.emergence_negative.append("Agent quality gate failure") # Negative emergence
    return False

def detect_emergence(memory: SessionMemory):
    """Applies rule-based emergence detection covering behavioural patterns and generates detailed explanations."""
    topic_keywords = set(word.lower() for word in memory.topic.split() if len(word) >= 5)
    
    # 1. Topic Drift (Negative) & Well-aligned solver (Positive)
    solver_words = set(memory.solver_output.lower().split())
    overlap = len(topic_keywords.intersection(solver_words))
    
    if len(topic_keywords) > 0:
        overlap_ratio = overlap / len(topic_keywords)
        if overlap_ratio < 0.20:
            missing_words = list(topic_keywords - solver_words)[:3]
            explanation = f"Topic drift: Only {overlap_ratio*100:.0f}% keyword overlap detected. The solver missed core concepts like: {missing_words}."
            memory.emergence_negative.append(explanation)
        elif overlap_ratio >= 0.50:
            explanation = f"Well-aligned solver output: Excellent focus, {overlap_ratio*100:.0f}% of the original topic keywords were utilized in the reasoning."
            memory.emergence_positive.append(explanation)

    # 2. Blind evaluator agreement (Negative)
    if re.search(r"CORRECT", memory.evaluator_output) and not re.search(r"error|issue|incorrect", memory.evaluator_output, re.IGNORECASE):
        explanation = "Blind evaluator agreement: The Evaluator endorsed the solution without highlighting any technical nuances, edge cases, or potential weaknesses."
        memory.emergence_negative.append(explanation)

    # 3. Insightful agent response (Positive)
    insight_regex = r"excellent|deep insight|brilliant"
    if re.search(insight_regex, memory.tutor_output + memory.feedback_output, re.IGNORECASE):
        explanation = "Insightful agent response: The system organically generated high-level synthesis and praised the structural reasoning of previous agents."
        memory.emergence_positive.append(explanation)

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
        
    detect_emergence(memory)
    
    # Compile final flags combining positive and negative behaviors
    memory.emergence_flags = [f"[POSITIVE] {flag}" for flag in memory.emergence_positive] + \
                             [f"[NEGATIVE] {flag}" for flag in memory.emergence_negative]
                             
    return memory