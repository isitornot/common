FROM python:3.6-onbuild
MAINTAINER Trevor R.H. Clarke <trevor@notcows.com>

COPY auth/ /opt/app/
WORKDIR /opt/app

EXPOSE 9000
CMD python main.py
