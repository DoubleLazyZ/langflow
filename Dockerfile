FROM python:3.10-slim

RUN apt-get update && apt-get install gcc g++ git make -y && apt-get clean \
	&& rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH
EXPOSE 7860
WORKDIR $HOME/app

COPY --chown=user . $HOME/app


RUN pip install git+https://github.com/logspace-ai/langflow.git -U --user
# RUN pip install langflow>==0.6.0 -U --user
# RUN pip install langflow==0.6.3a3 -U --user
RUN pip install langchain==0.0.345
CMD ["python", "-m", "langflow", "run", "--host", "0.0.0.0", "--port", "7860"]
