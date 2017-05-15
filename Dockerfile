FROM python:3-onbuild

RUN pip install .

ENV API_ROOT=https://sse.rit.edu/api/v2/

VOLUME /qmail

CMD ["qmail-manager"]
