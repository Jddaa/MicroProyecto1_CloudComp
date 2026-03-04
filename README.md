# 🛒 Microservices Store System

Sistema de tienda construido con **arquitectura de microservicios**,
utilizando **Flask, Docker, MySQL y Consul** para la comunicación entre
servicios.

El sistema permite gestionar:

-   👤 Usuarios\
-   📦 Productos\
-   🧾 Órdenes de compra\
-   🛒 Carrito de compras\
-   🔐 Autenticación con sesiones

Todo el sistema se ejecuta usando **Docker Compose**, lo que permite
levantar todos los servicios automáticamente.

------------------------------------------------------------------------

# 🏗 Arquitectura del sistema

El sistema está dividido en **microservicios independientes**, cada uno
con su propia base de datos.

Frontend (5001)\
│\
▼

Micro Users (5002) → MySQL Usuarios\
Micro Products (5003) → MySQL Productos\
Micro Orders (5004) → MySQL Ordenes

Todos los servicios se registran en **Consul**, que permite que los
microservicios se descubran entre sí.

------------------------------------------------------------------------

# 📁 Estructura del proyecto

project/

docker-compose.yml

frontend/\
microUsers/\
microProducts/\
microOrders/

initUsuarios.sql\
initProductos.sql\
initOrdenes.sql

------------------------------------------------------------------------

# ⚙️ Tecnologías utilizadas

**Backend** - Python - Flask - SQLAlchemy - Flask-CORS

**Arquitectura** - Microservicios - Consul (Service Discovery)

**Base de datos** - MySQL

**Contenedores** - Docker - Docker Compose

**Frontend** - HTML - Bootstrap - JavaScript

------------------------------------------------------------------------

# 🚀 Cómo ejecutar el proyecto

## 1️⃣ Clonar el repositorio

git clone https://github.com/tuusuario/microservices-store.git\
cd microservices-store

## 2️⃣ Levantar todos los servicios

docker compose up --build

Esto iniciará automáticamente:

-   Consul
-   MySQL Usuarios
-   MySQL Productos
-   MySQL Órdenes
-   Microservicio Users
-   Microservicio Products
-   Microservicio Orders
-   Frontend

------------------------------------------------------------------------

# 🌐 Puertos del sistema

| Servicio           | Puerto |
|--------------------|--------|
| Frontend           | 5001   |
| Users Service      | 5002   |
| Products Service   | 5003   |
| Orders Service     | 5004   |
| Consul             | 8500   |
| MySQL Usuarios     | 3306   |
| MySQL Productos    | 3307   |
| MySQL Ordenes      | 3308   |

------------------------------------------------------------------------

# 📦 API Endpoints

## Users Service

GET /api/users\
GET /api/users/{id}\
POST /api/users\
PUT /api/users/{id}\
DELETE /api/users/{id}\
POST /api/login\
POST /api/logout\
GET /api/session

------------------------------------------------------------------------

## Products Service

GET /api/products\
GET /api/products/{id}\
POST /api/products\
PUT /api/products/{id}\
DELETE /api/products/{id}

------------------------------------------------------------------------

## Orders Service

GET /api/orders\
GET /api/orders/{id}\
POST /api/orders

El servicio de órdenes se comunica con **Products Service** para:

-   verificar stock
-   obtener precios
-   actualizar inventario

------------------------------------------------------------------------

# 🔎 Consul

Consul permite que los microservicios encuentren automáticamente otros
servicios.

Panel web:

http://192.168.100.3:8500

------------------------------------------------------------------------

# 🔐 Autenticación

El sistema usa **sesiones de Flask**.

Flujo:

1.  Usuario inicia sesión\
2.  Se crea una sesión\
3.  Se guarda username y email\
4.  El sistema reconoce al usuario autenticado

------------------------------------------------------------------------

# 🧾 Flujo de compra

1.  Usuario inicia sesión\
2.  Navega al catálogo de productos\
3.  Agrega productos al carrito\
4.  Genera una orden\
5.  Orders Service:

-   consulta Products Service
-   verifica inventario
-   actualiza stock
-   guarda la orden en MySQL

------------------------------------------------------------------------

# 👨‍💻 Autores
Carlos Garzón y Juan Mendoza - Ingenieria Multimedia UAO

Proyecto desarrollado para práctica de arquitectura de microservicios.
