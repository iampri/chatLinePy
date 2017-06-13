REM pg backup to local

heroku pg:backups:capture

heroku pg:backups:download

pg_restore --verbose --clean --no-acl --no-owner -h localhost -U pychatline -d pychatline latest.dump

