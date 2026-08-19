from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class SessionMemory:
    # 1. Initial Student Inputs
    topic: str
    student_question: str
    student_answer: Optional[str] = None
    curriculum_hints: Optional[str] = None
    
    # 2. Individual Agent Output Slots
    tutor_output: str = ""
    solver_output: str = ""
    evaluator_output: str = ""
    feedback_output: str = ""
    planner_output: str = ""
    examiner_output: str = "" # NEW: Added slot for the External Examiner
    
    # 3. Orchestrator Logs & Emergence Tracking
    pipeline_log: List[str] = field(default_factory=list)
    emergence_positive: List[str] = field(default_factory=list)
    emergence_negative: List[str] = field(default_factory=list)
    emergence_flags: List[str] = field(default_factory=list)