up:
	docker-compose up --build

backend:
	docker-compose up --build backend

down: 
	docker-compose down

permisos:
	sudo chown -R $$USER:$$USER backend/migrations
	sudo chown $$USER:$$USER backend/alembic.ini

migrate:
	docker exec -it lapiz_backend alembic upgrade head

reset:
	docker-compose down -v
	docker-compose up --build