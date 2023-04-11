FROM python:3.10-slim

# this is the starting directory inside the container
WORKDIR /opt/sde/

# lets us import from folders inside /src/loader directly
ENV PYTHONPATH=/opt/sde

# install python requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# connect to prefect cloudPREFECT_API_KEY} --workspace ${PREFECT_WS}
# RUN prefect cloud login --key $PREFECT_API_KEY --workspace $PREFECT_WS
# RUN prefect cloud login --key pnu_ev71fvNLnW2bktM2uFyIQenYJRjhLK02o2aE --workspace amirzahreddinegmailcom/workspace-1

# COPY init_prefect_cloud.sh .
# RUN chmod +x sde/containers/loader/init_prefect_cloud.sh

# copy over the entire code folder to docker
COPY ../.. /opt/sde

# specify the entry command
# calling `uvicorn main:app --reload` from the fastapi example site
# code is inside the src directory
# also specifying host and port

# CMD ["tail", "-f", "/dev/null"]


# docker rm prefect-container
# docker build -t prefect-image-1 .
# docker run -v ${pwd}/src --name prefect-container -d prefect_docker_test_1_app
