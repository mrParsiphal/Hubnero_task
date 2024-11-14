FROM python:3.12


MAINTAINER MrParsiphal


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ="Europe/Moscow"


VOLUME ./getusd/:/getusd/

RUN pip install -r requirements.txt
RUN pip install gunicorn
CMD cd getusd
CMD python3 manage.py manage.py makemigrations
CMD python3 manage.py migrate
CMD python3 manage.py loaddata fixtures
CMD cd ../
CMD gunicorn -b 0.0.0.0:80 getusd.getusd.wsgi:application


EXPOSE 80