from pathlib import Path
import yaml
from typing import Dict, Any, List
import sys
import re

class ConfigValidator:
    """Utility class for validating YAML configuration files."""
    
    REQUIRED_AGENT_FIELDS = ['role', 'goal', 'backstory']
    REQUIRED_TASK_FIELDS = ['description', 'expected_output', 'agent', 'output_file', 'context']
    
    URL_PATTERN = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    @staticmethod
    def load_yaml(file_path: str) -> Dict[str, Any]:
        """
        Load and parse a YAML file.
        
        Args:
            file_path (str): Path to the YAML file
            
        Returns:
            Dict[str, Any]: Parsed YAML content
            
        Raises:
            IOError: If there's an error reading the file
            yaml.YAMLError: If there's an error parsing the YAML
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except IOError as e:
            raise IOError(f"Error reading config file {file_path}: {str(e)}")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML in {file_path}: {str(e)}")
    
    @classmethod
    def validate_agents_config(cls, config: Dict[str, Any]) -> List[str]:
        """
        Validate the agents configuration.
        
        Args:
            config (Dict[str, Any]): Agents configuration dictionary
            
        Returns:
            List[str]: List of validation errors, empty if valid
        """
        errors = []
        for agent_name, agent_config in config.items():
            if not isinstance(agent_config, dict):
                errors.append(f"Agent '{agent_name}' configuration must be a dictionary")
                continue
                
            for field in cls.REQUIRED_AGENT_FIELDS:
                if field not in agent_config:
                    errors.append(f"Agent '{agent_name}' is missing required field '{field}'")
                elif not isinstance(agent_config[field], str):
                    errors.append(f"Agent '{agent_name}' field '{field}' must be a string")
            
            if 'role' in agent_config:
                role = agent_config['role']
                if len(role) < 3:
                    errors.append(f"Agent '{agent_name}' role must be at least 3 characters long")
                if not any(c.isupper() for c in role):
                    errors.append(f"Agent '{agent_name}' role should contain at least one uppercase letter")
            
            if 'goal' in agent_config:
                goal = agent_config['goal']
                if len(goal) < 10:
                    errors.append(f"Agent '{agent_name}' goal must be at least 10 characters long")
                if not goal.endswith('.'):
                    errors.append(f"Agent '{agent_name}' goal should end with a period")
            
            if 'backstory' in agent_config:
                backstory = agent_config['backstory']
                if len(backstory) < 50:
                    errors.append(f"Agent '{agent_name}' backstory must be at least 50 characters long")
                if not backstory.endswith('.'):
                    errors.append(f"Agent '{agent_name}' backstory should end with a period")
            
            if 'allow_delegation' in agent_config:
                if not isinstance(agent_config['allow_delegation'], bool):
                    errors.append(f"Agent '{agent_name}' allow_delegation must be a boolean")
            
            if 'verbose' in agent_config:
                if not isinstance(agent_config['verbose'], bool):
                    errors.append(f"Agent '{agent_name}' verbose must be a boolean")
        
        return errors
    
    @classmethod
    def validate_tasks_config(cls, config: Dict[str, Any], agents_config: Dict[str, Any]) -> List[str]:
        """
        Validate the tasks configuration.
        
        Args:
            config (Dict[str, Any]): Tasks configuration dictionary
            agents_config (Dict[str, Any]): Agents configuration dictionary
            
        Returns:
            List[str]: List of validation errors, empty if valid
        """
        errors = []
        for task_name, task_config in config.items():
            if not isinstance(task_config, dict):
                errors.append(f"Task '{task_name}' configuration must be a dictionary")
                continue
                
            for field in cls.REQUIRED_TASK_FIELDS:
                if field not in task_config:
                    errors.append(f"Task '{task_name}' is missing required field '{field}'")
                elif field in ['description', 'expected_output'] and not isinstance(task_config[field], str):
                    errors.append(f"Task '{task_name}' field '{field}' must be a string")
                elif field == 'agent' and not isinstance(task_config[field], str):
                    errors.append(f"Task '{task_name}' field '{field}' must be a string")
                elif field == 'context' and not isinstance(task_config[field], list):
                    errors.append(f"Task '{task_name}' field '{field}' must be a list")
            
            if 'agent' in task_config:
                agent_name = task_config['agent']
                if agent_name not in agents_config:
                    errors.append(f"Task '{task_name}' references non-existent agent '{agent_name}'")
            
            if 'description' in task_config:
                description = task_config['description']
                if len(description) < 20:
                    errors.append(f"Task '{task_name}' description must be at least 20 characters long")
                if not description.endswith('.'):
                    errors.append(f"Task '{task_name}' description should end with a period")
            
            if 'expected_output' in task_config:
                expected_output = task_config['expected_output']
                if len(expected_output) < 20:
                    errors.append(f"Task '{task_name}' expected output must be at least 20 characters long")
                if not expected_output.endswith('.'):
                    errors.append(f"Task '{task_name}' expected output should end with a period")
            
            if 'output_file' in task_config:
                output_file = task_config['output_file']
                if not isinstance(output_file, str):
                    errors.append(f"Task '{task_name}' output_file must be a string")
                elif not output_file.startswith('output/'):
                    errors.append(f"Task '{task_name}' output_file must start with 'output/'")
            
            if 'dependencies' in task_config:
                dependencies = task_config['dependencies']
                if not isinstance(dependencies, list):
                    errors.append(f"Task '{task_name}' dependencies must be a list")
                else:
                    for dep in dependencies:
                        if not isinstance(dep, str):
                            errors.append(f"Task '{task_name}' dependency must be a string")
                        elif dep not in config:
                            errors.append(f"Task '{task_name}' references non-existent dependency '{dep}'")
        
        return errors
    
    @classmethod
    def validate_configs(cls, agents_path: str, tasks_path: str) -> None:
        """
        Validate both agents and tasks configuration files.
        
        Args:
            agents_path (str): Path to agents configuration file
            tasks_path (str): Path to tasks configuration file
            
        Raises:
            ValueError: If there are validation errors
        """
        agents_config = cls.load_yaml(agents_path)
        tasks_config = cls.load_yaml(tasks_path)
        
        agent_errors = cls.validate_agents_config(agents_config)
        task_errors = cls.validate_tasks_config(tasks_config, agents_config)
        
        if agent_errors or task_errors:
            error_msg = "Configuration validation failed:\n"
            if agent_errors:
                error_msg += "\nAgent configuration errors:\n" + "\n".join(f"- {e}" for e in agent_errors)
            if task_errors:
                error_msg += "\nTask configuration errors:\n" + "\n".join(f"- {e}" for e in task_errors)
            raise ValueError(error_msg) 