from bs4 import BeautifulSoup as bs
import requests
import re
from pprint import pprint

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36'}
hh_main_link = 'https://hh.ru'
sj_main_link = 'https://www.superjob.ru'


def hh(position, pages):
    html = requests.get(hh_main_link + '/search/vacancy?clusters=true&enable_snippets=true&text='
                        + position + '&showClusters=true', headers=headers)
    parsed_html = bs(html.text, 'html.parser')

    jobs = []
    for i in range(pages):
        jobs_div = parsed_html.find('div', {'class': 'vacancy-serp'})
        jobs_list = jobs_div.findChildren(recursive=False)
        for job in jobs_list:
            job_data = {}
            request = job.find('span', {'class': 'g-user-content'})
            if request:
                main_info = request.findChild()

                job_name = main_info.getText()
                job_data['name'] = job_name

                job_link = main_info['href']
                job_data['link'] = job_link

                salary = job.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
                if not salary:
                    salary_min = None
                    salary_max = None
                else:
                    salary = salary.getText().replace(u'\xa0', u'')
                    salaries = salary.split('-')
                    salaries[0] = re.sub(r'[^0-9]', '', salaries[0])
                    salary_min = int(salaries[0])
                    if len(salaries) > 1:
                        salaries[1] = re.sub(r'[^0-9]', '', salaries[1])
                        salary_max = int(salaries[1])
                    else:
                        salary_max = None
                job_data['salary_max'] = salary_max
                job_data['salary_min'] = salary_min

                jobs.append(job_data)
        next_page_button = parsed_html.find('a', {'class': 'bloko-button HH-Pager-Control'})
        next_button_link = next_page_button['href']
        html = requests.get(hh_main_link + next_button_link, headers=headers).text
        parsed_html = bs(html, 'html.parser')

    pprint(jobs)
    return jobs


def sj(position, pages):
    html = requests.get(sj_main_link + '/vacancy/search/?keywords=' + position, headers=headers)
    parsed_html = bs(html.text, 'html.parser')

    jobs = []
    for i in range(pages):
        jobs_block = parsed_html.find_all('div', {'class': 'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'})
        for job in jobs_block:
            job_data = {}

            job_name_no_text = job.find('a', {'class': 'icMQ_'})
            job_name = job_name_no_text.text
            job_data['name'] = job_name

            job_link = sj_main_link + job_name_no_text['href']
            job_data['link'] = job_link

            salary = job.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).text
            salary = salary.replace(u'\xa0', u'')

            if '—' in salary:
                salary_min = salary.split('—')[0]
                salary_min = re.sub(r'[^0-9]', '', salary_min)
                salary_max = salary.split('—')[1]
                salary_max = re.sub(r'[^0-9]', '', salary_max)
                salary_min = int(salary_min)
                salary_max = int(salary_max)
            elif 'от' in salary:
                salary_min = salary[2:]
                salary_min = re.sub(r'[^0-9]', '', salary_min)
                salary_min = int(salary_min)
                salary_max = None
            elif 'договорённости' in salary:
                salary_min = None
                salary_max = None
            elif 'до' in salary:
                salary_min = None
                salary_max = salary[2:]
                salary_max = re.sub(r'[^0-9]', '', salary_max)
                salary_max = int(salary_max)
            else:
                salary_min = int(re.sub(r'[^0-9]', '', salary))
                salary_max = int(re.sub(r'[^0-9]', '', salary))

            job_data['salary_max'] = salary_max
            job_data['salary_min'] = salary_min

            jobs.append(job_data)
        url = sj_main_link + \
              parsed_html.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'})['href']
        html = requests.get(url, headers=headers)
        parsed_html = bs(html.text, 'html.parser')

    pprint(jobs)
    return jobs


hh('Python', 2)
sj('Python', 2)
