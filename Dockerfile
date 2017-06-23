FROM python:2.7.12

ENV WORKDIR /opt/alert2sms

RUN pip install tornado \
  && useradd python

EXPOSE 8081

COPY . ${WORKDIR}
RUN chmod +x ${WORKDIR}/alert2sms.py ${WORKDIR}/entrypoint.sh \
  && chown -R python ${WORKDIR}

WORKDIR ${WORKDIR}
USER python
ENTRYPOINT [ "/opt/alert2sms/entrypoint.sh" ]
CMD [ "alert2sms.py" ]
