import pytest
import os
import tempfile
from pathlib import Path

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for testing."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv('OPENAI_API_KEY', 'test_openai_key')
        mp.setenv('SERPER_API_KEY', 'test_serper_key')
        yield

@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory with basic structure."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        project_dir = Path(tmpdirname)
        
        # Create basic directory structure
        (project_dir / 'src' / 'website_builder' / 'config').mkdir(parents=True)
        (project_dir / 'src' / 'website_builder' / 'utils').mkdir(parents=True)
        (project_dir / 'src' / 'website_builder' / 'tools').mkdir(parents=True)
        
        # Create basic config files
        agents_config = {
            'web_researcher': {
                'role': 'Web Research Specialist',
                'goal': 'Research and gather information',
                'backstory': 'Expert web researcher'
            }
        }
        tasks_config = {
            'research_task': {
                'description': 'Research the topic',
                'expected_output': 'Research document',
                'agent': 'web_researcher'
            }
        }
        
        # Write config files
        import yaml
        with open(project_dir / 'src' / 'website_builder' / 'config' / 'agents.yaml', 'w') as f:
            yaml.dump(agents_config, f)
        with open(project_dir / 'src' / 'website_builder' / 'config' / 'tasks.yaml', 'w') as f:
            yaml.dump(tasks_config, f)
        
        yield project_dir 