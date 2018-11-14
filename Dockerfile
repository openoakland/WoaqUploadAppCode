FROM python:3.6.7

WORKDIR /woaq

COPY requirements.txt .
COPY Assets Assets
COPY examples examples
COPY joiner_scripts joiner_scripts
COPY templates templates
COPY age.html .
COPY Procfile .
COPY render_template.html .
COPY runtime.txt .
COPY web.py .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP web.py
ENV FLASK_RUN_PORT 4555

EXPOSE 4555

CMD ["flask", "run", "--host", "0.0.0.0"]
