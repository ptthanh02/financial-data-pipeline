# Financial Data Pipeline

> An automated ETL (Extract, Transform, Load) system for collecting and processing Vietnamese stock market data using Apache Airflow, PostgreSQL, and Apache Superset.

## 🚀 Overview

This project implements a comprehensive data platform for financial data processing, specifically designed to collect, store, and visualize Vietnamese stock market data. The system utilizes modern data engineering tools to create an automated pipeline that runs daily to fetch stock prices from VNDirect API and presents them through interactive dashboards.

![architecture diagram](image.png)

## 🏗️ Architecture

The system follows a modern data platform architecture with three main components:

### 1. Data Collection Layer
- **Apache Airflow**: Orchestrates the ETL pipeline with scheduled DAGs
- **VNDirect API**: Data source for Vietnamese stock market information
- **Daily Schedule**: Automated data collection at 00:00 daily

### 2. Data Storage Layer
- **PostgreSQL**: Primary database for storing stock price data
- **Docker Compose**: Container orchestration for database deployment
- **Data Validation**: Duplicate prevention and incremental loading

### 3. Data Visualization Layer
- **Apache Superset**: Interactive dashboards and data exploration
- **Real-time Analytics**: Live stock market insights
- **Flexible Filtering**: Advanced data querying capabilities

## 📊 Features

- ✅ **Automated Data Collection**: Daily scheduled pipeline for stock data ingestion
- ✅ **Data Quality Assurance**: Duplicate detection and incremental updates
- ✅ **Scalable Architecture**: Containerized deployment with Docker
- ✅ **Interactive Dashboards**: Rich visualizations with Apache Superset
- ✅ **Multi-Stock Support**: Tracks 10 major Vietnamese stocks
- ✅ **Historical Data**: Complete data from 2020-01-01 to present
- ✅ **RESTful API Integration**: Seamless connection to VNDirect API

## 🎯 Monitored Stocks

The system currently tracks the following Vietnamese stocks:
- **VNM** (Vinamilk)
- **VCB** (Vietcombank)
- **VIC** (Vingroup)
- **BID** (BIDV)
- **SSI** (SSI Securities)
- **PNJ** (PNJ Gold)
- **HPG** (Hoa Phat Group)
- **GAS** (Gas South)
- **MWG** (Mobile World)
- **VJC** (VietJet Air)

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Orchestration** | Apache Airflow 2.8.1 | Workflow management and scheduling |
| **Database** | PostgreSQL 13 | Data storage and management |
| **Visualization** | Apache Superset | Interactive dashboards |
| **Message Broker** | Redis | Task queue for Celery |
| **Containerization** | Docker & Docker Compose | Environment management |
| **Programming** | Python 3.x | ETL logic and data processing |

## 📦 Installation & Setup

### Prerequisites
- Docker and Docker Compose installed
- Minimum 4GB RAM and 2 CPU cores
- At least 10GB free disk space

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/financial-data-pipeline.git
   cd financial-data-pipeline
   ```

2. **Set up environment variables**
   ```bash
   # Create .env file
   echo "AIRFLOW_UID=$(id -u)" > .env
   echo "_AIRFLOW_WWW_USER_USERNAME=admin" >> .env
   echo "_AIRFLOW_WWW_USER_PASSWORD=admin123" >> .env
   ```

3. **Start the services**
   ```bash
   # Initialize Airflow database
   docker-compose up airflow-init
   
   # Start all services
   docker-compose up -d
   ```

4. **Access the applications**
   - **Airflow UI**: http://localhost:8080 (admin/admin123)
   - **Superset UI**: http://localhost:8091
   - **PostgreSQL**: localhost:5432 (airflow/airflow)

### Service Configuration

The system deploys the following services:

| Service | Port | Description |
|---------|------|-------------|
| Airflow Webserver | 8080 | DAG management interface |
| Apache Superset | 8091 | Data visualization platform |
| PostgreSQL | 5432 | Database server |
| Redis | 6379 | Message broker (internal) |
| Flower | 5555 | Celery monitoring (optional) |

## 🔄 Pipeline Workflow

### ETL Process Flow

1. **Extract**: 
   - Scheduled daily at 00:00
   - Fetches data from VNDirect API
   - Handles JSON response processing

2. **Transform**:
   - Data validation and cleaning
   - Duplicate detection logic
   - Incremental loading strategy

3. **Load**:
   - Creates `stock_price` table if not exists
   - Inserts new records only
   - Maintains data integrity

**[Note: Add Airflow DAG graph screenshot here]**

### Database Schema

```sql
CREATE TABLE stock_price (
    code VARCHAR(50),           -- Stock symbol
    date DATE,                  -- Trading date
    time TIME,                  -- Trading time
    floor VARCHAR(50),          -- Exchange floor
    type VARCHAR(50),           -- Stock type
    basicPrice FLOAT,           -- Basic price
    ceilingPrice FLOAT,         -- Ceiling price
    floorPrice FLOAT,           -- Floor price
    open FLOAT,                 -- Opening price
    high FLOAT,                 -- Highest price
    low FLOAT,                  -- Lowest price
    close FLOAT,                -- Closing price
    average FLOAT,              -- Average price
    -- Additional price fields...
    nmVolume FLOAT,             -- Normal volume
    nmValue FLOAT,              -- Normal value
    ptVolume FLOAT,             -- Put-through volume
    ptValue FLOAT,              -- Put-through value
    change FLOAT,               -- Price change
    adChange FLOAT,             -- Adjusted change
    pctChange FLOAT             -- Percentage change
);
```

## 📈 Data Visualization

### Dashboard Features

The Apache Superset dashboard provides comprehensive stock market analytics:

![Superset dashboard](image-1.png)

- **Adjusted Close Prices**: Time series visualization of stock performance
- **Trading Volume Analysis**: Volume distribution across different stocks
- **Price Movement Tracking**: OHLC (Open, High, Low, Close) analysis
- **Volume Distribution**: Pie chart showing market share by volume
- **Price vs Volume Correlation**: Scatter plot analysis
- **Detailed Stock Data**: Tabular view with all metrics

### Key Metrics Tracked

- Daily price movements (Open, High, Low, Close)
- Trading volumes (Normal and Put-through)
- Price changes (Absolute and percentage)
- Average prices and adjusted values
- Market capitalization indicators

**[Note: Add SQL query interface screenshot here - Image 3]**

## 🔧 Configuration

### Airflow Configuration

Key Airflow settings in the DAG:

```python
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now() - timedelta(minutes=9),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Schedule: Daily at midnight
schedule_interval='0 0 * * *'
```

### Database Connection

The system uses PostgreSQL with the following connection:
- **Host**: postgres (Docker service name)
- **Port**: 5432
- **Database**: airflow
- **Username**: airflow
- **Password**: airflow

### API Configuration

VNDirect API endpoint:
```python
url = "https://finfo-api.vndirect.com.vn/v4/stock_prices"
params = {
    'sort': 'date',
    'q': 'code:VNM,VCB,VIC,BID,SSI,PNJ,HPG,GAS,MWG,VJC',
    'size': 9990,
    'page': 1
}
```

## 🚀 Usage

### Running the Pipeline

1. **Monitor DAG Status**:
   - Access Airflow UI at http://localhost:8080
   - Check `crawl_stock_data` DAG status
   - View task logs and execution history

2. **Data Verification**:
   ```sql
   -- Check latest data
   SELECT * FROM stock_price 
   ORDER BY date DESC 
   LIMIT 10;
   
   -- Count records by stock
   SELECT code, COUNT(*) as record_count 
   FROM stock_price 
   GROUP BY code;
   ```

3. **Dashboard Access**:
   - Open Superset at http://localhost:8091
   - Navigate to "Daily Stocks" dashboard
   - Explore interactive charts and filters

### Manual Execution

To run the pipeline manually:

```bash
# Access Airflow CLI
docker-compose exec airflow-webserver airflow dags trigger price_stock

# Check task status
docker-compose exec airflow-webserver airflow tasks list price_stock
```

## 📁 Project Structure

```
financial-data-pipeline/
├── docker-compose.yaml         # Docker services configuration
├── Dockerfile                  # Custom Airflow image
├── dags/
│   └── price_stock.py          # Main ETL pipeline DAG
├── logs/                       # Airflow logs
├── plugins/                    # Airflow plugins
├── config/                     # Configuration files
├── .env                        # Environment variables
└── README.md                   # Project documentation
```

## 🔍 Monitoring & Troubleshooting

### Service Health Checks

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs airflow-webserver
docker-compose logs postgres
docker-compose logs superset

# Restart services
docker-compose restart
```

### Common Issues

1. **Memory Issues**: Ensure at least 4GB RAM available
2. **Port Conflicts**: Check if ports 8080, 8091, 5432 are free
3. **Database Connection**: Verify PostgreSQL is running and accessible
4. **API Timeouts**: Check VNDirect API availability

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Apache Airflow** - Workflow orchestration platform
- **Apache Superset** - Data visualization and exploration
- **VNDirect** - Stock market data API provider
- **PostgreSQL** - Reliable database system
- **Docker** - Containerization platform
