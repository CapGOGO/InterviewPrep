def generate_daily_tasks(interview_agent):
    tasks = {
        "coding_problems": interview_agent.fetch_coding_problems(),
        "system_design_problem": interview_agent.fetch_system_design_problem(),
        "ml_theory": interview_agent.fetch_ml_theory()
    }
    return tasks