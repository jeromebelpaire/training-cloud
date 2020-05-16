FROM python:3
COPY . .
RUN pip install -r requirements.txt --trusted-host pypi.python.org
EXPOSE 5555
ENV PYTHONPATH .
CMD python ./App/app.py