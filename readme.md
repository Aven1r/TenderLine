<div align='center' >
<img src='docs/images/Frame 90.svg' width='30%'>
</div>
<h1 align='center'>TenderLine</h1>

TenderLine - service for communication between the supplier and the customer within the framework of agreeing on a future contract. Chat messages are forms for making changes to the contract, and as a result, both participants receive a ready-generated PDF document. There is also support for notifications of new messages via [telegram bot](https://t.me/tender_line_bot) and mail. 


## ✨ Technologies
- [FastApi](https://fastapi.tiangolo.com)
- [Aiogram](https://aiogram-birdi7.readthedocs.io)
- [Docker](https://www.docker.com/)
- [Clean JS]()

## ⚙️ Installation
### Requirements
To install and run the project, you need [Python](https://www.python.org) 3.10.5+

### Installation and launch of the project
#### Python way
Clone the project:
```sh
git clone https://github.com/NikitaKrylov/TenderLine.git
cd TenderLine
```
Create virtual env and install requirements:
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Start the project
```sh
uvicorn backend.api.app:app --host 0.0.0.0 --port 8000
```
#### Docker way
Clone the project:
```sh
git clone https://github.com/NikitaKrylov/TenderLine.git
cd TenderLine
```
Startup docker container:
```sh
docker compose up -d
```

## Contributing
if you have any ideas to improve the project or its individual components, then write [here](https://t.me/idoverchiviiloh) or make pull requests


## To do
- [x] Push project
- [ ] Fix all


## Project Team
MISIS 52

- [Крылов Никита](https://github.com/NikitaKrylov) — Python Backend Developer
- [Андрей Кадомцев](https://github.com/Aven1r) — Python Microservices Developer
- [Кристина Егорова](https://github.com/1Bermud) — Front-End Engineer 
- [Андрей Тычинин](https://t.me/yyyoner) — UI Designer
- [Брежнев Артем](https://t.me/dewerrr) — Presentation Designer
