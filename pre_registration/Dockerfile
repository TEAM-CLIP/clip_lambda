FROM public.ecr.aws/o1r5t7k5/chiksnap/common/python:3.9

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

COPY . ${LAMBDA_TASK_ROOT}

CMD ["lambda_function.handler"]