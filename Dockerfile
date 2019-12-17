FROM python:3.7-slim

# define variaveis
ENV APP_HOME /app

# prepara ambiente
RUN mkdir $APP_HOME

# define diretorio de trabalho
WORKDIR $APP_HOME

# copia source do projeto
COPY . .

# instala gerenciador de pacotes do python
RUN pip install pipenv

# instala dependencias do projeto
RUN pipenv install --system --deploy

# executa o servidor de aplicacao
# CMD python manage.py runserver 0.0.0.0:$PORT
CMD gunicorn --bind :$PORT --workers 1 --threads 8 core.wsgi
