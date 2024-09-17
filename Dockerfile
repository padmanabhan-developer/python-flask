FROM python:3.12.5
WORKDIR /app
COPY . .
SHELL ["/bin/bash", "-c"]
RUN rm -rf ansible_gateway
RUN python3 -m venv ansible_gateway
RUN source ansible_gateway/bin/activate
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt
EXPOSE 8443
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8443", "-w", "4"]