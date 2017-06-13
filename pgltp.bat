REM pg local to production

set PGUSER=pychatline

set PGPASSWORD=P1990ychat

pg_dump --no-acl --no-owner -h localhost -U pychatline pychatline > pychatline.dump

heroku pg:psql < pychatline.dump

