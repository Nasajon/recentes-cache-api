FROM arquiteturansj/flask:2.2

WORKDIR /var/www/html

COPY . /var/www/html

EXPOSE 5001

RUN python3 -m pip install -r /var/www/html/requirements.txt --no-cache-dir

CMD python3 /var/www/html/src/wsgi.py
