FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

RUN mkdir -p ${LAMBDA_TASK_ROOT}/common

# copy common package to lambda task root's common directory
COPY *.py ${LAMBDA_TASK_ROOT}/common