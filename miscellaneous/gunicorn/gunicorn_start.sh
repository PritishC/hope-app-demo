#!/bin/bash

NAME="django_jobs"                                # Name of the application
DJANGODIR=$HOME/web_deploy/jobs-app       # Django project directory
SOCKFILE=/tmp/gunicorn.sock   # we will communicte using this unix socket
USER=ubuntu                                       # the user to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_WSGI_MODULE=django_jobs.wsgi               # WSGI module name

echo "Starting $NAME as `whoami`"

# Create the run directory if it doesn't exist
RUNDIR=$SOCKFILE
# test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /usr/local/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
