FROM eclipse-temurin:21-jdk AS builder
WORKDIR /src
COPY RulesServer.java .
RUN javac -d /classes RulesServer.java
FROM eclipse-temurin:21-jre
COPY --from=builder /classes /app/classes
EXPOSE 8090
ENV PORT=8090
CMD ["java", "-cp", "/app/classes", "RulesServer"]
