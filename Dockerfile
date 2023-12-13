FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY Dishes /code/

CMD ["python", "DishesService.py"]