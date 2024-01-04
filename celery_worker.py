from celery import Celery
import importlib.util
import sys
import os
import logging
from poetry.factory import Factory
from poetry.utils.env import EnvManager
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
app = Celery('tasks', broker='pyamqp://guest@localhost//')

ROOT_DIR = os.getcwd()

@app.task
def execute_template_job(job_data:dict):
    try:
        # Change the current working directory to the root directory    
        template_name = job_data['template_name']
        template_path = f"templates/{template_name}"

        # Change the current working directory to the template's directory
        os.chdir(template_path)

        # Initialize poetry environment
        poetry = Factory().create_poetry(template_path)
        env_manager = EnvManager(poetry)
        env = env_manager.create_venv()

        # Install dependencies using Poetry
        env.run('poetry', 'install')

        # Dynamically import the main module of the template
        # re template-name to template_path
        tn = template_name.replace('-', '_')
        main_module = importlib.import_module(f"{tn}.main")
        main_func = getattr(main_module, "main")
        logger.info(f"Main function: {main_func}")

        # Dynamically load JobRequestSchema from the corresponding template's schemas.py
        schemas_module = importlib.import_module(f"{tn}.schema")
        JobRequestSchema = getattr(schemas_module, "JobRequestSchema")

        # Validate the job data with the loaded schema
        validated_data = JobRequestSchema(**job_data['template_args'])

        # Execute the job
        results = main_func(validated_data)
        print(results)
        # Change the current working directory back to the root directory
        os.chdir(ROOT_DIR)

        return results
    
    except Exception as e:
        # Change the current working directory back to the root directory
        os.chdir(ROOT_DIR)
        logger.error(e)


if __name__ == '__main__':
    # Test hello_world_1 template
    job_data = {
        "template_name": "hello-world-1",
        "template_args": {
            "name": "John"
        }
    }

    execute_template_job.delay(job_data)