import streamlit as st
from agents.sourcing_agent import SourcingAgent
from agents.screening_agent import ScreeningAgent
from agents.engagement_agent import EngagementAgent
from agents.scheduling_agent import SchedulingAgent
import os
from dotenv import load_dotenv
import PyPDF2
import io

# Load environment variables
load_dotenv()

# Initialize agents
@st.cache_resource
def get_agents():
    return {
        "sourcing": SourcingAgent(),
        "screening": ScreeningAgent(),
        "engagement": EngagementAgent(),
        "scheduling": SchedulingAgent()
    }

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_file(uploaded_file):
    """Extract text from either a text or PDF file"""
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    else:
        # Try different encodings for text files
        encodings = ['utf-8', 'latin-1', 'iso-8859-1']
        for encoding in encodings:
            try:
                return uploaded_file.read().decode(encoding)
            except UnicodeDecodeError:
                continue
        # If all encodings fail, try with error handling
        return uploaded_file.read().decode('utf-8', errors='replace')

def main():
    st.set_page_config(
        page_title="Intelligent Talent Acquisition Assistant",
        page_icon="🤖",
        layout="wide"
    )

    st.title("🤖 Intelligent Talent Acquisition Assistant")
    st.markdown("---")

    # Initialize session state
    if "current_candidate" not in st.session_state:
        st.session_state.current_candidate = None
    if "current_job" not in st.session_state:
        st.session_state.current_job = None

    # Get agents
    agents = get_agents()

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Job Posting", "Candidate Sourcing", "Resume Screening", 
         "Candidate Engagement", "Interview Scheduling", "Dashboard"]
    )

    if page == "Job Posting":
        st.header("📝 Post a New Job")
        with st.form("job_posting_form"):
            job_title = st.text_input("Job Title")
            job_description = st.text_area("Job Description")
            requirements = st.text_area("Requirements")
            
            if st.form_submit_button("Post Job"):
                if job_title and job_description and requirements:
                    st.session_state.current_job = {
                        "title": job_title,
                        "description": job_description,
                        "requirements": requirements
                    }
                    st.success("Job posted successfully!")

    elif page == "Candidate Sourcing":
        st.header("🔍 Source Candidates")
        if st.session_state.current_job:
            st.subheader(f"Current Job: {st.session_state.current_job['title']}")
            
            if st.button("Find Candidates"):
                with st.spinner("Searching for candidates..."):
                    results = agents["sourcing"].source_candidates(
                        st.session_state.current_job["description"],
                        st.session_state.current_job["requirements"]
                    )
                    
                    st.subheader("Search Queries")
                    st.write(results["search_queries"])
                    
                    st.subheader("Found Candidates")
                    for candidate in results["candidates"]:
                        with st.expander(f"Candidate {candidate['id']}"):
                            st.write(candidate)
        else:
            st.warning("Please post a job first!")

    elif page == "Resume Screening":
        st.header("📋 Screen Resumes")
        if st.session_state.current_job:
            uploaded_file = st.file_uploader("Upload Resume", type=["txt", "pdf"])
            
            if uploaded_file:
                try:
                    resume_text = extract_text_from_file(uploaded_file)
                    if st.button("Screen Resume"):
                        with st.spinner("Screening resume..."):
                            analysis = agents["screening"].screen_candidate(
                                resume_text,
                                st.session_state.current_job["description"]
                            )
                            
                            st.subheader("Screening Results")
                            st.write(f"Recommendation: {analysis['recommendation']}")
                            
                            st.subheader("Key Points")
                            for key, value in analysis["key_points"].items():
                                st.write(f"**{key.replace('_', ' ').title()}**: {value}")
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
        else:
            st.warning("Please post a job first!")

    elif page == "Candidate Engagement":
        st.header("💬 Engage with Candidates")
        candidate_id = st.text_input("Candidate ID")
        
        if candidate_id:
            if "messages" not in st.session_state:
                st.session_state.messages = []
            
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
            
            if prompt := st.chat_input("Type your message..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)
                
                with st.spinner("Generating response..."):
                    response = agents["engagement"].handle_candidate_response(
                        candidate_id,
                        prompt
                    )
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    with st.chat_message("assistant"):
                        st.write(response)

    elif page == "Interview Scheduling":
        st.header("📅 Schedule Interviews")
        candidate_id = st.text_input("Candidate ID")
        
        if candidate_id:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Candidate Availability")
                candidate_availability = {
                    "Monday": st.multiselect("Monday", ["9AM-12PM", "1PM-5PM"]),
                    "Tuesday": st.multiselect("Tuesday", ["9AM-12PM", "1PM-5PM"]),
                    "Wednesday": st.multiselect("Wednesday", ["9AM-12PM", "1PM-5PM"]),
                    "Thursday": st.multiselect("Thursday", ["9AM-12PM", "1PM-5PM"]),
                    "Friday": st.multiselect("Friday", ["9AM-12PM", "1PM-5PM"])
                }
            
            with col2:
                st.subheader("Interviewer Availability")
                interviewer_availability = {
                    "Monday": st.multiselect("Monday (Interviewer)", ["9AM-12PM", "1PM-5PM"]),
                    "Tuesday": st.multiselect("Tuesday (Interviewer)", ["9AM-12PM", "1PM-5PM"]),
                    "Wednesday": st.multiselect("Wednesday (Interviewer)", ["9AM-12PM", "1PM-5PM"]),
                    "Thursday": st.multiselect("Thursday (Interviewer)", ["9AM-12PM", "1PM-5PM"]),
                    "Friday": st.multiselect("Friday (Interviewer)", ["9AM-12PM", "1PM-5PM"])
                }
            
            if st.button("Find Available Slots"):
                with st.spinner("Finding available time slots..."):
                    slots = agents["scheduling"].find_available_slots(
                        candidate_availability,
                        interviewer_availability
                    )
                    
                    st.subheader("Available Time Slots")
                    if slots:
                        # Create a form for slot selection
                        with st.form("slot_selection_form"):
                            selected_slot = st.radio(
                                "Select a time slot:",
                                options=[slot['time'] for slot in slots],
                                format_func=lambda x: x
                            )
                            
                            if st.form_submit_button("Schedule Interview"):
                                # Find the selected slot object
                                selected_slot_obj = next(
                                    slot for slot in slots if slot['time'] == selected_slot
                                )
                                
                                interview = agents["scheduling"].schedule_interview(
                                    candidate_id,
                                    selected_slot_obj
                                )
                                st.success(f"Interview scheduled for {interview['time']}")
                    else:
                        st.info("No available time slots found. Please adjust the availability.")

    elif page == "Dashboard":
        st.header("📊 Recruitment Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Current Job")
            if st.session_state.current_job:
                st.write(f"**Title**: {st.session_state.current_job['title']}")
                st.write("**Description**:")
                st.write(st.session_state.current_job['description'])
            else:
                st.warning("No job posted yet")
        
        with col2:
            st.subheader("Scheduled Interviews")
            interviews = agents["scheduling"].get_scheduled_interviews()
            if interviews:
                for interview in interviews:
                    st.write(f"**Candidate {interview['candidate_id']}**: {interview['time']}")
            else:
                st.info("No interviews scheduled yet")

if __name__ == "__main__":
    main() 