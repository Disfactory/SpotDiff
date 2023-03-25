#modified by sourbiebie for SpotDiff
#from postgres(SQL + linux), install miniconda, flask, and pip
FROM postgres

# System packages 
RUN apt-get update && apt-get install -y curl


# Install miniconda to /miniconda
RUN curl -LO https://repo.anaconda.com/miniconda/Miniconda3-py38_4.9.2-Linux-x86_64.sh
RUN bash Miniconda3-py38_4.9.2-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda3-py38_4.9.2-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

# System packages 
RUN apt-get update && apt-get install -y \
    vim \
    git \
    libpq-dev \
    python-dev \    
		python3-pip    
		
		
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/