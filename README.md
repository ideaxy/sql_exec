# sql_exec
Execute the SQL statement and save the result


# Usage
`python3 main.py <connect information> <database type>`

- connect information:user/password@ip:port/service_name
- database type:oracle or mysql

Create a file named exec.sql in current directory.
The main.py file uses the connection information and the SQL statements in the sql_exex.sql file to run and writes the query results into the select_results.txt file.
Currently, only SELECT queries are supported.

