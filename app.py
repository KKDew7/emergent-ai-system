# import streamlit as st
# import requests

# # --- 1. UI Configuration ---
# st.set_page_config(page_title="Educational AI System", page_icon="🎓", layout="wide")
# st.title("🎓 Multi-Agent Educational Assistant")

# # --- 2. Sidebar Settings ---
# with st.sidebar:
#     st.header("⚙️ System Configuration")
#     topic = st.text_input("Current Study Topic:", value="Machine Learning")
#     st.markdown("---")
#     if st.button("🗑️ Clear Chat History"):
#         st.session_state.messages = []
#         st.rerun()

# # --- 3. Initialize Session State for Chat History ---
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # --- 4. Render Existing Chat History ---
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])
#         if "agent_data" in msg and msg["agent_data"]:
#             with st.expander("🔍 View Multi-Agent Breakdown"):
#                 st.json(msg["agent_data"])

# # --- 5. Handle New User Input ---
# if question := st.chat_input("Enter your specific question..."):
    
#     st.session_state.messages.append({"role": "user", "content": question})
#     with st.chat_message("user"):
#         st.markdown(question)

#     with st.chat_message("assistant"):
#         with st.status("Initiating multi-agent pipeline...", expanded=True) as status:
#             st.write("🕵️ Agents are processing the request...")
            
#             try:
#                 # Connected to your specific live Render backend
#                 API_URL = "https://emergent-ai-system.onrender.com/run-session"
                
#                 response = requests.post(
#                     API_URL, 
#                     json={"topic": topic, "question": question}
#                 )
                
#                 if response.status_code == 200:
#                     data = response.json()
                    
#                     feedback_text = data.get("feedback_output", "No feedback generated.")
#                     planner_text = data.get("planner_output", "No plan generated.")
#                     examiner_text = data.get("examiner_output", "No examiner verdict.")
                    
#                     # Combine Feedback, Planner, and the new Examiner output for the main chat UI
#                     full_response = (
#                         f"**Synthesized Feedback:**\n{feedback_text}\n\n"
#                         f"**Study Plan:**\n{planner_text}\n\n"
#                         f"--- \n"
#                         f"🏛️ **University Examiner Verdict:**\n{examiner_text}"
#                     )
                    
#                     # Collect all raw agent outputs and flags for the expander
#                     agent_metrics = {
#                         "Tutor Output": data.get("tutor_output"),
#                         "Solver Output": data.get("solver_output"),
#                         "Evaluator Output": data.get("evaluator_output"),
#                         "Examiner Output": data.get("examiner_output"),
#                         "Emergence Flags": data.get("emergence_flags", []),
#                         "Pipeline Logs": data.get("pipeline_log", [])
#                     }
                    
#                     status.update(label="Response finalized!", state="complete", expanded=False)
#                 else:
#                     full_response = f"Error: The backend encountered an issue (Status {response.status_code})."
#                     agent_metrics = {"error_details": response.text}
#                     status.update(label="Pipeline failed.", state="error", expanded=False)
                    
#             except requests.exceptions.ConnectionError:
#                 full_response = "Error: Cannot connect to the FastAPI backend. Is uvicorn running?"
#                 agent_metrics = None
#                 status.update(label="Connection failed.", state="error", expanded=False)

#         # Display the final answer
#         st.markdown(full_response)
        
#         # Display the raw agent data inside an expander
#         if agent_metrics:
#             with st.expander("🔍 View Multi-Agent Breakdown (Flags & Raw Outputs)"):
#                 st.write("**System Analysis & Emergence Flags:**")
                
#                 # Render the explanations with color coding based on the tag
#                 for flag in agent_metrics.get("Emergence Flags", []):
#                     if "[POSITIVE]" in flag:
#                         st.success(flag)
#                     elif "[NEGATIVE]" in flag:
#                         st.error(flag)
#                     else:
#                         st.info(flag) # Catches the new [INFO] explanations for neutral events
                        
#                 st.markdown("---")
#                 st.write("**Pipeline Execution Logs:**")
#                 for log in agent_metrics.get("Pipeline Logs", []):
#                     st.code(log)
                    
#                 st.write("**Raw Agent Outputs:**")
#                 st.json(agent_metrics)
                
#         # Save the assistant's response to the chat history
#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": full_response,
#             "agent_data": agent_metrics
#         })
import streamlit as st
import requests

# --- 1. UI Configuration ---
st.set_page_config(page_title="Educational AI System", page_icon="🎓", layout="wide")
st.title("🎓 Multi-Agent Educational Assistant")

# --- 2. Sidebar Settings ---
with st.sidebar:
    st.header("⚙️ System Configuration")
    topic = st.text_input("Current Study Topic:", value="Machine Learning")
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- 3. Initialize Session State for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. Render Existing Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "agent_data" in msg and msg["agent_data"]:
            with st.expander("🔍 View Multi-Agent Breakdown"):
                st.json(msg["agent_data"])

# --- 5. Handle New User Input ---
if question := st.chat_input("Enter your specific question..."):
    
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.status("Initiating multi-agent pipeline...", expanded=True) as status:
            st.write("🕵️ Agents are processing the request...")
            
            try:
                # Connected to your specific live Render backend
                API_URL = "https://emergent-ai-system.onrender.com/run-session"
                
                response = requests.post(
                    API_URL, 
                    json={"topic": topic, "question": question}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    tutor_text = data.get("tutor_output", "No context generated.")
                    solver_text = data.get("solver_output", "No solution generated.")
                    feedback_text = data.get("feedback_output", "No feedback generated.")
                    planner_text = data.get("planner_output", "No plan generated.")
                    examiner_text = data.get("examiner_output", "No examiner verdict.")
                    
                    # We now include the Tutor and Solver at the very top so it answers the question first!
                    full_response = (
                        f"### 📚 Tutor Introduction\n{tutor_text}\n\n"
                        f"### ⚙️ Technical Solution\n{solver_text}\n\n"
                        f"---\n"
                        f"**🗣️ Synthesized Feedback:**\n{feedback_text}\n\n"
                        f"**📅 Study Plan:**\n{planner_text}\n\n"
                        f"---\n"
                        f"🏛️ **University Examiner Verdict:**\n{examiner_text}"
                    )
                    
                    # Collect all raw agent outputs and flags for the expander
                    agent_metrics = {
                        "Tutor Output": data.get("tutor_output"),
                        "Solver Output": data.get("solver_output"),
                        "Evaluator Output": data.get("evaluator_output"),
                        "Examiner Output": data.get("examiner_output"),
                        "Emergence Flags": data.get("emergence_flags", []),
                        "Pipeline Logs": data.get("pipeline_log", [])
                    }
                    
                    status.update(label="Response finalized!", state="complete", expanded=False)
                else:
                    full_response = f"Error: The backend encountered an issue (Status {response.status_code})."
                    agent_metrics = {"error_details": response.text}
                    status.update(label="Pipeline failed.", state="error", expanded=False)
                    
            except requests.exceptions.ConnectionError:
                full_response = "Error: Cannot connect to the FastAPI backend. Is uvicorn running?"
                agent_metrics = None
                status.update(label="Connection failed.", state="error", expanded=False)

        # Display the final answer
        st.markdown(full_response)
        
        # Display the raw agent data inside an expander
        if agent_metrics:
            with st.expander("🔍 View Multi-Agent Breakdown (Flags & Raw Outputs)"):
                st.write("**System Analysis & Emergence Flags:**")
                
                # Render the explanations with color coding based on the tag
                for flag in agent_metrics.get("Emergence Flags", []):
                    if "[POSITIVE]" in flag:
                        st.success(flag)
                    elif "[NEGATIVE]" in flag:
                        st.error(flag)
                    else:
                        st.info(flag) # Catches the new [INFO] explanations for neutral events
                        
                st.markdown("---")
                st.write("**Pipeline Execution Logs:**")
                for log in agent_metrics.get("Pipeline Logs", []):
                    st.code(log)
                    
                st.write("**Raw Agent Outputs:**")
                st.json(agent_metrics)
                
        # Save the assistant's response to the chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response,
            "agent_data": agent_metrics
        })