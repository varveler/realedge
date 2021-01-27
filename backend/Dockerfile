FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /backend
COPY requirements.txt /backend
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' tasksuser
ADD wait-for-it.sh /backend/
RUN chmod +x /backend/wait-for-it.sh

COPY . /backend/
