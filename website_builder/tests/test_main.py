import pytest
from unittest.mock import patch, MagicMock
from website_builder.main import run, train, replay, test
from website_builder.crew import WebsiteBuilder
from crewai import Task
from crewai.agents.agent_builder.base_agent import BaseAgent

@pytest.fixture
def mock_crew():
    instance = MagicMock(spec=WebsiteBuilder)
    
    # Create mock agents with required fields
    web_researcher = MagicMock(spec=BaseAgent)
    web_researcher.role = "Web Researcher"
    web_researcher.goal = "Research web development topics"
    web_researcher.backstory = "Experienced web researcher"
    
    html_creator = MagicMock(spec=BaseAgent)
    html_creator.role = "HTML Creator"
    html_creator.goal = "Create HTML structure"
    html_creator.backstory = "Expert HTML developer"
    
    css_designer = MagicMock(spec=BaseAgent)
    css_designer.role = "CSS Designer"
    css_designer.goal = "Design website styles"
    css_designer.backstory = "Professional CSS designer"
    
    js_developer = MagicMock(spec=BaseAgent)
    js_developer.role = "JavaScript Developer"
    js_developer.goal = "Implement website functionality"
    js_developer.backstory = "Senior JavaScript developer"
    
    # Set up agent methods
    instance.web_researcher = MagicMock(return_value=web_researcher)
    instance.html_creator = MagicMock(return_value=html_creator)
    instance.css_designer = MagicMock(return_value=css_designer)
    instance.js_developer = MagicMock(return_value=js_developer)
    
    # Set up task methods with properly configured agents
    instance.research_task = MagicMock(return_value=Task(
        description="Research task description",
        expected_output="Research task output",
        agent=web_researcher,
        output_file="research_output.txt",
        context=[],
        dependencies=[]
    ))
    instance.html_creation_task = MagicMock(return_value=Task(
        description="HTML creation task description",
        expected_output="HTML creation task output",
        agent=html_creator,
        output_file="html_output.txt",
        context=[],
        dependencies=[]
    ))
    instance.css_design_task = MagicMock(return_value=Task(
        description="CSS design task description",
        expected_output="CSS design task output",
        agent=css_designer,
        output_file="css_output.txt",
        context=[],
        dependencies=[]
    ))
    instance.js_development_task = MagicMock(return_value=Task(
        description="JS development task description",
        expected_output="JS development task output",
        agent=js_developer,
        output_file="js_output.txt",
        context=[],
        dependencies=[]
    ))
    
    instance.crew = MagicMock()
    return instance

def test_run_success(mock_crew):
    """Test successful run execution."""
    topic = "Test Topic"
    run(topic)
    mock_crew.crew.return_value.kickoff.assert_called_once_with(inputs={'topic': topic, 'current_year': '2024'})

def test_run_failure(mock_crew):
    """Test run execution with error."""
    mock_crew.crew.return_value.kickoff.side_effect = Exception("Test error")
    with pytest.raises(SystemExit):
        run("Test Topic")

def test_train_success(mock_crew):
    """Test successful training execution."""
    iterations = 5
    filename = "test.json"
    topic = "Test Topic"
    train(iterations, filename, topic)
    mock_crew.crew.return_value.train.assert_called_once_with(n_iterations=iterations, filename=filename, inputs={'topic': topic})

def test_train_failure(mock_crew):
    """Test training execution with error."""
    mock_crew.crew.return_value.train.side_effect = Exception("Test error")
    with pytest.raises(SystemExit):
        train(5, "test.json", "Test Topic")

def test_replay_success(mock_crew):
    """Test successful replay execution."""
    task_id = "test_task_id"
    replay(task_id)
    mock_crew.crew.return_value.replay.assert_called_once_with(task_id=task_id)

def test_replay_failure(mock_crew):
    """Test replay execution with error."""
    mock_crew.crew.return_value.replay.side_effect = Exception("Test error")
    with pytest.raises(SystemExit):
        replay("test_task_id")

def test_test_success(mock_crew):
    """Test successful test execution."""
    iterations = 5
    model_name = "gpt-4"
    topic = "Test Topic"
    mock_crew.crew.return_value.test.return_value = {"result": "success"}
    
    result = test(iterations, model_name, topic)
    mock_crew.crew.return_value.test.assert_called_once_with(
        n_iterations=iterations,
        openai_model_name=model_name,
        inputs={'topic': topic, 'current_year': '2024'}
    )
    assert result == {"result": "success"}

def test_test_failure(mock_crew):
    """Test test execution with error."""
    mock_crew.crew.return_value.test.side_effect = Exception("Test error")
    with pytest.raises(SystemExit):
        test(5, "gpt-4", "Test Topic")

def test_test_no_results(mock_crew):
    """Test test execution with no results."""
    iterations = 5
    model_name = "gpt-4"
    topic = "Test Topic"
    mock_crew.crew.return_value.test.return_value = None
    
    result = test(iterations, model_name, topic)
    assert result is None 