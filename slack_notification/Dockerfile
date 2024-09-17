FROM public.ecr.aws/o1r5t7k5/chiksnap/common/python:3.9

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

RUN mkdir -p ${LAMBDA_TASK_ROOT}/recommend
RUN mkdir -p ${LAMBDA_TASK_ROOT}/pre_registration

COPY *.py ${LAMBDA_TASK_ROOT}
COPY recommend ${LAMBDA_TASK_ROOT}/recommend
COPY pre_registration ${LAMBDA_TASK_ROOT}/pre_registration

EXPOSE 8080

CMD ["lambda_function.handler"]