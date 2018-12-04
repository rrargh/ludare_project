FROM django:python3-onbuild
ADD . /ludare_project/ludare_app
WORKDIR /ludare_project/ludare_app
EXPOSE 8000
RUN pip install --upgrade pip && pip install -r requirements.txt
ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
