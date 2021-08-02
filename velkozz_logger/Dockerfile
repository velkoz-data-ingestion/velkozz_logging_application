FROM python

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Copying application to the container and setting working directory:
COPY . /home/logger/
WORKDIR /home/logger/

# Running all of the python install components:
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "manage.py", "wsgi.py"]

EXPOSE 5000