## Structure

agentic-opt-assistant/
├── agents/
│   ├── planner_agent.py
│   ├── solver_agent.py
│   ├── explainer_agent.py
│   └── retrieval_agent.py
├── data/                  # PDF/notes for RAG
├── app.py                 # Gradio app
├── main.py                #streamlit app
├── .env                   # API keys
├── README.md
├── requirements.txt
└── utils/
    └── prompt_templates.py
└── api/
    ├── __init__.py
    ├── routes/
    │   ├── planner.py
    │   ├── solver.py
    └── main.py  # FastAPI app
├── templates/              ← HTML files go here
│   └── index.html
└── static/                 ← CSS/JS/images here
    └── style.css

