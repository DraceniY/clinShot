FROM ubuntu:18.04

RUN apt-get update 
RUN pip install -r requirements.txt
RUN python setup.py build_ext --inplace

CMD bash run.sh
