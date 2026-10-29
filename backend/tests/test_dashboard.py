"""
Dashboard API Tests

This file tests all dashboard endpoints to ensure they return correct data.

How to run:
    pytest tests/test_dashboard.py -v
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app

client = TestClient(app)

def test_energy_capacity():
    """
    Test GET /dashboard_powerplant/energy_capacity
    
    Expected:
    - Status code: 200
    - Response is a list
    """
    response = client.get("/dashboard_powerplant/energy_capacity")
    
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_energy_trends():
    """
    Test GET /dashboard_powerplant/energy_trends
    
    Expected:
    - Status code: 200
    - Response is a list
    """
    response = client.get("/dashboard_powerplant/energy_trends")
    
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_country_insights():
    """
    Test GET /dashboard_powerplant/country_insights
    
    Expected:
    - Status code: 200
    - Response is a list
    """
    response = client.get("/dashboard_powerplant/country_insights")
    
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_energy_sources():
    """
    Test GET /dashboard_powerplant/energy_sources
    
    Expected:
    - Status code: 200
    - Response is a dictionary
    """
    response = client.get("/dashboard_powerplant/energy_sources")
    
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)