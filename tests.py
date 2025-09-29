#!/usr/bin/env python3
"""
Test script to check if the FastAPI endpoints are working correctly
"""

import requests
import json
import sys

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing MILP Optimization Agent API...")
    print(f"🌐 Base URL: {base_url}")
    print("-" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check: PASSED")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check: FAILED ({response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Health check: FAILED - Server not running")
        print("   Please start the FastAPI server with: python run.py")
        return False
    except Exception as e:
        print(f"❌ Health check: FAILED - {e}")
        return False
    
    print()
    
    # Test problem description
    test_problem = "Maximize profit: 3x + 2y subject to x + y <= 4, x >= 0, y >= 0"
    
    # Test solver endpoint
    try:
        print("🔧 Testing Solver API...")
        response = requests.post(
            f"{base_url}/solver/solve",
            json={"problem_description": test_problem},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Solver API: PASSED")
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Solver API: FAILED ({response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Solver API: FAILED - {e}")
    
    print()
    
    # Test planner endpoint
    try:
        print("📋 Testing Planner API...")
        response = requests.post(
            f"{base_url}/planner/plan",
            json={"problem_description": test_problem},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Planner API: PASSED")
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Planner API: FAILED ({response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Planner API: FAILED - {e}")
    
    print()
    
    # Test explainer endpoint
    try:
        print("💡 Testing Explainer API...")
        response = requests.post(
            f"{base_url}/explainer/solve",
            json={"problem_description": test_problem},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Explainer API: PASSED")
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Explainer API: FAILED ({response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Explainer API: FAILED - {e}")
    
    print()
    
    # Test code endpoint
    try:
        print("💻 Testing Code API...")
        response = requests.get(f"{base_url}/solver/code")
        if response.status_code == 200:
            print("✅ Code API: PASSED")
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Code API: FAILED ({response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Code API: FAILED - {e}")
    
    print()
    print("🏁 API testing complete!")
    print()
    print("💡 If any tests failed:")
    print("   1. Make sure your FastAPI server is running: python run.py")
    print("   2. Check that your agent files exist in the agents/ directory")
    print("   3. Verify your API routes are properly configured")
    print("   4. Check the server logs for detailed error messages")

if __name__ == "__main__":
    test_api_endpoints()
