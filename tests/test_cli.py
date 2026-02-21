#!/usr/bin/env python3
"""Tests for Ephemera CLI"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ephemera_cli import EphemeraClient

def test_client_init():
    """Test client initialization"""
    client = EphemeraClient("test_key", "test_secret")
    assert client.token == "test_key:test_secret"
    assert client.base_url == "https://app.alice.ws"
    print("✓ Client initialization test passed")

def test_client_custom_base_url():
    """Test client with custom base URL"""
    client = EphemeraClient("key", "secret", "https://custom.api.com/")
    assert client.base_url == "https://custom.api.com"
    print("✓ Custom base URL test passed")

if __name__ == "__main__":
    test_client_init()
    test_client_custom_base_url()
    print("\nAll tests passed!")
