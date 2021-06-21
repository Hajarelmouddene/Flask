# pull official base image

FROM postgres:13-alpine

#run create.sql on init
# adding create.sql to the "docker-entrypoint-initdb.d" directory in the container
ADD create.sql /docker-entrypoint-initdb.d 
