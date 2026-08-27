# AWS Database Connection Examples

This project contains simple starter examples for connecting to AWS databases using Python.

The examples cover:

- Amazon Timestream
- Amazon RDS
- Amazon Athena

There are two versions of each example.

# ------------------- Folder structure -------------------

```text
database_examples/
│
├── 01_simple_local/
│   ├── Timestream.py
│   ├── RDS.py
│   ├── Athena.py
│   └── README.md
│
└── 02_aws_compatible/
    ├── Timestream.py
    ├── RDS.py
    ├── Athena.py
    └── README.md

# SSO MUST BE SET UP BEFORE:

    data-science
    prod-timestream


# AWS Database Examples

Simple Python examples for connecting to:

- AWS Timestream
- AWS RDS
- AWS Athena

# ------------------- Folders -------------------

01_simple_local
Use this version when running the scripts locally. Start here.

02_aws_compatible
Use this version when the code needs to work both locally and in AWS/CloudFormation.

# ------------------- Install -------------------

Install the required packages:

pip install boto3 pymysql PyAthena

For Timestream:

pip install boto3

# ------------------- AWS Profiles -------------------

The local examples use AWS profiles.

Check your profiles with:

aws configure list-profiles

The examples currently use:

data-science
prod-timestream

# ------------------- Run -------------------

Open the folder in Visual Studio Code.

Open:

Terminal > New Terminal

Run an example:

python Timestream.py

or:

python RDS.py

or:

python Athena.py

# ------------------- Start Here -------------------

If you are new to the project:

1. Start with 01_simple_local
2. Run Timestream.py
3. Try changing the query
4. Try RDS.py
5. Try Athena.py
6. Look at 02_aws_compatible afterwards

# ------------------- Important -------------------

Do not put AWS passwords, access keys, secret keys or database passwords directly into the code.

Use AWS profiles and Secrets Manager.

If you have connection or permission issues, check your AWS profile or ask savan.
# starter_code
# starter_code
# starter_code
