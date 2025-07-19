# main.py

from agents.interview_agent import InterviewAgent
from prompts.daily_tasks import generate_daily_tasks

def main():
    # Generate and save solutions for all unsolved top company questions
    
    agent = InterviewAgent()
    # Ensure we have a curated list of top questions before attempting solutions
    agent.curate_top_company_questions()
    agent.generate_solutions_for_all_unsolved()
    
    # Generate daily tasks
    daily_tasks = generate_daily_tasks(agent)

    # Display coding questions with category name
    from config import settings
    print("Coding Questions for company:", settings.COMPANY_NAME)
    coding_problems = agent.fetch_coding_problems()
    # Filter problems by company tag if available
    relevant_problems = []
    for problem in coding_problems:
        tags = problem.get('stat', {}).get('question__tags', []) if isinstance(problem, dict) else []
        # LeetCode company tags may be in a different field, adjust as needed
        company_tags = problem.get('companies', []) if isinstance(problem, dict) else []
        if settings.COMPANY_NAME in tags or settings.COMPANY_NAME in company_tags:
            relevant_problems.append(problem)
    # If no relevant problems found, show all
    display_list = relevant_problems if relevant_problems else coding_problems
    for idx, problem in enumerate(display_list, 1):
        category = problem.get('difficulty', 'Unknown') if isinstance(problem, dict) else 'Unknown'
        title = problem.get('stat', {}).get('question__title', str(problem)) if isinstance(problem, dict) else str(problem)
        print(f"{idx}. [{category}] {title}")

    # Display the rest of the tasks for the day
    print("\nOther Daily Tasks:")
    for task in daily_tasks:
        print(task)

if __name__ == "__main__":
    main()