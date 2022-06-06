FROM eclipse-temurin:11

ARG assignment_id

COPY uploads/${assignment_id}/*.java /opt/test/
COPY dockerfiles/java.sh /opt/test/

WORKDIR /opt/test/
RUN chmod +x java.sh
ENTRYPOINT ["./java.sh"]