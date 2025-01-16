# publish-confluence-pages-programatically
publish confluce pages programattically

# using poetry as python virtual environment manager

* [Python - Poetry docs](https://python-poetry.org/docs/managing-environments/)
* [Poetry set up - Pycharm](https://www.jetbrains.com/help/pycharm/poetry.html)

# Python sdk from atlassian
* [Atlassian python sdk](https://atlassian-python-api.readthedocs.io/confluence.htmlhttps://atlassian-python-api.readthedocs.io/confluence.html)

**Python-dotenv package takes care of env variable set up on local system**

## .env file
```
CONFLUENCE_URL="xxxx"
CONFLUENCE_USERNAME="xxxx"
CONFLUENCE_PASSWORD="xxxx"
```

:heavy_check_mark:  Replace "xxxx" with proper values. this is used for authentication

# Program Inputs

The program requires 4 Inputs

* action --> action to be performed. One among 'create','update','append','delete'
* confluence_space --> confluence space
* confluence_page_title --> new confluence page title
* markdown_file_path --> markdown file path and name based. of md files are inside a folder use complete path<br> </br>
**Eg**: foldername/markdown file name

# Run code in local

1. clone the repository to your local
2. Change directory to the cloned repository
3. set up the .env file 
4. Run `python3 confluence.py --confluence_space <provide your confluence space name> --confluence_page_title "<Confluence title>" --action <action> --markdown_file_path <markfown file>`
5. Run python3 confluence.py --confluence_space devwithkrishna --confluence_page_title "This is the title - QT" --action update --markdown_file_path README.md


`usage: confluence.py [-h] --action {create,update,append,delete}
                     --confluence_space CONFLUENCE_SPACE
                     --confluence_page_title CONFLUENCE_PAGE_TITLE
                     --markdown_file_path MARKDOWN_FILE_PATH`


>[!NOTE]
> This Program uses username & api key for authentication with atlassian confluence.
> On local testing python-dotenv with .env file is used
> On GitHub Workflow, passed as aa environment variable in from GitHub Secrets.