# water-tariff-dashboard

<p align="center">
  <img src=".img/innwater-logo.png" alt="InnWater Logo" width="220"/>
</p>

<p align="center">
  <strong>Water Tariff Simulation and Assessment Tool within the InnWater project</strong>
</p>

<p align="center">
  <a href="https://innwater.eurecatprojects.com/msm/" target="_blank">
    <img src="https://img.shields.io/badge/Access%20Application-Live%20Demo-blue?style=for-the-badge&logo=appveyor" alt="Access Water Tariff Tool"/>
  </a>
</p>

---

## Overview

The **InnWater Water Tariff Tool** is an interactive platform designed to simulate, analyze, and optimize water tariff structures. It provides a comprehensive framework for assessing the economic and financial sustainability of water services while ensuring affordability for different consumer groups.

Key features include:

- **Tariff Simulation**: Model different tariff structures (flat rates, increasing block tariffs, etc.) and predict their impact on revenue and consumption.
- **Financial Sustainability**: Evaluate the cost recovery of water services, including operational, maintenance, and capital costs.
- **Affordability Analysis**: Assess the impact of water bills on household income across various socio-economic groups.
- **Economic Efficiency**: Analyze the incentives for water conservation and efficient resource allocation.
- **Environmental Costs**: Incorporate environmental and resource costs into the tariff design process.

Users can create multiple scenarios, compare results, and visualize the trade-offs between financial viability and social equity.

---

## Background

The InnWater project develops tools to support:

- **multi-level, cross-sector governance of water systems**
- **economic and financial modelling**, including tariff simulations
- **stakeholder engagement and governance assessment frameworks**

Visit the **[InnWater Governance Platform](https://le.innwater.eu/)** to explore other project tools and the learning environment.

The Water Tariff Tool serves as a decision-support system for utility managers and regulators to design fair and sustainable water pricing policies.

---

## Technologies

The platform is built using a modern full-stack architecture:

- **Frontend**:
  - **Angular 15** – Core framework for the user interface.
  - **Bootstrap 5** – Responsive design and UI components.
  - **Chart.js & D3.js** – Interactive visualizations and data-driven charts.
  - **ngx-markdown** – Rendering of dynamic documentation and reports.

- **Backend**:
  - **FastAPI (Python)** – High-performance API framework for tariff calculations and data management.
  - **PostgreSQL** – Relational database for storing simulations and user data.
  - **SQLAlchemy** – ORM for database interactions.
  - **Pandas & NumPy** – Advanced data processing and economic modeling.

- **Deployment**:
  - **Docker & Docker Compose** – Containerization for consistent development and production environments.

---

## Usage

### Local Execution (Manual)

To run the project locally without Docker, you need to set up both the frontend and the backend.

#### 1. Backend (FastAPI)

```bash
cd fast_backend
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
# Run the server
uvicorn main:app --reload
```

#### 2. Frontend (Angular)

```bash
cd frontend
npm install
npm start
```
The application will be available at `http://localhost:4200`.

### Using Docker (Recommended)

You can run the entire stack (Frontend, Backend, and Database) using Docker Compose:

```bash
docker-compose up --build
```

---

## Contact

- **Water Tariff Dashboard design and development**: Michel Paul & Jimmy Lauret (University of La Réunion)
- **Software Development**: Oriol Alàs (Eurecat)

---

<p align="center">
  <img src=".img/footer.png" alt="EU and UKRI Funding Logo" width="600"/>
</p>

<p align="center">
  This project has received funding from the European Union's Horizon Europe programme (Grant Agreement No. 101086512) and from UK Research and Innovation (UKRI) under the UK government's Horizon Europe funding guarantee (Grant No. 10066637).
</p>
