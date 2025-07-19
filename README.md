# Job Prep Agentic System

This project is designed to assist machine learning engineers in preparing for job switches and interviews. It provides daily coding problems, system design challenges, and machine learning theory topics, along with resources tailored to specific companies.

## Project Structure

- **src/main.py**: Entry point of the application that initializes the agentic system and orchestrates daily tasks.
- **src/agents/interview_agent.py**: Contains the `InterviewAgent` class with methods to fetch coding problems, system design problems, and ML theory topics.
- **src/prompts/daily_tasks.py**: Exports a function to generate a list of daily tasks.
- **src/resources/company_resources.py**: Provides a function to find resources relevant to specific companies.
- **src/utils/helpers.py**: Contains utility functions for formatting output and handling API requests.
- **src/config/settings.py**: Configuration settings for the application, including API keys and resource URLs.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd job-prep-agentic-system
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure any necessary settings in `src/config/settings.py`.

## Usage Guidelines

To run the application, execute the following command:
```
python src/main.py
```

This will start the agentic system and generate daily tasks for preparation.

## Functionality Overview

The system will:
- Provide a set of coding problems daily.
- Present a system design problem.
- Offer a topic in machine learning theory.
- Find and suggest resources relevant to specific companies.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.