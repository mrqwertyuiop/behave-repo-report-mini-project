import requests
import pandas as pd
import numpy as np

class Repository:
    def __init__(self, name='', organization=''):
        # the explanation for each property is documented on README.md
        self.name = name
        self.organization = organization
        self.url_repo = ''
        self.issues_df = None
        # for final dataframe report
        self.detail_df = None
        self.summary_df = None
        # flag variable to check if the report has been created pr not
        self.created_report = False
        self.report_name = ''
    

    def get_url_repo(self):
        # set url_repo into some url api repo github
        self.url_repo = f"https://api.github.com/repos/{self.organization}/{self.name}"


    def get_issues_df(self):
        # we will do loop from page_index 1 until last page which still has data, by default, each page has 30 issues
        page_index = 1

        # this is example of using access_token from github account, for the demo only, active for 30 days
        # if we make request by access_token or other authentication method, the API rate limit will be higher than without any authentication
        # if you do not want to use authentication, remove headers parameter from get request
        access_token = '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'
        headers = {'Authorization': f'access_token {access_token}'}
        
        # LOOPING to get all complete records of issues
        page_url = f"{self.url_repo}/issues?state=all&page={page_index}"
        res = requests.get(page_url, headers=headers)
        res_issues = res.json()

        completed_downloaded_issues = []
        while len(res_issues) != 0:
            # first conditional is to check if the request has meet the limit rate of github API
            if type(res_issues) != type([]):
               if "API rate limit exceeded" in res_issues.get('message'):
                   break
            # if the request can get list issue
            else:
                # append the list into completed_downloaded_issues
                completed_downloaded_issues += res_issues
                # move to the next page and create new request
                page_index += 1
                page_url = f"{self.url_repo}/issues?state=all&page={page_index}"
                res = requests.get(page_url)
                res_issues = res.json()
        
        if len(completed_downloaded_issues) > 0:

            # create dataframe
            resource_df = pd.DataFrame(data=completed_downloaded_issues)

            # filtering the issues record, because completed_downloaded_issues also contain pull request which state is 'closed'
            self.issues_df = resource_df[pd.isna(resource_df["pull_request"])]


    def get_state_issues(self, state=''):
        # to filter dataframe based on desired state, 'open' or 'closed'
        state_issues_df = self.issues_df[self.issues_df['state'] == state]
        return state_issues_df


    def convert_col_into_datetime(self, column):
        # to convert a column from dataframe into datetime object
        return pd.to_datetime(column, errors='ignore')


    def convert_col_into_string(self, column):
        # to convert a datetime column from dataframe into string,due to process of saving into excel report
        column = column.apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        
        # to clean up values which equal 'NaT' datetime object 
        column = column.apply(lambda x: '' if x == 'NaT' else x)
        return column
    

    def get_summary_dataframe(self, year):
        # create a summary dataframe, processed from whole issues record
        # the steps: 
        # 1.convert the typical datetime column into datetime object
        # 2.loop each month by filtering only record with 'created_at' column month's value equal to related month,
        # count the records, append the related month records into array
        # 3. convert the array into dataframe and assign the value for summary_df field object

        # a dictionary to get month's name, with key of month number
        month_numb_to_str = {
        1:'Jan', 2:'Feb', 3:'Mar',4:'Apr', 5:'May', 6:'June',
        7:'July',8:'Aug', 9:'Sep',10:'Oct', 11:'Nov', 12:'Dec'
        }

        issues_df = self.issues_df

        # convert the datetime column into datetime object
        issues_df['created_at'] = self.convert_col_into_datetime(issues_df['created_at'])
        issues_df['updated_at'] = self.convert_col_into_datetime(issues_df['updated_at'])
        issues_df['closed_at'] = self.convert_col_into_datetime(issues_df['closed_at'])

        # count record for 'closed' and 'open' issue(s) for each month
        closed_issues_df = self.get_state_issues('closed')
        open_issues_df = self.get_state_issues('open')

        # count open and closed issues for each month, then save the result into list and append into issues_arr
        issues_arr = []
        for month in range(1,13):
            open_issues = open_issues_df[(open_issues_df['created_at'].dt.month == month) & (open_issues_df['created_at'].dt.year == year)]
            closed_issues = closed_issues_df[(closed_issues_df['closed_at'].dt.month == month) & (closed_issues_df['closed_at'].dt.year == year)]
            record = [month_numb_to_str[month],len(open_issues), len(closed_issues)]
            issues_arr.append(record)

        # convert the issues_arr into dataframe
        summary_df = pd.DataFrame.from_dict(issues_arr)
        summary_df.columns = ['Month', 'Created Issues', 'Closed Issues']

        self.summary_df = summary_df


    def get_detail_dataframe(self, year):
        # create a detail dataframe, processed from whole issues record
        # the steps: 
        # 1.convert the typical datetime column into datetime object
        # 2.filter only for the specified year by datetime dataframe method
        # 3.convert the datetime object columns into string type
        # 4.loop each record of issues by construct each desired value of columns
        # 5. convert the array into dataframe and assign the value for summary_df field object
        detail_issues= []
        issues_df = self.issues_df

        # convert typical datetime into datetime object column
        issues_df['created_at'] = self.convert_col_into_datetime(issues_df['created_at'])
        issues_df['updated_at'] = self.convert_col_into_datetime(issues_df['updated_at'])
        issues_df['closed_at'] = self.convert_col_into_datetime(issues_df['closed_at'])

        # filter only for the specified year
        issues_df = issues_df[(issues_df['created_at'].dt.year == year)]

        # convert datetime column into string type
        issues_df['created_at'] = self.convert_col_into_string(issues_df['created_at'])
        issues_df['updated_at'] = self.convert_col_into_string(issues_df['updated_at'])
        issues_df['closed_at'] = self.convert_col_into_string(issues_df['closed_at'])
        
        for row in issues_df.iterrows():
            row_data = row[1]            
            detail_issues.append([self.name, self.url_repo, row_data['title'], row_data['html_url'], row_data['created_at'], row_data['closed_at']])

        detail_df = pd.DataFrame(data=detail_issues)
        detail_df.columns = ['Repository Name', 'Repository URL', 'Issue Title', 'Issue Link', 'Created Issue Date', 'Closed Issue Date']
        self.detail_df = detail_df

    def get_sheet_report(self, year):
        # output: xlsx file of repository report
        # the steps: 
        # 1.get detail dataframe and summary dataframe
        # 2.if both dataframe exist, we can contiune to save both into separated sheet
        
        self.get_detail_dataframe(year)
        self.get_summary_dataframe(year)
        report_name = f"{self.name} repository - {year} report.xlsx"

        # Create a Pandas Excel writer using openpyxl as the engine.
        writer = pd.ExcelWriter(report_name, engine='openpyxl')

        # Write each dataframe to a different worksheet.
        self.summary_df.to_excel(writer, sheet_name='Summarized View', index=False)
        self.detail_df.to_excel(writer, sheet_name='Detailed View', index=False)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

        # set field created_report that creation of report has been done
        self.created_report = True
        self.report_name = report_name





