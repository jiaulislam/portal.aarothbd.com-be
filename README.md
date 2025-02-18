
![Aarothbd.com](/images/banner.png)

# AAROTHBD

Backend Project for the 'aarothbd.com'. This application designed as Monolith project as this is just a MVP.

### Operations:
- Core Admin (Default Django Admin)
- Central Admin( Customer Admin Panel)
- Company Portal
- eCommerce

### Tech:
- Django
- Django Rest Framework
- PostgreSQL
- Custom Authentication System (CookieBased Authentication)

# Quick Start Demo

![Swagger Preview](/images/swagger.png)

This Project relies on the `UV` package manager to manage dependency. Installation instructions for `uv` can be found [Here](https://docs.astral.sh/uv/getting-started/installation/).

- clone the repository
```bash
git clone https://github.com/jiaulislam/portal.aarothbd.com-be
```
- visit into the directory
```bash
cd portal.aarothbd.com-be
```
- make a `.env` file from given example env file and set the variables with your own
```bash
cp .env.example .env
```
- install dependencies with `uv`
```bash
uv sync
```
- run the project
```bash
uv run python manage.py runserver
```
