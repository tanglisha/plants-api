# Development
Set up pre-commit: `pre-commit install --install-hooks`

## Docker setup
### Database
`docker compose up -d db`

### Application
`docker compose watch app`

The application will be at `http://localhost:8001` if you don't change the port
