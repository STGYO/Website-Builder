import sys
import warnings
import argparse
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from website_builder.crew import WebsiteBuilder
import click

load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

@click.group()
def cli():
    pass

@cli.command()
@click.argument('topic')
def run(topic):
    """Run the website builder with a specific topic"""
    print(f"Running crew for topic: {topic}")
    try:
        builder = WebsiteBuilder(topic=topic)
        crew = builder.crew()
        result = crew.kickoff()
        print("Website building completed successfully!")
        return result
    except Exception as e:
        print(f"Error during 'run': {str(e)}")
        print("Please check your configuration and try again.")
        sys.exit(1)

@cli.command()
@click.argument('iterations', type=int)
@click.argument('filename')
@click.argument('topic')
def train(iterations: int, filename: str, topic: str) -> None:
    """
    Train the crew for a given number of iterations.
    
    Args:
        iterations (int): Number of training iterations
        filename (str): Name of the file to save training session
        topic (str): Topic context for training
        
    Raises:
        Exception: If there's an error during training
    """
    inputs: Dict[str, str] = {
        "topic": topic
    }
    print(f"Training crew for topic '{topic}' with {iterations} iterations, saving to '{filename}'...")
    try:
        WebsiteBuilder(topic=topic).crew().train(n_iterations=iterations, filename=filename, inputs=inputs)
        print("Crew training finished successfully.")
    except Exception as e:
        print(f"Error during 'train': {str(e)}", file=sys.stderr)
        print("Please check your configuration and try again.", file=sys.stderr)
        sys.exit(1)

@cli.command()
@click.argument('task_id')
def replay(task_id: str) -> None:
    """Replay the crew execution from a specific task."""
    print(f"Replaying crew execution starting from task: {task_id}")
    try:
        WebsiteBuilder().crew().replay(task_id=task_id)
        print("Crew replay finished successfully.")
    except Exception as e:
        print(f"Error during 'replay': {str(e)}", file=sys.stderr)
        print("Please check the task ID and try again.", file=sys.stderr)
        sys.exit(1)

@cli.command()
@click.argument('iterations', type=int)
@click.argument('model_name')
@click.argument('topic')
def test(iterations: int, model_name: str, topic: str) -> Optional[Dict[str, Any]]:
    """Test the crew execution and returns the results."""
    inputs: Dict[str, str] = {
        "topic": topic,
        "current_year": str(datetime.now().year)
    }
    print(f"Testing crew for topic '{topic}' with {iterations} iterations using model '{model_name}'...")
    try:
        results = WebsiteBuilder().crew().test(n_iterations=iterations, openai_model_name=model_name, inputs=inputs)
        print("Crew testing finished successfully.")
        if results:
            print("\nTest Results:")
            print(results)
        return results
    except Exception as e:
        print(f"Error during 'test': {str(e)}", file=sys.stderr)
        print("Please check your configuration and try again.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    cli()
