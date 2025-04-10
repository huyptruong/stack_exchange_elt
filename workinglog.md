# 4/9/2025
Added a virtual environment

Improve the web scraping code with pagination capabiltiy

# 12/11/2024

Talk with Bobby about him leading the sessions.

# 12/2/2024

How to add comments to the pull request.
* The shorter the commit, the more likely I will get feedback from the reviewer.

Watch out for the API rate limit on stack exchange
* Bobby thinks it's per credential.
* Why don't we just create 10 ghosts account for the workaround.

End-goal Objective
1. What are the questions with the most scores?
2. What are the answers to those questions?
3. Who provided those answers
  * We assume that these people are experts in the field of landscaping and gardening.
  * We'll reach out to them to validate our list of ideas.

Nice-to-have goal:
* Create a chatbot to answer questions using LLM technology.

Question: What do people do as the data keep changing.

So we agreed that since the size of the gardening se is small, we're just gonna run the code everytime to get the latest data. At some point it's not going to be sustainable for us, and we'll come back to partitioning or incremental extraction.

## Next step
* Show Bobby the partition example that I learned from my Data Engineering course sometime ago.
* Update the scraper to have id fields and run the code (try increasing it to 10, 100, etc., measure the run time, see if we have any rate limit error)
* Look into Athena, Bobby would love to see me presenting Athena.
* Study dbt

Set up metric and progress tracker

# 11/25/2024

We want to store data in a way so that we don't lose any critical information and we can come back to it.

Here' are some data format to consider:
* csv. Could be bad since it could take a long time to save and read.
* serialized data like pickle? **Reasearch it.**
* parquet, avro, json? **Research it.**

In general, the job will make the decision on the data type.
* So what's the raw format for this extracted stackexchange data? Isn't it json?

## Next step
* Develop a proof of concept for the entire analytics pipeline: extract data into a preferred data format, save the data source into s3, connect athena to it for querying, and finally connect Tableau to athena for visualization.
  * ✅ Got the code for scraping data as JSON and uploading it to s3.
  * ❓ I'm not sure how to efficiently do the partition in s3. Do I need to rewrite my code ```webscrape_and_s3upload.py```? The concept of partition sounds very much like creating a bunch of folders for storing data on different days.
  * ❓ My problem right now is I don't know what to do: json -> parquet, then do query in Athena?
    * I can already connect Tableau to s3 https://help.tableau.com/current/pro/desktop/en-us/examples_amazons3.htm.
    * Memory could be a huge issue too. Even though data are not stored locally, my machine must have been "holding" the data while scraping the web. I'm thinking my RAM. So an obvious question is whether my laptop's RAM can hold a lot of data.
      * Maybe that's why we introduce the concept of partitioning.
      * Or we could just run the code on the cloud and push everything else up there.
* Automation: Use Lambda or Airflow to trigger dbt runs and automate workflows.
  * ❓Why is there a need for Airflow? Why can't we do everything in AWS?
* **Learn more about dbt**
* **Experiment the difference between parquet and csv**
* **Review the idea of partition from the DE specialization on Coursera**
## More on data type (from Bobby)

When comparing Parquet to CSV, Parquet generally offers several advantages, particularly for large-scale data processing, analytics, and storage. Here’s a breakdown of the key differences and advantages of Parquet over CSV:

**Data Storage Efficiency**

Parquet:

Columnar Storage: Parquet is a columnar storage format, which means data is stored by columns instead of rows. This structure allows for much better compression and storage efficiency, especially when only a subset of columns is queried.
    * I recall matlab does the same thing. Could this strange columnar storage affect the way we query the data source because I remember I had to access data element differently when working with matlab. But I did it so long ago that I couldn't remember how it works.

Efficient Compression: Due to its columnar nature, Parquet can compress data more effectively, which reduces storage costs. The same data stored in CSV can take up significantly more space.

Example: Parquet files can achieve 3x to 10x better compression than CSV files, depending on the data.

CSV:

Row-based Storage: CSV stores data row by row, meaning each row includes all the columns, even if you're interested in only a few columns.
No Compression: CSV files are plain text and do not have built-in compression, resulting in larger file sizes compared to Parquet for similar data.

**Performance for Querying and Analytics**

Parquet:

Faster Queries: Since Parquet is columnar, tools like Athena, Presto, Spark, and Hive can read only the necessary columns, making queries much faster. This is particularly beneficial when you’re dealing with large datasets, as only the needed data is loaded into memory.

Optimized for Analytics: Parquet is optimized for analytical queries, especially when combined with big data tools (like Hadoop or Spark), because it allows for predicate pushdown, meaning filters can be applied at the storage level to minimize the data read into memory.

<mark>Schema Support: Parquet files contain schema information (metadata) which ensures consistency across data and allows tools to automatically infer the structure without needing manual parsing.</mark>

CSV:

Slower Queries: Since CSV is row-based, reading the entire dataset is necessary even if only specific columns are needed, which leads to slower performance for large-scale queries. CSV is not optimized for analytics or fast data access.

No Schema: CSV files don’t include schema, so each time you process the data, you need to explicitly define the schema, which can lead to errors or inconsistencies.

**Flexibility and Schema Management**

Parquet:

Self-describing Schema: Parquet files include embedded schema information, making it easier for systems to understand and process the data without needing separate schema definitions.

Supports Nested Data: Parquet can handle complex, nested data structures (such as arrays, structs, and maps), making it well-suited for semi-structured data like JSON.

Schema Evolution: Parquet supports schema evolution, which allows changes to the data schema (such as adding new columns) without breaking existing processes or data.

CSV:

No Native Schema: CSV files do not store schema information, so schema must be inferred or defined manually, which can lead to inconsistencies, especially with large datasets or datasets with evolving structures.

Flat Data Only: CSV is a flat format and cannot handle complex or nested data types. Each column must contain data of the same type, and relationships between different pieces of data must be represented in a flat way.

**Data Integrity and Precision**

Parquet:

Data Types: Parquet supports a wide range of data types, including integer, float, string, timestamp, and more. It can store large numbers with high precision and preserve complex types like Decimal, Timestamp, etc.

Consistency: Parquet ensures consistency in data types and structures, which reduces the chances of data corruption or errors.

CSV:

Loss of Precision: Since CSV is plain text, it doesn’t inherently support complex data types like Decimal or Timestamp and may lose precision when converting or exporting from more complex formats (e.g., floating-point numbers).

Data Type Issues: When working with CSV files, it’s easy for data types to be misinterpreted (e.g., numbers stored as strings), which can lead to parsing issues or incorrect results during analysis.

**Interoperability and Ecosystem**

Parquet:

Designed for Big Data: Parquet is designed for the big data ecosystem and integrates seamlessly with tools like Apache Hadoop, Spark, Hive, Presto, and cloud data platforms (e.g., AWS Athena, Google BigQuery, Azure Synapse).

<mark>Optimized for Data Lakes: It’s the standard for data lakes, where you need to store large amounts of data in a highly efficient and query-optimized way.</mark>

CSV:

Widely Supported: CSV is universally supported and can be opened by nearly any data tool, spreadsheet program, or programming language. However, it lacks optimizations for big data processing and analytics.

**Use Case**

Parquet:

Large-scale Analytics: Ideal for storing large datasets that will be queried for analytical purposes. Parquet excels when you need to perform aggregation, filtering, or complex queries across large datasets.

Data Lakes: When you need to build a data lake for storage, processing, and querying large volumes of data, Parquet is the format of choice due to its optimized performance, scalability, and flexibility.

Efficient ETL Pipelines: Parquet is suitable for ETL (extract, transform, load) workflows, especially when working with big data tools like Apache Spark or AWS Glue.

CSV:

Simple Data: Best used for small to medium-sized datasets or when you need to export/import simple, tabular data for use in spreadsheets or quick reports.

Interchange Format: CSV is a great interchange format for sharing data between applications, especially for cases where you don’t need to process large volumes of data or perform complex queries.

**Summary Comparison**

| Feature | Parquet | CSV |
|---------|---------|-----|
| **Storage Efficiency** | High (columnar, compressed) | Low (row-based, uncompressed) |
| **Compression** | High (better compression) | Low (no inherent compression) |
| **Query Performance** | Very Fast (optimized for analytics) | Slow (needs to read entire file) |
| **Schema Support** | Yes (self-describing schema) | No (manual schema definition) |
| **Nested Data** | Supports (arrays, structs, maps) | Not supported (flat data only) |
| **Data Types** | Supports complex types and precision | Limited (prone to loss of precision) |
| **Interoperability** | Best for big data and cloud analytics | Universal (good for sharing simple data) |
| **Use Cases** | Data lakes, big data, analytics, ETL | Small data, quick exchange, spreadsheets |

**Conclusion**

Use Parquet if you're working with large datasets, performing analytics, or need high compression, performance, and schema management. It's particularly suited for big data environments and data lakes.

Use CSV for small, simple datasets or when you need to exchange data between systems with minimal overhead, and where performance isn’t a critical concern.

# Approach to Data Storage
Your approach to storing raw data in S3 for downstream analysis is sound and aligns well with modern data engineering practices. Here are some considerations and best practices to ensure your workflow is efficient and scalable:

**Best Practices for Storing Raw Data in S3**

Use Optimal File Formats:
* Parquet or ORC: Columnar storage formats are efficient for analytics and work seamlessly with Athena, dbt, and other query tools.
* JSON or Avro: Suitable for raw, nested data. You can later transform JSON into Parquet/ORC for querying.
* <mark>Consider storing both the raw (e.g., JSON) and processed (e.g., Parquet) formats.</mark>

Organize Your S3 Bucket: Use a hierarchical structure for easy querying and lifecycle management.
 ```
 s3://my-bucket/
  raw/
    stackexchange/
      yyyy=2024/
        mm=11/
          dd=25/
            part-0000.json
  processed/
    parquet/
```
Partition by commonly queried fields, such as yyyy, mm, and dd, to optimize Athena queries.

**Set Up Lifecycle Policies**
* Archive older raw data to Glacier if infrequently accessed.
* Configure expiration for raw data if you no longer need it after processing.

**Compression**
* Compress files using gzip or snappy to reduce storage costs and improve processing performance in Athena or dbt.

**For Analysis: Athena and dbt**
* Athena:
  * Create external tables on your S3 data for direct querying.
  * Use Glue Data Catalog to manage table metadata.
* dbt:
  * Use dbt’s materializations to transform raw data into analytics-ready formats (e.g., creating fact and dimension tables in S3 or a database like Redshift or Snowflake).

**For Future Analytics and Systems**
* Event-Driven Workflows:
  * Use AWS Lambda or Step Functions to trigger transformations when new data is uploaded.
* Schema Evolution:
  * If schema changes over time, use tools like AWS Glue or Apache Iceberg for schema discovery and versioning.
* Data Validation:
  * Validate and clean data during ingestion using tools like Great Expectations or custom scripts.

**Transactional Systems Consideration**
* S3 is Not Ideal for Transactional Workloads:
<mark>S3 is optimized for large-scale analytics and storage, not for frequent transactional updates or low-latency access. For transactional needs, consider loading processed data into a relational database (e.g., PostgreSQL or DynamoDB) or a data warehouse.</mark>

If your pipeline grows more complex, consider:
* ETL Tools:
  * Use tools like Apache Airflow, Dagster, or AWS Glue for managing data workflows.
* Data Lakes and Warehouses:
  * Lake Formation: Manage permissions and fine-grained access to your data lake.
  * Redshift/Snowflake/BigQuery: Complement S3 for faster query performance, especially for ad-hoc analytics.

**Conclusion**
Your approach is solid, but the key to success lies in:
* Choosing the right format and structure for your data.
* Defining clear workflows for ingestion, transformation, and analytics.
* Planning for scalability and schema evolution.

# Sample S3 Structure, Athena Query, or dbt Project

Let’s start with a basic setup and walk through these steps for a sample S3 structure, an Athena query, and a dbt project.

## Sample S3 Structure
**Organize Raw and Processed Data**

We’ll use the following structure:
```
s3://stackexchange-data/
  raw/
    yyyy=2024/
      mm=11/
        dd=25/
          raw-part-0000.json
          raw-part-0001.json
  processed/
    stackexchange/
      yyyy=2024/
        mm=11/
          dd=25/
            data.parquet
```
**How to Upload Data to S3**

Here’s a Python snippet for uploading raw data from the StackExchange API:
```
import boto3
import json
from datetime import datetime

# Initialize S3 client
s3 = boto3.client('s3')

# Replace with your bucket name and data
BUCKET_NAME = 'stackexchange-data'
RAW_FOLDER = 'raw/'

# Simulate pulling data from the API
data = {"question": "What is Python?", "votes": 42}
timestamp = datetime.now()

# Generate S3 path
s3_path = f"{RAW_FOLDER}yyyy={timestamp.year}/mm={timestamp.month:02d}/dd={timestamp.day:02d}/raw-part-0000.json"

# Upload JSON data to S3
s3.put_object(
    Bucket=BUCKET_NAME,
    Key=s3_path,
    Body=json.dumps(data),
    ContentType='application/json'
)

print(f"Data uploaded to s3://{BUCKET_NAME}/{s3_path}")
```
## Setting Up Athena

**Create a Table for Raw Data**

Use the AWS Glue Data Catalog to register your data or run a query directly in Athena. Here’s a sample query for creating a table from raw JSON files:
```
CREATE EXTERNAL TABLE stackexchange_raw (
  question STRING,
  votes INT
)
PARTITIONED BY (yyyy STRING, mm STRING, dd STRING)
STORED AS JSON
LOCATION 's3://stackexchange-data/raw/';
```

**Add Partitions**

Athena doesn’t automatically detect new partitions. Run the following query after uploading new data:
```
MSCK REPAIR TABLE stackexchange_raw;
```

Query Example

Fetch data for a specific date:
```
SELECT * 
FROM stackexchange_raw
WHERE yyyy = '2024' AND mm = '11' AND dd = '25';
```

## Setting Up dbt

**dbt Initialization**

Install dbt for your data warehouse (e.g., dbt Athena adapter for S3).

Initialize a dbt project:
```
 dbt init my_dbt_project
```

**dbt Configuration**

Edit profiles.yml to configure your connection to Athena:
```
default:
  outputs:
    dev:
      type: athena
      s3_staging_dir: s3://stackexchange-data/processed/dbt/
      region_name: us-west-2
      database: stackexchange
  target: dev
```

**dbt Model**

Create a models/processed_questions.sql file:
```
WITH cleaned AS (
    SELECT
        question,
        votes,
        CAST(votes AS INT) AS vote_count,
        CURRENT_DATE AS processed_date
    FROM {{ ref('stackexchange_raw') }}
)
SELECT *
FROM cleaned;
```

Run the model:
```dbt run```

# Create AWS Credentials on sst_admin 
<mark> AWS only allows for a maximum of 2 S3's API keys at a time</mark>

Using a .env.local file to store sensitive information like access keys is a good practice. Here's how you can do it in Python:

**Install Python Dotenv:** First, install the python-dotenv library, which allows Python to read environment variables from a .env file:
```pip install python-dotenv```

**Create a .env.local File:** Create a .env.local file in the same directory as your Python script and add your access key:
```ACCESS_KEY=your-access-key-here```

**Load and Access Environment Variables in Python:** Here's how to read the ACCESS_KEY from the .env.local file in your Python script:
```
from dotenv import load_dotenv
import os

# Load the .env.local file
load_dotenv(dotenv_path=".env.local")

# Get the access key
access_key = os.getenv("ACCESS_KEY")

# Print or use the access key
print(f"Your access key is: {access_key}")
```

**Best Practices:**

Exclude .env.local from version control: Add .env.local to your .gitignore file to avoid committing sensitive information.

Check for missing environment variables: Handle cases where the ACCESS_KEY is missing to avoid runtime errors:
```
if not access_key:
  raise ValueError("ACCESS_KEY is not set in the .env.local file.")
```

This approach keeps your keys secure and ensures your Python application can access them efficiently.


# December 2, 2024
**Maybe do the below during the meeting with Aaron**

Need secret access key to talk to s3

In the initial_eda.ipynb, why can't I run my code? I thought I already installed requests.

Play around with Poetry.

| Feature             | Poetry                      | Pip + Virtualenv           |
|---------------------|-----------------------------|----------------------------|
| **Dependency Management** | Built-in, declarative      | Manual with `requirements.txt` |
| **Virtualenv Handling** | Automatic                   | Requires `virtualenv`      |
| **Reproducibility**  | `poetry.lock` file          | Requires `pip freeze`      |
| **Publishing**       | Simplified with metadata    | Requires `setup.py`        |


**Maybe do the below during the meeting with Bobby**

Learn how to do version control for SQL

Bobby does it in 3 places:
1. metabase or snowflake worksheets: eda, poking.
2. dbt: model and transformation. The sql I'm talking about 
3. airflow files or python: pull out something.

LEARN DBT AND THEN YOU'RE OFFICIALLY "ONE OF US" -- ANALYTICS ENGINEERS.

api.stackexchange.com/docs

Outstanding Questions/To Dos

What IS The data?
EDA w/ notebook, etc.
How can we use this data (in production)?
What design best suits that use case?
Practice building a Git Repo


Eat with Bobby (reschedule)
Set up a progress tracker with clear milestones, including metrics of success (lead vs lag metric)
Nov 21, 2024
Bobby propose using Poetry. Explore it and get back to him next time
Second pass. Don’t prioritize it but at some point it’ll be cool for us to try
Figure out how to jump between terminal and code environment in vscode.

Next time, how to set up credentials for boto3 s3.
Nov 21, 2024
Bobby propose using Poetry. Explore it and get back to him next time
Second pass. Don’t prioritize it but at some point it’ll be cool for us to try
Figure out how to jump between terminal and code environment in vscode.

Next time, how to set up credentials for boto3 s3.

maybe this: https://stackoverflow.com/questions/45981950/how-to-specify-credentials-when-connecting-to-boto3-s3



How do you do version control for sql

Start using vs code to write this doc (in vs code as mark down) this gives me a chance to use vim
How do I share that with Bobby?
Ohhh, Bobby will need to start using git if he wants to edit this document too. Win-Win-Win-Win!


___ 
https://us-east-1.console.aws.amazon.com/s3/buckets/stackexchangegardening?region=us-east-1&bucketType=general&tab=objects

--- 
Common Commands with requirements.txt:
Generate requirements.txt: Save currently installed packages to a file:
bash
Copy code
pip freeze > requirements.txt


Install from requirements.txt: Install all dependencies:
bash
Copy code
pip install -r requirements.txt


Upgrade Packages: To update all packages based on requirements.txt:
bash
Copy code
pip install --upgrade -r requirements.txt

----

VENV chatgpt notes:
Creating and using a virtual environment in Python is straightforward. Below are the steps and most commonly used commands:

1. Create a Virtual Environment
Run the following command in your project directory:
python -m venv venv

python: Ensure this is the correct Python version you want to use (e.g., python3 or python3.x).
venv: This is the name of the virtual environment directory (can be any name, like .venv).

2. Activate the Virtual Environment
On Windows (Command Prompt):
 .\venv\Scripts\activate


On Windows (PowerShell):
 .\venv\Scripts\Activate.ps1


On macOS/Linux:
 source venv/bin/activate



3. Install Packages
After activation, install Python packages with pip:
pip install <package-name>

Example:
pip install requests


4. Save Installed Packages
To save the list of installed packages to a requirements.txt file:
pip freeze > requirements.txt


5. Deactivate the Virtual Environment
When you're done, deactivate the environment:
deactivate


6. Recreate the Environment
If you have a requirements.txt file and need to recreate the environment:
Create and activate a new virtual environment.
Install all dependencies from requirements.txt:
 pip install -r requirements.txt



7. Remove a Virtual Environment
Simply delete the venv folder:
rm -rf venv

(On Windows, use rmdir /s /q venv).

Most Common Commands Summary
Command
Description
python -m venv venv
Create a virtual environment.
source venv/bin/activate
Activate on macOS/Linux.
.\venv\Scripts\activate
Activate on Windows CMD.
pip install <package-name>
Install a package.
pip freeze > requirements.txt
Save dependencies.
deactivate
Deactivate the environment.

Let me know if you'd like help with any of these commands!


Nov 18, 2024
Setup Lastpass AWS credentials for Huy
Created Stack Exchange S3 bucket
Started Venv process for test script writing to S3

Python script to extract data and store in S3 → Athena to query → Tableau
Simplest way to get started.

11/18/2024: run script, get my data DS1 (.parquet, .csv) and stored in S3

11/19/2024: run script, get my data DS2
Nov 11, 2024
Helped Huy install live share on VS Code.

What are we going to use this data for?
Analytics engineer: learn dbt (Bobby is very good at it)
Dbt is a substitute to Athena.
Think about ELT
Bobby thinks I’ll have a better chance to be a visual analytics.

Figure out what Athena is, how it works, and how to play with it.
Can ask

Send emails to Bobby and Aaron if I have questions.

Don’t mention Bobby in my journal.
Nov 4, 2024
Talked about Project and next steps

Outstanding Questions/To Dos

What IS The data?
EDA w/ notebook, etc.
How can we use this data (in production)?
What design best suits that use case?
Practice building a Git Repo


If this week, Huy can do EDA

Conformed on Internship Expectations 
Huy's Expectations

EDA progress:
With chatgpt, it’s fairly easy to get the data.
No API is required but there’s something about rate limit
A lot of information comes back:tags, question title, question content, answers, who asked the questions, who answered the questions, question ranking, etc.
An easy analysis we can do is to visualize stats such as what tags showed up the most, user’s statistics (who has the most questions / answers, won the most badges, etc. – basically, who’s the most credible). Tableau to visualize the data.
Reach out to those people to validate our bucket of ideas
Ask them to try out the web site.
An easy idea to get our name out there:
Once we have a good dataset, maybe reach out to Future Fridays to see if they can help visualize a sample of this dataset. It’s free!
Need help with:
What’s the best way to store this data? My interest is in learning more about AWS but the learning curve seems very steep.
How you want to store the data depends on how you want to use the data
It’s better to look at the whole data life cycle and do backwards engineering.
Maybe reach out to someone who has experience? Bobby, Aaron, (the instructor for a course I’m taking, Morgan Willis), Chip Huyen.
Goal: 
By the end of the next session, walk away with something to read or try.
Screen that will receive from.
Help set up my dev corner.
Start writing my internship journal to post on linkedin. (I need to write 2 journals already).
Thoughts:
I have a government-sponsored account with Coursera, so I can take any courses on that platform that I want. As we’re building the data architect for this project, I want to take some courses to help me become a better data engineer. Can we review a couple of courses on Coursera? If you see anything helpful for this project, please recommend it to me.
If we have time for chatbot, I think we can leverage free GPU or TPU from kaggle. It’s actually very easy to do. Google offers Google AI Studio https://aistudio.google.com/ completely free for developers.
