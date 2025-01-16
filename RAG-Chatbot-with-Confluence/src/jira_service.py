from jira_bot.commands.issue import create_issue
from jira_bot.commands.list import ls
from jira_bot.commands.update import UpdateSubCommand
from jira_bot.commands.comment import comment
from jira import JIRA
import argparse

class JiraService:
    def __init__(self, server, username, api_key):
        self.jira = JIRA(
            server=server,
            basic_auth=(username, api_key)
        )
        self._setup_parsers()

    def _setup_parsers(self):
        # Create parser for commands
        self.parser = argparse.ArgumentParser(description='JIRA Integration')
        subparsers = self.parser.add_subparsers()
        
        # Initialize command handlers
        self.issue_handler = create_issue(subparsers)
        self.list_handler = ls(subparsers)
        self.update_handler = UpdateSubCommand(subparsers)
        self.comment_handler = comment(subparsers)

    def create_issue(self, project, summary, description, issue_type='Task'):
        """Create a JIRA issue"""
        args = self.parser.parse_args([
            'create',
            '-P', project,
            '-s', summary,
            '-t', issue_type
        ])
        
        config = {
            'default': {
                'project': project,
                'summary': summary,
                'description': description,
                'issuetype': issue_type
            }
        }
        
        return self.issue_handler.run(self.jira, config['default'])

    def list_issues(self, project=None):
        """List JIRA issues"""
        args = self.parser.parse_args(['list', 'issues'])
        config = {'default': {}}
        if project:
            config['default']['project'] = project
            
        return self.list_handler.run(self.jira, config['default'])