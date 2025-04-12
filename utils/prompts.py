from langchain.prompts import PromptTemplate

# Sourcing Agent Prompts
SOURCING_PROMPT = PromptTemplate(
    input_variables=["job_description", "requirements"],
    template="""You are an expert talent sourcing agent. Analyze the following job description and requirements to find suitable candidates:
    
    Job Description: {job_description}
    Requirements: {requirements}
    
    Based on this information, create a detailed search query that will help find the most suitable candidates. Consider:
    1. Required skills and experience
    2. Industry-specific keywords
    3. Location preferences
    4. Education requirements
    
    Return a structured search query that can be used across multiple platforms."""
)

# Screening Agent Prompts
SCREENING_PROMPT = PromptTemplate(
    input_variables=["resume", "job_description"],
    template="""You are an expert resume screening agent. Analyze the following resume against the job description:
    
    Resume: {resume}
    Job Description: {job_description}
    
    Evaluate the candidate based on:
    1. Skills match
    2. Experience relevance
    3. Education requirements
    4. Cultural fit indicators
    
    Provide a detailed analysis and a recommendation (Strong Match, Potential Match, or Not a Match) with specific reasons."""
)

# Engagement Agent Prompts
ENGAGEMENT_PROMPT = PromptTemplate(
    input_variables=["candidate_info", "job_details"],
    template="""You are an expert candidate engagement agent. Based on the following information:
    
    Candidate Info: {candidate_info}
    Job Details: {job_details}
    
    Create a personalized outreach message that:
    1. Highlights relevant aspects of the candidate's profile
    2. Explains why they might be interested in this opportunity
    3. Maintains a professional yet engaging tone
    4. Includes a clear call to action
    
    Return a well-structured message that can be sent to the candidate."""
)

# Scheduling Agent Prompts
SCHEDULING_PROMPT = PromptTemplate(
    input_variables=["candidate_availability", "interviewer_availability"],
    template="""You are an expert scheduling agent. Based on the following availability:
    
    Candidate Availability: {candidate_availability}
    Interviewer Availability: {interviewer_availability}
    
    Find the best possible time slots for the interview that:
    1. Work for both parties
    2. Consider time zones if applicable
    3. Allow for adequate preparation time
    4. Follow company scheduling guidelines
    
    Return a list of proposed time slots in order of preference."""
) 