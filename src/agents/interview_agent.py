class InterviewAgent:
    def fetch_coding_problems(self):
        import requests, json, os
        from config import settings
        response = requests.get(settings.LEETCODE_API_URL)
        problems = []
        if response.status_code == 200:
            data = response.json()
            # Example: get first N problems
            problems = data.get('stat_status_pairs', [])[:settings.DAILY_CODING_PROBLEMS_COUNT]
        # Save to resources/coding_problems.json
        resources_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')
        os.makedirs(resources_dir, exist_ok=True)
        with open(os.path.join(resources_dir, 'coding_problems.json'), 'w', encoding='utf-8') as f:
            json.dump(problems, f, ensure_ascii=False, indent=2)
        return problems

    def fetch_system_design_problem(self):
        import requests, json, os
        # Placeholder: fetch from a static list or API
        problems = [
            "Design a scalable recommendation system.",
            "Design a distributed cache.",
            "Design a real-time chat application."
        ]
        from config import settings
        selected = problems[:settings.SYSTEM_DESIGN_PROBLEM_COUNT]
        resources_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')
        os.makedirs(resources_dir, exist_ok=True)
        with open(os.path.join(resources_dir, 'system_design_problem.json'), 'w', encoding='utf-8') as f:
            json.dump(selected, f, ensure_ascii=False, indent=2)
        return selected

    def fetch_ml_theory(self):
        import requests, json, os
        from bs4 import BeautifulSoup
        from config import settings
        response = requests.get(settings.WIKIPEDIA_ML_URL)
        topics = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Example: get all h2 headings as topics
            topics = [h2.text.strip() for h2 in soup.find_all("h2")]
        selected = topics[:settings.ML_THEORY_TOPICS_COUNT]
        resources_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')
        os.makedirs(resources_dir, exist_ok=True)
        with open(os.path.join(resources_dir, 'ml_theory.json'), 'w', encoding='utf-8') as f:
            json.dump(selected, f, ensure_ascii=False, indent=2)
        return selected