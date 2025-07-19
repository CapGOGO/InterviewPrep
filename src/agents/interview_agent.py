class InterviewAgent:
    def generate_solutions_for_all_unsolved(self):
        unsolved = self.get_unsolved_questions()
        if not unsolved:
            # Try to populate questions if none are available yet
            self.curate_top_company_questions()
            unsolved = self.get_unsolved_questions()
        for question in unsolved:
            print(f"Generating solutions for: {question.get('stat', {}).get('question__title', '')}")
            py_solution = self.generate_llm_solution(question, 'python')
            cpp_solution = self.generate_llm_solution(question, 'cpp')
            qid = question.get('stat', {}).get('question_id')
            self.mark_question_solved(qid)
    def curate_top_company_questions(self):
        import requests, json, os
        from ..config import settings
        response = requests.get(settings.LEETCODE_API_URL)
        top_questions = []
        if response.status_code == 200:
            data = response.json()
            all_problems = data.get('stat_status_pairs', [])
            # Filter by company
            company = settings.COMPANY_NAME
            relevant = []
            for prob in all_problems:
                tags = prob.get('stat', {}).get('question__tags', []) if isinstance(prob, dict) else []
                company_tags = prob.get('companies', []) if isinstance(prob, dict) else []
                if company in tags or company in company_tags:
                    relevant.append(prob)
            # Sort by total_submitted (most hits)
            relevant.sort(key=lambda x: x.get('stat', {}).get('total_submitted', 0), reverse=True)
            top_questions = relevant[:100]
        # Save top 100 to file
        resources_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')
        os.makedirs(resources_dir, exist_ok=True)
        with open(os.path.join(resources_dir, 'top_company_questions.json'), 'w', encoding='utf-8') as f:
            json.dump(top_questions, f, ensure_ascii=False, indent=2)
        return top_questions

    def get_unsolved_questions(self):
        import json, os
        resources_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')
        top_path = os.path.join(resources_dir, 'top_company_questions.json')
        solved_path = os.path.join(resources_dir, 'solved_questions.json')
        if not os.path.exists(top_path):
            return []
        with open(top_path, 'r', encoding='utf-8') as f:
            top_questions = json.load(f)
        solved_ids = set()
        if os.path.exists(solved_path):
            with open(solved_path, 'r', encoding='utf-8') as f:
                solved_ids = set(json.load(f))
        unsolved = [q for q in top_questions if q.get('stat', {}).get('question_id') not in solved_ids]
        return unsolved

    def mark_question_solved(self, question_id):
        import json, os
        resources_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')
        solved_path = os.path.join(resources_dir, 'solved_questions.json')
        solved_ids = set()
        if os.path.exists(solved_path):
            with open(solved_path, 'r', encoding='utf-8') as f:
                solved_ids = set(json.load(f))
        solved_ids.add(question_id)
        with open(solved_path, 'w', encoding='utf-8') as f:
            json.dump(list(solved_ids), f, ensure_ascii=False, indent=2)

    def generate_llm_solution(self, question, language):
        import requests, os
        from ..config import settings
        # Prepare prompt for LLM
        title = question.get('stat', {}).get('question__title', '')
        description = f"Solve the following coding problem in {language}: {title}. Provide the most optimized solution and explain briefly."
        # Example for Google Gemini API (replace with your actual endpoint and headers)
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + settings.API_KEY
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": description}]}]
        }
        response = requests.post(url, headers=headers, json=payload)
        solution = ""
        if response.status_code == 200:
            data = response.json()
            # Extract solution from response (adjust as per API)
            solution = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        # Save solution to file
        ext = 'py' if language.lower() == 'python' else 'cpp' if language.lower() == 'cpp' else language
        resources_dir = os.path.join(os.path.dirname(__file__), '..', 'resources', 'solutions', language.lower())
        os.makedirs(resources_dir, exist_ok=True)
        qid = question.get('stat', {}).get('question_id')
        filename = os.path.join(resources_dir, f"{qid}.{ext}")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(solution)
        return solution
    def fetch_coding_problems(self):
        import requests, json, os, random
        from config import settings
        response = requests.get(settings.LEETCODE_API_URL)
        problems = []
        if response.status_code == 200:
            data = response.json()
            all_problems = data.get('stat_status_pairs', [])
            # Try to filter by company tag
            company = settings.COMPANY_NAME
            relevant = []
            for prob in all_problems:
                tags = prob.get('stat', {}).get('question__tags', []) if isinstance(prob, dict) else []
                company_tags = prob.get('companies', []) if isinstance(prob, dict) else []
                if company in tags or company in company_tags:
                    relevant.append(prob)
            # If relevant problems found, randomly select from them
            source = relevant if relevant else all_problems
            problems = random.sample(source, min(settings.DAILY_CODING_PROBLEMS_COUNT, len(source)))
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