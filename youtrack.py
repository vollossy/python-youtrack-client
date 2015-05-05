__author__ = 'roman'

import requests
import xml.etree.ElementTree as ET
from datetime import datetime


class YoutrackClient:
    """Youtrack rest api client"""

    def __init__(self, login, password, base_url):
        """

        :param login: User login
        :param password: User Password
        :param base_url: base url(should look like 'youtrack.test:8081', without 'http://')
        :return:
        """
        super().__init__()
        self.login = login
        self.password = password
        #todo: Добавить проверку на наличие http:// и автоматическую подстановку, если не указано
        self.base_url = 'http://'+base_url
        self.cookies = dict()

        self.sign_in()


    def sign_in(self):
        """Provides functionality for user login

        Sends request to api login endpoint

        :return: boolean Result of login
        """
        r = requests.post(self.base_url+'/rest/user/login', data={'login': self.login, 'password': self.password})

        result = ET.fromstring(r.text)
        self.cookies = r.cookies
        if result.text == 'ok':
            return True
        raise Exception(result.text)

    def get_issues(self, filter):
        """Gets issues from list issues endpoint

        :param filter: string Filter query to reduce items amount
        :return: list of YoutrackIssue
        """
        r = requests.get(self.base_url+'/rest/issue', {'filter': filter}, cookies=self.cookies)
        issues = ET.fromstring(r.text)
        parsed_issues = []
        for issue in issues:
            due_date = issue.find('field[@name="Due Date"]')
            if due_date:
                due_date = datetime.fromtimestamp(int(due_date[0].text)/1e3)
            yti = YoutrackIssue(
                id=issue.attrib['id'],
                summary=issue.find('field[@name="summary"]')[0].text,
                description=issue.find('field[@name="description"]')[0].text,
                due_date=due_date
            )
            parsed_issues.append(yti)
        return parsed_issues


class YoutrackIssue:
    """Simple entity representing single youtrack issue"""

    def __init__(self, id, summary, description, due_date=None):
        """Constructor

        :param id: string Issue id(for example, um-112)
        :param summary: string Issue summary
        :param description: string Issue description
        :param due_date: datetime Issue due date
        """
        super().__init__()
        self.id = id
        self.summary = summary
        self.description = description
        self.due_date = due_date

