from memory import SessionMemory
from backbone import call_llm

class BaseAgent:
    """Base class that all specialized agents inherit from."""
    def __init__(self, role: str, min_words: int, temperature: float):
        self.role = role
        self.min_words = min_words
        self.temperature = temperature

    def run(self, memory: SessionMemory):
        # To be implemented by each specific agent
        pass

class TutorAgent(BaseAgent):
    def __init__(self):
        # Concept Explainer: High temp (0.75) for creative analogies, 80 min words[cite: 1]
        super().__init__(role="Concept Explainer", min_words=80, temperature=0.75)
        
    def run(self, memory: SessionMemory) -> SessionMemory:
        system_prompt = (
            "You are an expert Tutor. Your role is to explain the underlying concepts "
            "related to the student's question clearly and engagingly. Do not solve the problem directly. "
            f"Please write at least {self.min_words} words."
        )
        user_message = f"Topic: {memory.topic}\nStudent Question: {memory.student_question}"
        
        output = call_llm(system_prompt, user_message, self.temperature)
        memory.tutor_output = output
        return memory

class ProblemSolverAgent(BaseAgent):
    def __init__(self):
        # Step-by-Step Solver: Low temp (0.30) for deterministic, verifiable reasoning, 100 min words[cite: 1]
        super().__init__(role="Step-by-Step Solver", min_words=100, temperature=0.30)
        
    def run(self, memory: SessionMemory) -> SessionMemory:
        system_prompt = (
            "You are a rigorous Problem Solver. Using the Tutor's conceptual explanation as context, "
            "provide a deterministic, step-by-step solution to the student's question. Number your steps. "
            f"Please write at least {self.min_words} words."
        )
        user_message = (
            f"Topic: {memory.topic}\n"
            f"Question: {memory.student_question}\n"
            f"Tutor's Context: {memory.tutor_output}"
        )
        
        output = call_llm(system_prompt, user_message, self.temperature)
        memory.solver_output = output
        return memory

class EvaluatorAgent(BaseAgent):
    def __init__(self):
        # Critical Reviewer: Temp (0.40) to balance judgment with nuance, 60 min words[cite: 1]
        super().__init__(role="Critical Reviewer", min_words=60, temperature=0.40)
        
    def run(self, memory: SessionMemory) -> SessionMemory:
        system_prompt = (
            "You are a Critical Evaluator. Review the Problem Solver's step-by-step output. "
            "Identify any logical leaps, errors, or confirm if the solution is completely correct. "
            f"Please write at least {self.min_words} words."
        )
        user_message = (
            f"Original Question: {memory.student_question}\n"
            f"Solver's Output to evaluate: {memory.solver_output}"
        )
        
        output = call_llm(system_prompt, user_message, self.temperature)
        memory.evaluator_output = output
        return memory

class FeedbackAgent(BaseAgent):
    def __init__(self):
        # Feedback Synthesiser: High temp (0.80) for supportive synthesis, 60 min words[cite: 1]
        super().__init__(role="Feedback Synthesiser", min_words=60, temperature=0.80)
        
    def run(self, memory: SessionMemory) -> SessionMemory:
        system_prompt = (
            "You are a Feedback Synthesizer. Combine the Tutor's concepts and the Evaluator's critique "
            "into constructive, easy-to-understand feedback for the student. "
            f"Please write at least {self.min_words} words."
        )
        user_message = (
            f"Tutor's Explanation: {memory.tutor_output}\n"
            f"Evaluator's Critique: {memory.evaluator_output}"
        )
        
        output = call_llm(system_prompt, user_message, self.temperature)
        memory.feedback_output = output
        return memory

class PlannerAgent(BaseAgent):
    def __init__(self):
        # Learning Planner: Moderate temp (0.50) for structured planning, 80 min words[cite: 1]
        super().__init__(role="Learning Planner", min_words=80, temperature=0.50)
        
    def run(self, memory: SessionMemory) -> SessionMemory:
        system_prompt = (
            "You are a Learning Planner. Based on the feedback provided, create a forward-looking "
            "study plan with actionable steps for the student to master this topic. Explicitly address "
            "any errors identified by the Evaluator. "
            f"Please write at least {self.min_words} words."
        )
        user_message = (
            f"Evaluator's Notes: {memory.evaluator_output}\n"
            f"Synthesized Feedback: {memory.feedback_output}"
        )
        
        output = call_llm(system_prompt, user_message, self.temperature)
        memory.planner_output = output
        return memory

class ExternalExaminerAgent(BaseAgent):
    def __init__(self):
        # Strict University Examiner: Low temp (0.20) for uncompromising engineering evaluation
        super().__init__(role="External Examiner", min_words=60, temperature=0.20)
        
    def run(self, memory: SessionMemory) -> SessionMemory:
        system_prompt = (
            "You are a rigorous External Examiner for a technical university. "
            "Your role is to review the Problem Solver's solution and the Planner's study plan. "
            "Grade the overall response on technical accuracy, clarity, and adherence to strict engineering university standards. "
            "Conclude your evaluation with a clear 'PASS' or 'FAIL' verdict and justify your reasoning. "
            f"Please write at least {self.min_words} words."
        )
        user_message = (
            f"Topic: {memory.topic}\n"
            f"Question: {memory.student_question}\n"
            f"Solver's Output: {memory.solver_output}\n"
            f"Proposed Study Plan: {memory.planner_output}"
        )
        
        output = call_llm(system_prompt, user_message, self.temperature)
        memory.examiner_output = output
        return memory