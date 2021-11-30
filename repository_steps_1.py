from behave import *
from repository import Repository
import pandas as pd
import openpyxl

@given('repo class {name} from {organization} has been created')
def step_impl(context, name, organization):
    context.repo = Repository(name=name, organization=organization)
    context.repo.get_url_repo()
    print('repo successed created..')
    assert context.repo.name == name

@given('repository {name} issues from {organization}')
def step_impl(context, name, organization):
    context.repo = Repository(name=name, organization=organization)
    assert context.repo.name == name and context.repo.organization == organization

@given('we have access for {name} report in {year}')
def step_impl(context, name, year):
    context.report_name = f"{name} repository - {year} report.xlsx"
    context.summary_df = pd.read_excel(context.report_name, sheet_name='Summarized View', engine='openpyxl')
    context.detail_df = pd.read_excel(context.report_name, sheet_name='Detailed View', engine='openpyxl')

    assert len(context.summary_df) > 0 and len(context.detail_df) > 0

@when('detail and summary dataframe prepared')
def step_impl(context):
    context.repo.get_url_repo()
    context.repo.get_issues_df()
    assert len(context.repo.issues_df) > 0

@when('we request issues from github api')
def step_impl(context):
    context.repo.get_issues_df()

@when("we don't have any issues repo")
def step_impl(context):
    assert context.repo.issues_df == None

@when('we open the {type} sheet')
def step_impl(context, type):
    context.type_view = type
    if type == 'Summarized View':
        assert len(context.summary_df) > 0
    else:
        assert len(context.detail_df) > 0

@then('we have issues list')
def step_impl(context):
    assert len(context.repo.issues_df) > 0

@then('we do not create repository report')
def step_impl(context):
    assert context.repo.created_report == False

@then('we have {name} report in {year}')
def step_impl(context, name, year):
    context.repo.get_sheet_report(year=int(year))
    assert context.repo.created_report == True

@then('we see table with column: {columns}')
def step_impl(context, columns):
    if context.type_view == 'Summarized View':
        column_words = ', '.join(context.summary_df.columns)
    else:
        column_words = ', '.join(context.detail_df.columns)
    assert columns == column_words

