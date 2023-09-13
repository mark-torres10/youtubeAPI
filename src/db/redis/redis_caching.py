"""Implement Redis cache.

Technically, Redis is an in-memory store, but for the purposes of a PoC we'll
persist the data. In a deployed instance, we can use Redis to avoid duplicate
requests to the API endpoints, but for local development a naive Redis cache
won't persist the data.
"""
pass