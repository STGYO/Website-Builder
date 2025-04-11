import pytest
import tempfile
import os
import yaml
from website_builder.utils.config_validator import ConfigValidator

@pytest.fixture
def temp_config_dir():
    """Create a temporary directory for test config files."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

@pytest.fixture
def valid_agents_config(temp_config_dir):
    """Create a valid agents configuration file."""
    config = {
        'web_researcher': {
            'role': 'Web Research Specialist',
            'goal': 'Research and gather information',
            'backstory': 'Expert web researcher'
        },
        'html_creator': {
            'role': 'HTML Creator',
            'goal': 'Create HTML structure',
            'backstory': 'Skilled HTML developer'
        }
    }
    file_path = os.path.join(temp_config_dir, 'agents.yaml')
    with open(file_path, 'w') as f:
        yaml.dump(config, f)
    return file_path

@pytest.fixture
def valid_tasks_config(temp_config_dir):
    """Create a valid tasks configuration file."""
    config = {
        'research_task': {
            'description': 'Research the topic',
            'expected_output': 'Research document',
            'agent': 'web_researcher'
        },
        'html_task': {
            'description': 'Create HTML',
            'expected_output': 'HTML file',
            'agent': 'html_creator'
        }
    }
    file_path = os.path.join(temp_config_dir, 'tasks.yaml')
    with open(file_path, 'w') as f:
        yaml.dump(config, f)
    return file_path

def test_valid_configs(valid_agents_config, valid_tasks_config):
    """Test validation of valid configuration files."""
    ConfigValidator.validate_configs(valid_agents_config, valid_tasks_config)
    # Should not raise any exceptions

def test_invalid_agent_config(temp_config_dir, valid_tasks_config):
    """Test validation of invalid agent configuration."""
    invalid_config = {
        'web_researcher': {
            'role': 'Web Research Specialist',
            # Missing required fields
        }
    }
    file_path = os.path.join(temp_config_dir, 'agents.yaml')
    with open(file_path, 'w') as f:
        yaml.dump(invalid_config, f)
    
    with pytest.raises(ValueError) as exc_info:
        ConfigValidator.validate_configs(file_path, valid_tasks_config)
    assert 'missing required field' in str(exc_info.value)

def test_invalid_task_config(temp_config_dir, valid_agents_config):
    """Test validation of invalid task configuration."""
    invalid_config = {
        'research_task': {
            'description': 'Research the topic',
            # Missing required fields
        }
    }
    file_path = os.path.join(temp_config_dir, 'tasks.yaml')
    with open(file_path, 'w') as f:
        yaml.dump(invalid_config, f)
    
    with pytest.raises(ValueError) as exc_info:
        ConfigValidator.validate_configs(valid_agents_config, file_path)
    assert 'missing required field' in str(exc_info.value)

def test_nonexistent_agent_reference(temp_config_dir, valid_agents_config):
    """Test validation of task referencing nonexistent agent."""
    invalid_config = {
        'research_task': {
            'description': 'Research the topic',
            'expected_output': 'Research document',
            'agent': 'nonexistent_agent'
        }
    }
    file_path = os.path.join(temp_config_dir, 'tasks.yaml')
    with open(file_path, 'w') as f:
        yaml.dump(invalid_config, f)
    
    with pytest.raises(ValueError) as exc_info:
        ConfigValidator.validate_configs(valid_agents_config, file_path)
    assert 'references non-existent agent' in str(exc_info.value)

def test_invalid_yaml_syntax(temp_config_dir):
    """Test validation of invalid YAML syntax."""
    invalid_yaml = """
    web_researcher:
        role: Web Research Specialist
        goal: Research and gather information
        backstory: Expert web researcher
        invalid: yaml: syntax: here
    """
    file_path = os.path.join(temp_config_dir, 'agents.yaml')
    with open(file_path, 'w') as f:
        f.write(invalid_yaml)
    
    with pytest.raises(yaml.YAMLError):
        ConfigValidator.validate_configs(file_path, 'dummy_tasks.yaml') 