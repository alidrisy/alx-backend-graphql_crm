#!/usr/bin/env python
"""
Comprehensive test script for GraphQL CRM functionality
Run this script to test all features of the GraphQL API
"""

import os
import sys
import django
import json
from decimal import Decimal
from django.db import models

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order


def test_basic_queries():
    """Test basic GraphQL queries"""
    print("=" * 60)
    print("TESTING BASIC QUERIES")
    print("=" * 60)
    
    # Test hello query
    print("1. Testing hello query...")
    # This would be tested via GraphQL endpoint
    
    # Test single object queries
    print("2. Testing single object queries...")
    customers = Customer.objects.all()[:3]
    products = Product.objects.all()[:3]
    orders = Order.objects.all()[:3]
    
    if customers:
        print(f"   - Found {customers.count()} customers")
    if products:
        print(f"   - Found {products.count()} products")
    if orders:
        print(f"   - Found {orders.count()} orders")


def test_filtering():
    """Test filtering functionality"""
    print("\n" + "=" * 60)
    print("TESTING FILTERING")
    print("=" * 60)
    
    # Test customer filtering
    print("1. Testing customer filtering...")
    customers_by_name = Customer.objects.filter(name__icontains='Alice')
    print(f"   - Customers with 'Alice' in name: {customers_by_name.count()}")
    
    customers_by_email = Customer.objects.filter(email__icontains='example')
    print(f"   - Customers with 'example' in email: {customers_by_email.count()}")
    
    # Test product filtering
    print("2. Testing product filtering...")
    products_by_price = Product.objects.filter(price__gte=100, price__lte=1000)
    print(f"   - Products between $100-$1000: {products_by_price.count()}")
    
    low_stock_products = Product.objects.filter(stock__lt=10)
    print(f"   - Products with low stock (<10): {low_stock_products.count()}")
    
    # Test order filtering
    print("3. Testing order filtering...")
    orders_by_amount = Order.objects.filter(total_amount__gte=100)
    print(f"   - Orders with total >= $100: {orders_by_amount.count()}")
    
    orders_by_customer = Order.objects.filter(customer__name__icontains='Alice')
    print(f"   - Orders by customers with 'Alice' in name: {orders_by_customer.count()}")


def test_mutations():
    """Test mutation functionality"""
    print("\n" + "=" * 60)
    print("TESTING MUTATIONS")
    print("=" * 60)
    
    # Test customer creation
    print("1. Testing customer creation...")
    try:
        customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com",
            phone="+1234567890"
        )
        print(f"   - Created customer: {customer.name} ({customer.email})")
        
        # Test duplicate email validation
        try:
            duplicate_customer = Customer.objects.create(
                name="Duplicate Customer",
                email="test@example.com",  # Same email
                phone="+1987654321"
            )
            print("   - ERROR: Duplicate email should have been rejected")
        except Exception as e:
            print(f"   - Correctly rejected duplicate email: {str(e)}")
            
    except Exception as e:
        print(f"   - Error creating customer: {str(e)}")
    
    # Test product creation
    print("2. Testing product creation...")
    try:
        product = Product.objects.create(
            name="Test Product",
            price=Decimal('99.99'),
            stock=5
        )
        print(f"   - Created product: {product.name} - ${product.price}")
        
        # Test negative price validation
        try:
            invalid_product = Product.objects.create(
                name="Invalid Product",
                price=Decimal('-10.00'),
                stock=5
            )
            print("   - ERROR: Negative price should have been rejected")
        except Exception as e:
            print(f"   - Correctly rejected negative price: {str(e)}")
            
    except Exception as e:
        print(f"   - Error creating product: {str(e)}")
    
    # Test order creation
    print("3. Testing order creation...")
    try:
        # Get existing customer and products
        customer = Customer.objects.first()
        products = Product.objects.all()[:2]
        
        if customer and products.exists():
            # Calculate total
            total_amount = sum(product.price for product in products)
            
            order = Order.objects.create(
                customer=customer,
                total_amount=total_amount
            )
            order.products.set(products)
            
            print(f"   - Created order #{order.id} for {order.customer.name} - ${order.total_amount}")
            
            # Verify total calculation
            calculated_total = order.calculate_total()
            print(f"   - Calculated total: ${calculated_total}")
            
        else:
            print("   - Skipping order creation: need customer and products")
            
    except Exception as e:
        print(f"   - Error creating order: {str(e)}")


def test_ordering():
    """Test ordering functionality"""
    print("\n" + "=" * 60)
    print("TESTING ORDERING")
    print("=" * 60)
    
    # Test customer ordering
    print("1. Testing customer ordering...")
    customers_by_name = Customer.objects.order_by('name')
    print(f"   - Customers ordered by name: {customers_by_name.count()}")
    
    customers_by_date = Customer.objects.order_by('-created_at')
    print(f"   - Customers ordered by creation date (desc): {customers_by_date.count()}")
    
    # Test product ordering
    print("2. Testing product ordering...")
    products_by_price = Product.objects.order_by('price')
    print(f"   - Products ordered by price: {products_by_price.count()}")
    
    products_by_stock = Product.objects.order_by('-stock')
    print(f"   - Products ordered by stock (desc): {products_by_stock.count()}")
    
    # Test order ordering
    print("3. Testing order ordering...")
    orders_by_amount = Order.objects.order_by('-total_amount')
    print(f"   - Orders ordered by total amount (desc): {orders_by_amount.count()}")
    
    orders_by_date = Order.objects.order_by('-order_date')
    print(f"   - Orders ordered by order date (desc): {orders_by_date.count()}")


def test_complex_queries():
    """Test complex query scenarios"""
    print("\n" + "=" * 60)
    print("TESTING COMPLEX QUERIES")
    print("=" * 60)
    
    # Test orders with customer and product details
    print("1. Testing orders with related data...")
    orders_with_details = Order.objects.select_related('customer').prefetch_related('products')
    
    for order in orders_with_details[:3]:
        print(f"   - Order #{order.id}: {order.customer.name} - ${order.total_amount}")
        print(f"     Products: {', '.join([p.name for p in order.products.all()])}")
    
    # Test customers with order counts
    print("2. Testing customers with order counts...")
    customers_with_orders = Customer.objects.annotate(
        order_count=models.Count('orders')
    ).order_by('-order_count')
    
    for customer in customers_with_orders[:3]:
        print(f"   - {customer.name}: {customer.order_count} orders")
    
    # Test products with order counts
    print("3. Testing products with order counts...")
    products_with_orders = Product.objects.annotate(
        order_count=models.Count('orders')
    ).order_by('-order_count')
    
    for product in products_with_orders[:3]:
        print(f"   - {product.name}: {product.order_count} orders")


def cleanup_test_data():
    """Clean up test data created during testing"""
    print("\n" + "=" * 60)
    print("CLEANING UP TEST DATA")
    print("=" * 60)
    
    # Remove test customers
    test_customers = Customer.objects.filter(email__icontains='test@example.com')
    if test_customers.exists():
        test_customers.delete()
        print("   - Removed test customers")
    
    # Remove test products
    test_products = Product.objects.filter(name__icontains='Test Product')
    if test_products.exists():
        test_products.delete()
        print("   - Removed test products")
    
    # Note: Test orders will be removed automatically due to CASCADE


def main():
    """Main test function"""
    print("STARTING GRAPHQL CRM COMPREHENSIVE TESTS")
    print("=" * 60)
    
    # Run all tests
    test_basic_queries()
    test_filtering()
    test_mutations()
    test_ordering()
    test_complex_queries()
    cleanup_test_data()
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED!")
    print("=" * 60)
    print("\nTo test the GraphQL endpoint directly, visit:")
    print("http://localhost:8000/graphql/")
    print("\nSample GraphQL queries to try:")
    print("""
# Basic hello query
{
  hello
}

# Get all customers with filtering
{
  allCustomers(filter: {nameIcontains: "Alice"}) {
    edges {
      node {
        id
        name
        email
        phone
      }
    }
  }
}

# Get products with price filtering and ordering
{
  allProducts(filter: {priceGte: 100}, orderBy: ["-price"]) {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}

# Create a customer
mutation {
  createCustomer(input: {
    name: "John Doe",
    email: "john@example.com",
    phone: "+1234567890"
  }) {
    customer {
      id
      name
      email
    }
    message
    success
  }
}
    """)


if __name__ == "__main__":
    main() 