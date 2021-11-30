Feature: Repository Report

Scenario: get issues list from github api
# example repository: https://github.com/xendit/xendit-php
Given repo class xendit-php from xendit has been created
When we request issues from github api
Then we have issues list

Scenario: issues list is empty so the repository report will not be created
# example repository: https://github.com/mrqwertyuiop/gatsby-netlify
Given repo class gatsby-netlify from mrqwertyuiop has been created
When we request issues from github api
And we don't have any issues repo
Then we do not create repository report

Scenario Outline: create some repositories report
Given repository <name> issues from <organization>
When detail and summary dataframe prepared
Then we have <name> report in <year>

Examples: Repositories
   | name          | organization | year   |
   | xendit-php    | xendit       | 2021   |
   | xendit-go     | xendit       | 2021   |
   | xendit-node   | xendit       | 2021   |
   | xendit-java   | xendit       | 2021   |

# Main Scenario
Scenario Outline: See Summarized View of Report
Given we have access for <name> report in <year>
When we open the Summarized View sheet
Then we see table with column: Month, Created Issues, Closed Issues

Examples: Repositories
   | name          | organization | year   |
   | xendit-php    | xendit       | 2021   |
   | xendit-go     | xendit       | 2021   |
   | xendit-node   | xendit       | 2021   |
   | xendit-java   | xendit       | 2021   |

Scenario Outline: See Detailed View of Report
Given we have access for <name> report in <year>
When we open the Detailed View sheet
Then we see table with column: Repository Name, Repository URL, Issue Title, Issue Link, Created Issue Date, Closed Issue Date

Examples: Repositories
   | name          | organization | year   |
   | xendit-php    | xendit       | 2021   |
   | xendit-go     | xendit       | 2021   |
   | xendit-node   | xendit       | 2021   |
   | xendit-java   | xendit       | 2021   |


###################
# if you want only single repository, you can use this scenario
# you can change other repository yourself, including your organization repository :)
# Scenario: create some repositories report
# Given repository xendit-php issues from xendit
# When detail and summary dataframe prepared
# Then we have xendit-php report in 2021

# Scenario: See Summarized View of Report
# Given we have access for xendit-php report in 2021
# When we open the Summarized View sheet
# Then we see table with column: Month, Created Issues, Closed Issues

# Scenario: See Detailed View of Report
# Given we have access for xendit-php report in 2021
# When we open the Summarized View sheet
# Then we see table with column: Month, Created Issues, Closed Issues





