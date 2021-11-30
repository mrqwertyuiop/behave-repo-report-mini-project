
# Short Brief of the project

## Background
Normally, an organization can manage a single repository or more.
To help this task, a report for each repository would be helpful in order to see the performance.
By creating this mini-program, we can automatically generate brief report for any repository we want.
This would help anybody or even engineering team who have concern for their repository. Due to those reasons, this application is created to help and answer those problems

The report will be created as an excel file **(xlsx)** which has 2 sheets, summarized view and detailed view.

The app is developed under BDD framework. Behavior-driven development (or BDD) is an agile software development technique that put clear understanding of desired software behavior through discussion with stakeholders. 

If TDD writing cases is done through multiple tests of unit function, BDD extends TDD by writing test cases in a natural language that non-programmers can read.

Behavior-driven developers use their native language in combination with the ubiquitous language of domain-driven design to describe the purpose and benefit of their code. This allows the developers to focus on why the code should be created, rather than the technical details, and minimizes translation between the technical language in which the code is written and the domain language spoken by the business, users, stakeholders, project management, etc.

BDD is writen by **[Gherkin syntax](https://cucumber.io/docs/gherkin/)**. This application uses python as primary language and behave library is one of some [tools](https://cucumber.io/docs/installation/), which implement BDD paradigm.

To understand the limitation of the project, please read Program Details Section

---
## Development Approach

Application development was started from describing example of the requirement, for example **“get issues list from github api”**. Each requirement is clarified by breaking down into steps. After that, the code for each steps are created **(in this case on steps/repository_steps.py)** and formed what Repository Class look like **(repository.py)**. When the creation of one example was done, writing process moved to the next example. This process modified the Repository Class. The loop was done after the main example requirement had been fulfilled.

This breaking down process into specific small examples before move to the bigger one was executed to reduce the error of the program
Below is the sequence of the example that tried to fulfilled the main requirement (point 3a and 3b)

    1. get issues list from github api -> if empty scenario example: issues list is empty so the repository report will not be created
    2. create some repositories report
    3a. See Summarized View of Report
    3b. See Detailed View of Report

---
## How Behave Works
- First, start to understand what Gherkin syntax works (https://cucumber.io/docs/gherkin/reference/).
- Then, you can start play with behave.
Here are some good introduction resource related to behave. Read the **[tutorial](https://behave.readthedocs.io/en/stable/tutorial.html)**.
Here are some **keywords** that I tried to understand when I build this app (you can find it one the tutorial page):
    - Scenario Outlines
    - Step Parameters
    - Context
    "Context" helps alot. You can store any information that will be used for the next step and you can do other thing too(specified on tutorial page). A short brief from the **[tutorial page](https://behave.readthedocs.io/en/stable/tutorial.html)**:

        > "It’s a clever place where you and behave can store information to share around. It runs at three levels, automatically managed by behave.

- If you want to debug a failure, you can set up something (read https://behave.readthedocs.io/en/stable/tutorial.html#debug-on-error-in-case-of-step-failures)

- Other useful example: (https://github.com/behave/behave.example/tree/master/features)

---
## Program Details

#### Program Structure
 * [steps](./steps)
   * [behave_example.py](./steps/behave_example.py)
   * [repository_steps.py](./steps/repository_steps.py)
 * [repository.py](./repository.py)
 * [README.md](./README.md)
 * [requirements.txt](./requirements.txt)
 * [xendit-go repository - 2021 report.xlsx](./xendit-go repository - 2021 report.xlsx)
 * xendit-java repository - 2021 report.xlsx
 * xendit-node repository - 2021 report.xlsx
 * xendit-php repository - 2021 report.xlsx


#### Repository Class has some properties:
- **name**
    repository name (for example, when you visit https://github.com/xendit/xendit-php, the repository name is "xendit-php")
- **organization**
    organization name (from https://github.com/xendit/xendit-php, the organization name is xendit)
- **url_repo**
    it will be filled by get_url_repo() function
- **issues_df** 
    it will be filled by get_issues_df() function
- **detail_df** 
    it will be filled by get_detail_dataframe() function
- **summary_df**
    it will be filled by get_summary_dataframe() function
- **created_report**
    True value will be assigned after get_sheet_report() completely produced excel report
- **report_name**
    filename of the produced excel report, filled by get_sheet_report()

#### List of functions:
- get_url_repo
- get_issues_df
- get_state_issues
- convert_col_into_datetime
- convert_col_into_string
- get_summary_dataframe
- get_detail_dataframe
- get_sheet_report

#### Scenario sequence (how program works)
The program will run in a sequence, starts from the first scenario **"get issues list from github api"** and complete by scenario **"See Detailed View of Report"**

Some scenarios are ***independent***, while others might ***depend from the result of scenario before them***
.
The **main scenario** of the program: "See Summarized View of Report" and "See Detailed View of Report depend on "create some repositories report".
The "create some repositories report" scenario depends on "get issues list from github api" scenario.

Starting from "get issues list from github api", it will run get_state_issues function, by sending request to the **[GITHUB API](https://docs.github.com/en/rest)**.
>As a reminder, GITHUB API has **[limit rate](https://docs.github.com/en/rest/reference/rate-limit)**. It used on get_issues_df() function. in order to get higher rate limit, you need to set authentication. This project used authentication  with **[access token](https://github.com/settings/tokens)**, although you can use the program without authentication. 

> If you reach the limit, you need to wait a couple minutes before you can use GITHUB API later. By the time you run the command, the scenario "create some repositories report" and its next scenarios will also fail.

#### Commented Scenario
You can try other scenario which is similar, it has been commented on the **"repository.feature"**

---
## Environment and How to Run
1. First, make sure ***you have installed python***. When created this project, I used ***python 3.6.8***
2. ***Create virtual environment*** for this project. You can use pipenv or virtualenv library
3. ***Activate*** the environment and ***install*** the library package, by 
    >**pip install -r requirements.txt**
4. Make sure you already on the ***"features"*** directory
    > **"../features/"**
5. Run command ***"behave repository.feature"***. In this project you can also type only "behave" due to the single feature file that this directory has. However, if you have more than one feature file, you need to specify it. 

    > Note: when command completes, you will see some excel files similar with "xendit-go repository - 2021 report.xlsx" and other 3 files. I put the excel files as a reference.


---
## Other resources
* **Behaviour-Driven Development (BDD) reference** - [link](https://cucumber.io/school/)
* **Behave philosophy** - (still on discussion of BDD) [link](https://behave.readthedocs.io/en/stable/philosophy.html)
* **Behave Documentation** - [link](https://behave.readthedocs.io/en/stable/)
* **Behave Github** - [link](https://github.com/behave/behave)
