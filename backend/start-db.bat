@echo off
REM Script to start PostgreSQL database for REGIQ backend

docker run -d ^
  --name regiq-postgres ^
  -e POSTGRES_DB=regiq_backend ^
  -e POSTGRES_USER=regiq_user ^
  -e POSTGRES_PASSWORD=regiq_password ^
  -p 5432:5432 ^
  -v regiq_postgres_data:/var/lib/postgresql/data ^
  postgres:13

echo PostgreSQL database started for REGIQ backend
echo Database: regiq_backend
echo User: regiq_user
echo Password: regiq_password