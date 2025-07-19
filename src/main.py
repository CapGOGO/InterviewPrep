# main.py

from agents.interview_agent import InterviewAgent
from prompts.daily_tasks import generate_daily_tasks

def main():
    agent = InterviewAgent()
    
    # Generate daily tasks
    daily_tasks = generate_daily_tasks(agent)
    
    # Display the tasks for the day
    for task in daily_tasks:
        print(task)

if __name__ == "__main__":
    main()