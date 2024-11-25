import os
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
log = logging.getLogger()

class SelfEvolvingApp:
    def __init__(self):
        self.version = "0.1"
        self.logs = []
        self.project_name = "my_app"
        self.structure = {
            "main_file": "app.py",
            "readme": "README.md",
            "config": "config.json"
        }

    def ask_user(self):
        log.info("Starting self-evolution process...")
        self.project_name = input("Enter the project name (default: my_app): ") or self.project_name
        initial_feature = input("What feature should the app start with? (e.g., 'Hello World API'): ")
        return initial_feature

    def generate_initial_files(self, feature):
        log.info("Generating initial files...")
        os.makedirs(self.project_name, exist_ok=True)

        # Main app file
        main_file_content = f"""
# {self.project_name} - Generated by Self-Evolving App v{self.version}
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to {self.project_name}! Feature: {feature}"

if __name__ == "__main__":
    app.run(debug=True)
"""
        self._write_file(os.path.join(self.project_name, self.structure["main_file"]), main_file_content)

        # README file
        readme_content = f"# {self.project_name}\n\nFeature: {feature}\n\nGenerated by Self-Evolving App v{self.version}."
        self._write_file(os.path.join(self.project_name, self.structure["readme"]), readme_content)

        # Config file
        config_data = {
            "project_name": self.project_name,
            "version": self.version,
            "features": [feature],
            "last_updated": datetime.now().isoformat()
        }
        self._write_file(
            os.path.join(self.project_name, self.structure["config"]),
            json.dumps(config_data, indent=4)
        )

        log.info("Initial files created successfully.")

    def evolve(self):
        log.info("Evolving the app...")
        # Ask the user for another feature
        new_feature = input("What new feature should I add? (e.g., '/status endpoint', press Enter to skip): ")
        if new_feature:
            self.add_feature(new_feature)
            self.logs.append(f"Added new feature: {new_feature}")
        else:
            log.info("No new features added.")

    def add_feature(self, feature):
        log.info(f"Adding feature: {feature}...")
        main_file_path = os.path.join(self.project_name, self.structure["main_file"])
        with open(main_file_path, "r") as f:
            content = f.read()

        # Append new route for the feature
        new_route = f"""
@app.route("/{feature.split()[0].lower()}")
def {feature.split()[0].lower()}():
    return "{feature} is live!"
"""
        content += new_route
        self._write_file(main_file_path, content)

        # Update config
        config_path = os.path.join(self.project_name, self.structure["config"])
        with open(config_path, "r") as f:
            config_data = json.load(f)

        config_data["features"].append(feature)
        config_data["last_updated"] = datetime.now().isoformat()
        self._write_file(config_path, json.dumps(config_data, indent=4))

        log.info(f"Feature '{feature}' added successfully.")

    def _write_file(self, path, content):
        with open(path, "w") as f:
            f.write(content)
        log.info(f"File written: {path}")

    def run(self):
        feature = self.ask_user()
        self.generate_initial_files(feature)
        self.evolve()

if __name__ == "__main__":
    app = SelfEvolvingApp()
    app.run()
