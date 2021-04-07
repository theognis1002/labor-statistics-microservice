This repository is created for Michael McClelland.


# Goals of this project
Please use the data from [this file](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2019/H-1B_Disclosure_Data_FY2019.xlsx). It is an excel file that has public salary data for jobs linked to inmigrant visa applications in the US. This contains a list of ~500k jobs with company names, locations and base salaries. 

## Guidelines for this project

In order to best simulate a real world experience, we have designed a problem that you may not be able to
solve without asking questions, making assumptions, and working around problems. We want to understand how you
will work with others on your team as well as how you solve problems, throught the process you should feel free to 
ask any questions about the goal or process that you wish.

## Goal 1: Review data and identify cleanup areas
Review the data and identify which data you want to extract. Also, decide what you want to do about data that doesn't exactly fit your use case -- e.g. whether to clean it up or omit it, and explain your decisions and the effect on the data.

## Goal 2: Ingest data into an appropriate database
Extract data into any appropriate database. We suggest using Elasticsearch (if you are unfamiliar with it see the notes at the end of this README for some tips), if you have a strong preference for another data warehouse type db (like Amazon Redshift) or Spark that is also fine.

The database needs to support both aggregating statistics and doing free text searches quickly, which is why we suggest Elasticsearch. 

## Goal 3: Create a REST API service with the following interface:
Inputs:
- Title query text (e.g. "software engineer" or "java")
- Location query text (e.g. "new york city", "Portland, Maine", "Portland, Oregon")

Outputs:
- Number of datapoints:
- Mean salary:
- Median salary:
- 25% percentile salary
- 75% percentile salary

## Goal 4: Deployment

- There are two options for deployment:
  - Local (Default): Develop in your own local machine and have us test it in ours. Assume that we will be starting with nothing but the repo and docker + docker-compose on a bare linux machine. How you choose to deploy is entirely up to you.
  - AWS: Should you wish to host your project on AWS instead, we will pay up to $50 in compute costs. 
- Document all deployment instructions. 

# Logistics
- Use this repository to check in your code along with deployment instructions. If this has dependancies, provide instructions on how to install those dependencies so we can deploy and test your code
- Once you have read these instructions, set up a 30 min call with Ron to go over any questions you have. After that, start the assignment and set up a time once you are done to go over your code. 
- This exercise should take about ~5-10 hours of your time, plus time to actually run the code to load the data during testing and deployment.
- We will pay candidates $250 to complete this project regardless of whether you get offered a position at Datapeople. However, in order for you to receive this payment, we require the project to be completed (i.e. code checked in and tested as working).
- When in doubt, ask. If you need guidance on anything just ask Ron, and we'll set up a time to talk with either Ron or one of the other engineering staff.
- We are rooting for you to succeed!

# Notes and Hints
- Here are some resources for getting started with Elasticsearch:
  - [Elasticsearch introduction](https://www.elastic.co/guide/en/elasticsearch/reference/7.12/elasticsearch-intro.html)
  - [Getting started](https://www.elastic.co/guide/en/elasticsearch/reference/7.12/getting-started.html)
  
- Here are some links to Elasticsearch concepts that you might find helpful, if you choose to use it:
  - [mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html)
  - [field data types](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html)
  - [aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html)

- There are several ways to read an Excel file from python (including directly from the url)
