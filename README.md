# AC_GroupTest

## Bithumb API 를 받아 Web 상에 차트를 표시합니다.

### Architecture

Back & middleware : Python Flask
DB : Redis
Front : ChartJS, JavaScript 
Runtime : Docker Engine

### Describe

├── Dockerfile
├── README.md
├── data
│   └── dump.rdb
├── docker-compose.yaml
└── pyweb-app
    ├── crawling_data.py
    ├── custom_module
    │   ├── __pycache__
    │   │   └── get_tools.cpython-311.pyc
    │   └── get_tools.py
    ├── index.py
    ├── requirements.txt
    └── templates
        ├── bubble_chart.html
        ├── linechart.html
        ├── otherchart.html
        └── treemap.html

/data : crawling_data.py를 통해 수집하는 디렉터리입니다. Redis와 mount됩니다.
/pyweb-app : Flask 코드가 위치한 디렉터리입니다.
/pyweb-app/index.html : Flask 코드입니다.
/pyweb-app/crawling_data.py : bithumb API 호출을 통해 얻은 데이터를 Redis에 적재하는 스크립트입니다.
/pyweb-app/custom_module: middleware 역할을 하는 함수들을 모아놓는 디렉터리입니다.
/pyweb-app/templates : html 페이지가 위치합니다.

### Web Page

- 종목별 차트 : 단순 차트를 확인하실 수 있는 페이지 입니다. 라인과 바 차트의 경우는, 추세를 보는데 중점을 두어 min-max scaling을 통해서 값을 정규화하였습니다.

- 트리맵 : 전체 종목들의 정보 별, 비율을 확인할 수 있습니다.

- 버블차트 : 거래량 - 거래금액 - 가격변동을 한 번에 확인할 수 있습니다.


### 실행방법

docker-compose 환경에 맞추어 한 번에 확인하실 수 있도록 설계되었습니다.
시작 디렉터리에서 docker-compose up 명령을 통해 실행합니다.
crawling_data.py는 별도로 host의 crontab에 등록하여 정기적으로 데이터를 모읍니다.