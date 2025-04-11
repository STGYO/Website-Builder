from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool
)
from pathlib import Path
from website_builder.utils.file_manager import FileManager
from website_builder.utils.config_validator import ConfigValidator
import yaml
import os

@CrewBase
class WebsiteBuilder():
    """WebsiteBuilder crew for creating complete websites with multiple specialized agents"""

    def __init__(self, topic: str = None):
        if not topic:
            raise ValueError("Topic is required. Please provide a topic for the website.")
            
        config_dir = Path(__file__).parent / 'config'
        self.agents_config_path = str(config_dir / 'agents.yaml')
        self.tasks_config_path = str(config_dir / 'tasks.yaml')
        
        with open(self.agents_config_path, 'r') as f:
            self.agents_config = yaml.safe_load(f)
        with open(self.tasks_config_path, 'r') as f:
            self.tasks_config = yaml.safe_load(f)
        
        self.file_manager = FileManager()
        self.docs_tool = DirectoryReadTool(directory=str(self.file_manager.output_dir))
        self.file_tool = FileReadTool()
        self.search_tool = SerperDevTool()
        self.web_tool = WebsiteSearchTool()
        
        self.topic = topic
        
        for agent_name, agent_config in self.agents_config.items():
            for key, value in agent_config.items():
                if isinstance(value, str):
                    agent_config[key] = value.format(topic=self.topic)
        
        for task_name, task_config in self.tasks_config.items():
            for key, value in task_config.items():
                if isinstance(value, str):
                    task_config[key] = value.format(topic=self.topic)
        
        ConfigValidator.validate_configs(self.agents_config_path, self.tasks_config_path)

    def save_file(self, content: str, filename: str):
        """Save content to a file in the output directory."""
        return self.file_manager.write_file(filename, content)

    @agent
    def web_researcher(self) -> Agent:
        config = self.agents_config['web_researcher'].copy()
        config['role'] = config['role'].format(topic=self.topic)
        config['goal'] = config['goal'].format(topic=self.topic)
        config['backstory'] = config['backstory'].format(topic=self.topic)
        return Agent(
            config=config,
            verbose=True,
            tools=[self.search_tool, self.web_tool],
            context=[f"Topic: {self.topic}"]
        )

    @agent
    def html_creator(self) -> Agent:
        config = self.agents_config['html_creator'].copy()
        config['role'] = config['role'].format(topic=self.topic)
        config['goal'] = config['goal'].format(topic=self.topic)
        config['backstory'] = config['backstory'].format(topic=self.topic)
        return Agent(
            config=config,
            verbose=True,
            tools=[self.file_tool, self.docs_tool],
            context=[f"Topic: {self.topic}"]
        )

    @agent
    def css_designer(self) -> Agent:
        config = self.agents_config['css_designer'].copy()
        config['role'] = config['role'].format(topic=self.topic)
        config['goal'] = config['goal'].format(topic=self.topic)
        config['backstory'] = config['backstory'].format(topic=self.topic)
        return Agent(
            config=config,
            verbose=True,
            tools=[self.file_tool],
            context=[f"Topic: {self.topic}"]
        )

    @agent
    def js_developer(self) -> Agent:
        config = self.agents_config['js_developer'].copy()
        config['role'] = config['role'].format(topic=self.topic)
        config['goal'] = config['goal'].format(topic=self.topic)
        config['backstory'] = config['backstory'].format(topic=self.topic)
        return Agent(
            config=config,
            verbose=True,
            tools=[self.file_tool],
            context=[f"Topic: {self.topic}"]
        )

    @task
    def research_task(self) -> Task:
        task_config = self.tasks_config['research_task']
        task_config['description'] = task_config['description'].format(topic=self.topic)
        task_config['expected_output'] = task_config['expected_output'].format(topic=self.topic)
        return Task(
            description=task_config['description'],
            expected_output=task_config['expected_output'],
            agent=self.web_researcher(),
            context=task_config['context'],
            dependencies=task_config['dependencies']
        )

    @task
    def html_creation_task(self) -> Task:
        task_config = self.tasks_config['html_creation_task']
        task_config['description'] = task_config['description'].format(topic=self.topic)
        task_config['expected_output'] = task_config['expected_output'].format(topic=self.topic)
        return Task(
            description=task_config['description'],
            expected_output=task_config['expected_output'],
            agent=self.html_creator(),
            context=task_config['context'],
            dependencies=task_config['dependencies'],
            output_file='output/index.html'
        )

    @task
    def css_design_task(self) -> Task:
        task_config = self.tasks_config['css_design_task']
        task_config['description'] = task_config['description'].format(topic=self.topic)
        task_config['expected_output'] = task_config['expected_output'].format(topic=self.topic)
        return Task(
            description=task_config['description'],
            expected_output=task_config['expected_output'],
            agent=self.css_designer(),
            context=task_config['context'],
            dependencies=task_config['dependencies'],
            output_file='output/style.css'
        )

    @task
    def js_development_task(self) -> Task:
        task_config = self.tasks_config['js_development_task']
        task_config['description'] = task_config['description'].format(topic=self.topic)
        task_config['expected_output'] = task_config['expected_output'].format(topic=self.topic)
        return Task(
            description=task_config['description'],
            expected_output=task_config['expected_output'],
            agent=self.js_developer(),
            context=task_config['context'],
            dependencies=task_config['dependencies'],
            output_file='output/script.js'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the WebsiteBuilder crew"""
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable is not set")
            
            llm = LLM(
                model="gemini-pro",
                api_key=api_key,
                provider="google",
                temperature=0.7,
                max_tokens=4000
            )
        except Exception as e:
            raise ValueError(f"Failed to configure LLM: {str(e)}")

        tasks = [
            self.research_task(),
            self.html_creation_task(),
            self.css_design_task(),
            self.js_development_task(),
        ]

        # Ensure output directory exists
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)

        # Create backup directory
        backup_dir = output_dir / 'backups'
        backup_dir.mkdir(exist_ok=True)

        # Create versions directory
        versions_dir = output_dir / 'versions'
        versions_dir.mkdir(exist_ok=True)

        return Crew(
            agents=self.agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
            llm=llm
        )
