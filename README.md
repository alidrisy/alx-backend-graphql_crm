# ALX Backend GraphQL CRM

A comprehensive Customer Relationship Management (CRM) system built with Django and GraphQL, featuring advanced filtering, mutations, and real-time data querying capabilities.

## 🚀 Features

### Core Functionality
- **GraphQL API** with single endpoint for all operations
- **Customer Management** with validation and bulk operations
- **Product Catalog** with inventory tracking
- **Order Processing** with automatic total calculation
- **Advanced Filtering** with multiple search criteria
- **Sorting & Ordering** support for all entities
- **Real-time Data** with optimized queries

### GraphQL Features
- **Queries**: Single object and filtered list queries
- **Mutations**: Create, bulk create, and complex operations
- **Filtering**: Case-insensitive search, date ranges, numeric ranges
- **Ordering**: Multi-field sorting with ascending/descending support
- **Error Handling**: Comprehensive validation and user-friendly error messages
- **Nested Queries**: Related data fetching with optimized performance

## 📋 Requirements

- Python 3.8+
- Django 5.2.3
- graphene-django 3.2.3
- django-filter 25.1

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd alx_backend_graphql_crm
   ```

2. **Create virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Seed the database**
   ```bash
   python seed.py
   ```

6. **Start the server**
   ```bash
   python manage.py runserver
   ```

7. **Access GraphQL interface**
   ```
   http://localhost:8000/graphql/
   ```

## 🗄️ Database Models

### Customer
- `name` (CharField): Customer's full name
- `email` (EmailField): Unique email address
- `phone` (CharField): Phone number with validation
- `created_at` (DateTimeField): Creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

### Product
- `name` (CharField): Product name
- `price` (DecimalField): Product price (positive validation)
- `stock` (PositiveIntegerField): Available stock quantity
- `created_at` (DateTimeField): Creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

### Order
- `customer` (ForeignKey): Reference to Customer
- `products` (ManyToManyField): Associated products
- `total_amount` (DecimalField): Calculated order total
- `order_date` (DateTimeField): Order timestamp
- `created_at` (DateTimeField): Creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

## 🔍 GraphQL Queries

### Basic Queries

#### Hello Query
```graphql
{
  hello
}
```

#### Single Object Queries
```graphql
# Get customer by ID
{
  customer(id: "1") {
    id
    name
    email
    phone
    createdAt
  }
}

# Get product by ID
{
  product(id: "1") {
    id
    name
    price
    stock
  }
}

# Get order by ID
{
  order(id: "1") {
    id
    customer {
      name
      email
    }
    products {
      name
      price
    }
    totalAmount
    orderDate
  }
}
```

### Filtered Queries

#### Customer Filtering
```graphql
# Filter customers by name
{
  allCustomers(filter: {nameIcontains: "Alice"}) {
    edges {
      node {
        id
        name
        email
        phone
        createdAt
      }
    }
  }
}

# Filter customers by email and creation date
{
  allCustomers(filter: {
    emailIcontains: "example",
    createdAtGte: "2025-01-01"
  }) {
    edges {
      node {
        id
        name
        email
      }
    }
  }
}

# Filter customers by phone pattern
{
  allCustomers(filter: {phonePattern: "+1"}) {
    edges {
      node {
        id
        name
        phone
      }
    }
  }
}
```

#### Product Filtering
```graphql
# Filter products by price range
{
  allProducts(filter: {
    priceGte: 100,
    priceLte: 1000
  }) {
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

# Filter low stock products
{
  allProducts(filter: {lowStock: true}) {
    edges {
      node {
        id
        name
        stock
      }
    }
  }
}
```

#### Order Filtering
```graphql
# Filter orders by customer name and total amount
{
  allOrders(filter: {
    customerName: "Alice",
    totalAmountGte: 500
  }) {
    edges {
      node {
        id
        customer {
          name
        }
        totalAmount
        orderDate
      }
    }
  }
}

# Filter orders by product name
{
  allOrders(filter: {productName: "Laptop"}) {
    edges {
      node {
        id
        products {
          name
          price
        }
        totalAmount
      }
    }
  }
}
```

### Ordering Queries
```graphql
# Order customers by name
{
  allCustomers(orderBy: ["name"]) {
    edges {
      node {
        id
        name
        email
      }
    }
  }
}

# Order products by price (descending)
{
  allProducts(orderBy: ["-price"]) {
    edges {
      node {
        id
        name
        price
      }
    }
  }
}

# Order orders by total amount (descending)
{
  allOrders(orderBy: ["-totalAmount"]) {
    edges {
      node {
        id
        totalAmount
        orderDate
      }
    }
  }
}
```

## ✏️ GraphQL Mutations

### Customer Mutations

#### Create Single Customer
```graphql
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
      phone
    }
    message
    success
    errors
  }
}
```

#### Bulk Create Customers
```graphql
mutation {
  bulkCreateCustomers(input: [
    {
      name: "Alice Johnson",
      email: "alice@example.com",
      phone: "+1234567890"
    },
    {
      name: "Bob Smith",
      email: "bob@example.com",
      phone: "123-456-7890"
    }
  ]) {
    customers {
      id
      name
      email
    }
    errors
    successCount
    errorCount
  }
}
```

### Product Mutations

#### Create Product
```graphql
mutation {
  createProduct(input: {
    name: "Laptop Pro",
    price: 1299.99,
    stock: 15
  }) {
    product {
      id
      name
      price
      stock
    }
    message
    success
    errors
  }
}
```

### Order Mutations

#### Create Order
```graphql
mutation {
  createOrder(input: {
    customerId: "1",
    productIds: ["1", "2", "3"]
  }) {
    order {
      id
      customer {
        name
        email
      }
      products {
        name
        price
      }
      totalAmount
      orderDate
    }
    message
    success
    errors
  }
}
```

## 🔧 Advanced Features

### Filtering Options

#### Customer Filters
- `name` / `nameIcontains`: Case-insensitive name search
- `email` / `emailIcontains`: Case-insensitive email search
- `phone`: Exact phone number match
- `phonePattern`: Phone number pattern matching
- `createdAt`: Exact creation date
- `createdAtGte` / `createdAtLte`: Creation date range

#### Product Filters
- `name` / `nameIcontains`: Case-insensitive name search
- `price`: Exact price match
- `priceGte` / `priceLte`: Price range
- `stock`: Exact stock match
- `stockGte` / `stockLte`: Stock range
- `lowStock`: Boolean filter for stock < 10
- `createdAtGte` / `createdAtLte`: Creation date range

#### Order Filters
- `totalAmount`: Exact total amount match
- `totalAmountGte` / `totalAmountLte`: Total amount range
- `orderDate`: Exact order date match
- `orderDateGte` / `orderDateLte`: Order date range
- `customerName`: Filter by customer name
- `customerEmail`: Filter by customer email
- `customerId`: Filter by customer ID
- `productName`: Filter by product name
- `productId`: Filter by product ID
- `createdAtGte` / `createdAtLte`: Creation date range

### Ordering Options
- `name`: Customer/Product name (ascending)
- `-name`: Customer/Product name (descending)
- `price`: Product price (ascending)
- `-price`: Product price (descending)
- `stock`: Product stock (ascending)
- `-stock`: Product stock (descending)
- `totalAmount`: Order total (ascending)
- `-totalAmount`: Order total (descending)
- `orderDate`: Order date (ascending)
- `-orderDate`: Order date (descending)
- `createdAt`: Creation date (ascending)
- `-createdAt`: Creation date (descending)

## 🧪 Testing

### Run Comprehensive Tests
```bash
python test_graphql.py
```

### Manual Testing
1. Start the server: `python manage.py runserver`
2. Visit: `http://localhost:8000/graphql/`
3. Use the GraphiQL interface to test queries and mutations

### Sample Test Queries
```graphql
# Test basic functionality
{
  hello
}

# Test customer filtering
{
  allCustomers(filter: {nameIcontains: "Alice"}) {
    edges {
      node {
        id
        name
        email
      }
    }
  }
}

# Test product filtering with ordering
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

# Test order creation
mutation {
  createCustomer(input: {
    name: "Test User",
    email: "test@example.com",
    phone: "+1234567890"
  }) {
    customer {
      id
      name
      email
    }
    success
  }
}
```

## 🏗️ Project Structure

```
alx_backend_graphql_crm/
├── alx_backend_graphql_crm/     # Main Django project
│   ├── settings.py              # Django settings
│   ├── urls.py                  # URL configuration
│   └── schema.py                # Main GraphQL schema
├── crm/                         # CRM application
│   ├── models.py                # Database models
│   ├── schema.py                # GraphQL types and mutations
│   ├── filters.py               # Django-filter configurations
│   ├── admin.py                 # Django admin configuration
│   └── migrations/              # Database migrations
├── seed.py                      # Database seeding script
├── test_graphql.py              # Comprehensive test script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔒 Validation & Error Handling

### Customer Validation
- Email uniqueness validation
- Phone number format validation (supports international and US formats)
- Required field validation

### Product Validation
- Positive price validation
- Non-negative stock validation
- Required field validation

### Order Validation
- Customer existence validation
- Product existence validation
- Minimum one product requirement
- Positive total amount validation

### Error Response Format
```json
{
  "data": null,
  "errors": [
    {
      "message": "Email already exists",
      "locations": [{"line": 2, "column": 3}],
      "path": ["createCustomer"]
    }
  ]
}
```

## 🚀 Performance Optimizations

- **Database Indexing**: Optimized queries with proper indexing
- **Select Related**: Efficient related data fetching
- **Prefetch Related**: Optimized many-to-many relationships
- **Connection Fields**: Pagination support for large datasets
- **Filter Optimization**: Efficient filtering with django-filter

## 📝 API Documentation

The GraphQL API is self-documenting. Use the GraphiQL interface at `http://localhost:8000/graphql/` to:

- Explore the schema
- View available types and fields
- Test queries and mutations
- See real-time documentation
- Validate queries before execution

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is part of the ALX Backend Development curriculum.

## 🆘 Support

For issues and questions:
1. Check the GraphiQL interface for schema documentation
2. Review the test script for usage examples
3. Check Django and GraphQL documentation
4. Open an issue in the repository

---

**Happy Coding! 🎉**