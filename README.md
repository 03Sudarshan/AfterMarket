# AfterMarket

A high-throughput, containerized REST API backend engine architected to handle real-time asset listings, transactional state management, and highly concurrent bidding cycles. Built using a decoupled microservices-ready topology, this engine guarantees strict relational data consistency and sub-second transaction routing under high database concurrency profiles.

---

## 🏗️ System Architecture & Cloud Topology

The application is engineered around an isolated, multi-tier cloud deployment topology to guarantee high availability, strict security boundary isolation, and independent layer scalability:

*   **Edge & Traffic Routing Layer:** Public ingress is managed via **Amazon Route 53** passing traffic down to an **Application Load Balancer (ALB)** handling SSL/TLS termination.
*   **Public DMZ Proxy Layer:** High-performance **Nginx** reverse-proxy containers sit within public subnets to serve static configurations and forward dynamic upstream requests to the internal compute tier.
*   **Isolated Compute Tier (Private Subnets):** The backend core application running inside **Docker containers** handles heavy transactional business logic completely shielded from direct public internet exposure.
*   **Data Persistence Layer (Database Subnets):** A secure **Amazon RDS PostgreSQL** deployment manages relational storage, isolated completely via strict security group rules allowing inbound traffic *only* from the compute tier.

---

## 🛠️ Core Technology Stack

*   **Language & Core Runtime:** Python 3.11 / FastAPI (Asynchronous Server Gateway Interface)
*   **Data Persistence & ORM:** PostgreSQL / SQLAlchemy ORM (Connection-pooled)
*   **Containerization & Orchestration:** Docker / Docker Compose
*   **Target Cloud Infrastructure:** AWS (EC2, ALB, RDS, Route 53, IAM Security Zones)

---

## 📁 Repository Directory Blueprint

```text
aftermarket/
├── .github/
│   └── workflows/
│       ├── backend-ci.yml       # Automates linting, formatting, and unit tests
│       └── security-scan.yml    # Scans dependencies for known vulnerabilities
├── backend/
│   ├── app/
│   │   ├── api/                 # Clean REST API routing (v1 endpoints)
│   │   ├── core/                # System configurations and DB connection pools
│   │   ├── models/              # Relational database models and structural schemas
│   │   └── services/            # Pure business logic (bidding mechanics, valuations)
│   ├── tests/                   # PyTest integration and unit test suite
│   ├── Dockerfile               # Multi-stage optimized production Docker configuration
│   └── requirements.txt
├── docker-compose.yml           # Local multi-container development playground
└── README.md                    # Core system documentation
