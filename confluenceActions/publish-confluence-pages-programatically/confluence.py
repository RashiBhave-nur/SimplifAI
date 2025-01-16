import argparse
import os
import markdown
import datetime
from atlassian import Confluence
from dotenv import load_dotenv

def report_datetime():
    """
    python code to get time in format str
    :return:
    """
    now = datetime.datetime.now()
    formatted_datetime = now.strftime('%d-%B-%Y %A %H:%M')
    return formatted_datetime


def get_confluence_page_id(confluence_client, confluence_space: str, confluence_page_title: str):
    """
    return confluence page id
    :return:
    """
    confluence = confluence_client
    confluence_page_id = confluence.get_page_id(space=confluence_space,title=confluence_page_title)
    print(f'Confluence id is : {confluence_page_id}')
    return confluence_page_id


def render_html_from_md_file(markdown_file_path: str):
    """
    Render html content to pass to confluence object from markdown file
    :param markdown_file_path:
    :return:
    """
    markdown_file_path = markdown_file_path
    with open(markdown_file_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content)
    return html_content


def create_confluence_page(confluence_client, html_content, confluence_space: str, confluence_page_title: str):
    """
    Create a confluence page from scratch using python sdk
    :return:
    """
    confluence = confluence_client
    status = confluence.create_page(
        space=confluence_space,
        title=confluence_page_title,
        body=html_content
    )
    time = report_datetime()
    print(f'Confluence page created on {confluence_space} with title {confluence_page_title} at {time}')


def update_confluence_page_if_exists(confluence_client, html_content, confluence_page_id: str, confluence_page_title: str):
    """
    update an existing confluence page - clear and write fresh if existing
    :param confluence_client:
    :param html_content:
    :param confluence_page_id:
    :param confluence_page_title:
    :return:
    """
    confluence = confluence_client
    status = confluence.update_page(
        page_id=confluence_page_id,
        title=confluence_page_title,
        body=html_content
    )
    time = report_datetime()
    # print(status)
    print(f'Confluence page updated on {confluence_page_title} at {time}')


def append_body_to_page(confluence_client, html_content, confluence_page_id: str, confluence_page_title:str):
    """
    Append body to page if already exist
    :return:
    """
    confluence = confluence_client
    status = confluence.append_page(
        page_id=confluence_page_id,
        title=confluence_page_title,
        append_body=html_content
    )
    # print(status)
    time = report_datetime()
    print(f'Confluence page data appended on {confluence_page_title} at {time}')

def delete_confluence_page(confluence_client, confluence_page_id: str):
    """
    Remove conluence page with confluence page of==id
    :param ce_client:
    :param confluence_page_id:
    :return:
    """
    confluence = confluence_client
    confluence.remove_page(page_id=confluence_page_id)
    time = report_datetime()
    print(f'Confluence page with id {confluence_page_id} removed at {time}')


def choose_action(action:str,confluence_space:str,confluence_page_title:str,markdown_file_path):
    """
    choose a function based on action
    :param action:
    :param confluence_space:
    :param confluence_page_title:
    :param markdown_file_path:
    :return:
    """
    load_dotenv()
    confluence_url = os.getenv('CONFLUENCE_URL')
    # print(confluence_url)
    username = os.getenv('CONFLUENCE_USERNAME')
    # print(username)
    password = os.getenv('CONFLUENCE_PASSWORD')
    # print(password)
    # Create conflience client
    confluence_client = Confluence(url='https://nurix-team.atlassian.net', username='rashi@nurix.ai',
            password='token', cloud=True)
    # Render markdon --> html
    html_content = render_html_from_md_file(markdown_file_path=markdown_file_path)
    # html_content = ""
    if action == 'create':
        print(f'Creating confluence page with title {confluence_page_title}...')
        create_confluence_page(confluence_client=confluence_client, html_content=html_content,
                               confluence_page_title=confluence_page_title, confluence_space=confluence_space)
    elif action == 'update':
        print(f'updating {confluence_page_title}...')
        print(f'retreiving confluence page id...')
        confluence_page_id = get_confluence_page_id(confluence_client=confluence_client, confluence_space=confluence_space,
                                                    confluence_page_title=confluence_page_title)
        update_confluence_page_if_exists(confluence_client=confluence_client, confluence_page_id=confluence_page_id,
                                         html_content=html_content, confluence_page_title=confluence_page_title)
    elif action == "append":
        print(f'modifying confluence page...')
        print(f'retreiving confluence page id...')
        confluence_page_id = get_confluence_page_id(confluence_client=confluence_client,
                                                    confluence_space=confluence_space,
                                                    confluence_page_title=confluence_page_title)
        append_body_to_page(confluence_client=confluence_client, confluence_page_title=confluence_page_title,
                            confluence_page_id=confluence_page_id, html_content=html_content)
    else:
        print(f'Deleting confluence page with title {confluence_page_title}...')
        print(f'retreiving confluence page id...')
        confluence_page_id = get_confluence_page_id(confluence_client=confluence_client,
                                                    confluence_space=confluence_space,
                                                    confluence_page_title=confluence_page_title)
        delete_confluence_page(confluence_client=confluence_client,confluence_page_id=confluence_page_id)


def main():
    """ To test the script"""
    parser = argparse.ArgumentParser(description='Process arguments for the program')
    parser.add_argument("--action", type=str, choices=['create','update','append','delete'], help='Possble actions', required=True)
    # parser.add_argument("--confluence_space", type=str, help='Confluence space', required=True)
    # parser.add_argument("--confluence_page_title", type=str, help='Confluence page title', required=True)
    # parser.add_argument("--markdown_file_path", type=str, help='Markdown file path with file name', required=True)


    args = parser.parse_args()
    action = args.action
    confluence_space = '~rashibhave'
    confluence_page_title = 'Rashi Bhave'
    markdown_file_path = '/Users/rashibhave/Desktop/hackathon-simplifai/confluenceActions/publish-confluence-pages-programatically/Lorem Ipsum.md'

    # function call
    choose_action(action=action,confluence_space=confluence_space,
                  confluence_page_title=confluence_page_title,markdown_file_path=markdown_file_path)


if __name__ == "__main__":
    main()
