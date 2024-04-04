
# Mac troubleshooting
If you get an error like `OCI runtime create failed: runc create failed: unable to start container process: exec: "cd": executable file not found in $PATH: unknown`
when bringing up the database, you need to set the userid of your data directories.

From the docs:
> As this is a non-root container, the mounted files and directories must have the proper permissions for the UID 1001

```bash
sudo dscl . create /Users/bitnami_postgres PrimaryGroupID 20
sudo dscl . create /Users/bitnami_postgres UniqueID 1001
sudo chown -R 1001:1001 db
sudo chmod -R 777 db
```


Docker Lock file: ~/Library/Application\ Support/com.docker.compose/plants-api.pid

# Alembic
## Create a migration
For this to work like you want, back the database up to before the changes you want existed. The info will be generated from models.

`alembic revision --autogenerate -m "subject action"`

## Migrate
`alembic upgrade head`
