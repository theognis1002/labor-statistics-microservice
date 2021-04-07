# Datapeople Project - H1B Data FY2019 API

### Dependencies
1. docker
1. docker-compose
___
### Setup
1. Install docker & docker-compose on Ubuntu machine
    - `chmod +x ./setup_env.sh`
    - `./setup_env.sh`
1. `docker-compose up`
1. In separate terminal, run import script in an interactive terminal:
    - `docker ps`
      - get `container_id` for app service
    - `docker exec -it <container_id> sh`
    - `python utils/import.py`
      - import script may take awhile depending on the amount of CPU/RAM available
___
### Usage

1.  Inputs *(may be sent as a json body or as query parameters)*:

    - Title query text (e.g. "software engineer" or "java")
    - Location query text (e.g. "new york city", "Portland, Maine")
    
    ###### Example cURLs:
    ```
    curl --request POST \ --url 'http://localhost:5000/salary?location=NY&job_title=software'
    ```
    ```
    curl --request POST \
    --url http://localhost:5000/salary \
     --header 'Content-Type: application/json' \
     --data '{
    "job_title": "manager",
    "location": "new york"
    }'
    ```

1.  Outputs:
    -   Number of results
    -   Mean salary
    -   Median salary
    -   25% percentile salary
    -   75% percentile salary

        ###### Example output:
    ```
    {
      "num_results": 5,
      "statistics": {
        "mean_salary": {
          "value": 128899.6
        },
        "median_salary": {
          "values": {
            "50.0": 125000.0
          }
        },
        "salary_percentiles": {
          "values": {
            "25.0": 103377.0,
            "75.0": 142447.5
          }
        }
      }
    }
    ```
___
### Additional Notes
1. Technologies used:
  - `docker`
  - `docker-compose`
  - `flask`
  - `gunicorn`
  - `Elasticsearch`
  - `nginx`
  - `AWS EC2`
1. Currently deployed on an AWS EC2 instance with data imported already here: 
  - `http://3.129.60.49`
1. If deployed on a VM, the security group must allow incoming TCP requests on port 80.