# Intelligent Talent Acquisition Assistant

An AI-powered recruitment system that automates candidate sourcing, screening, and initial outreach using multiple specialized agents.

## Features

- **Sourcing Agent**: Automatically crawls job platforms and internal databases
- **Screening Agent**: Uses NLP to assess resumes and job fitment
- **Engagement Agent**: Communicates with candidates using LLM-based chat
- **Scheduling Agent**: Automatically schedules interviews
- **HR Manager Interface**: Real-time chat interface for recruitment process monitoring

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with:
```
GROQ_API_KEY=your_groq_api_key
```

3. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
├── app.py                  # Main Streamlit application
├── agents/                 # AI agents implementation
│   ├── sourcing_agent.py
│   ├── screening_agent.py
│   ├── engagement_agent.py
│   └── scheduling_agent.py
├── utils/                  # Utility functions
│   ├── prompts.py         # Agent prompts
│   └── database.py        # Database operations
├── data/                  # Data storage
│   └── chroma_db/        # Vector database
└── requirements.txt       # Project dependencies
``` 