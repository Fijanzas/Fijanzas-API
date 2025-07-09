# Fijanzas API - Bond Valuation System

API REST para cálculo de valuación de bonos utilizando el método alemán de amortización.

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- MySQL Server
- Git

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd Fijanzas-API
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
Asegúrate de tener MySQL ejecutándose y actualiza la configuración en `database.py` con tus credenciales:

```python
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://usuario:contraseña@localhost/nombre_bd"
```

### 5. Iniciar la API
```bash
uvicorn main:app --reload
```

La API estará disponible en: `http://localhost:8000`

## 📖 Documentación de la API

### Documentación interactiva:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔐 Autenticación

### 1. Crear Usuario
**POST** `/users`

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "mypassword123"
}
```

**Respuesta:**
```json
{
  "message": "User created successfully",
  "username": "testuser"
}
```

### 2. Iniciar Sesión
**POST** `/login`

```json
{
  "username": "testuser",
  "password": "mypassword123"
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Login successful",
  "username": "testuser"
}
```

## 💰 Gestión de Bonos

### 1. Crear Bono
**POST** `/bonds`

```json
{
  "user_id": 1,
  "nominal_value": 1200,
  "commercial_value": 1200,
  "coupon_rate":    0.05809140331,
  "market_rate": 0.05809140331,
  "payment_frequency": 2,
  "duration": 3,
  "bonus": 0.009,
  "flotation": 0,
  "cavali": 0,
  "structuration": 0,
  "colocation": 0,
  "total_grace_period": 1,
  "partial_grace_period": 1
}
```

**Respuesta:**
```json
{
  "id": 1,
  "user_id": 1,
  "nominal_value": 1200,
  "commercial_value": 1200,
  "coupon_rate": 0.0286357,
  "market_rate": 0.002004008,
  "payment_frequency": 3,
  "duration": 6,
  "bonus": 0.009,
  "flotation": 0.0045,
  "cavali": 0.005,
  "structuration": 0.008,
  "colocation": 0.009,
  "total_grace_period": 1,
  "partial_grace_period": 1
}
```

### 2. Obtener Bono por ID
**GET** `/bonds/{bond_id}`

**Respuesta:**
```json
{
  "id": 1,
  "user_id": 1,
  "nominal_value": 1200,
  "commercial_value": 1200,
  "coupon_rate": 0.0286357,
  "market_rate": 0.002004008,
  "payment_frequency": 3,
  "duration": 6,
  "bonus": 0.009,
  "flotation": 0.0045,
  "cavali": 0.005,
  "structuration": 0.008,
  "colocation": 0.009,
  "total_grace_period": 1,
  "partial_grace_period": 1
}
```

### 3. Obtener Flujos de Caja
**GET** `/bonds/{bond_id}/flows`

**Respuesta:**
```json
[
  {
    "bond_id": 1,
    "period": 1,
    "initial_balance": 1200.00,
    "amortization": 200.00,
    "coupon": 34.36,
    "bonus": 10.80,
    "net_flow": 245.16,
    "final_balance": 1000.00
  },
  {
    "bond_id": 1,
    "period": 2,
    "initial_balance": 1000.00,
    "amortization": 200.00,
    "coupon": 28.64,
    "bonus": 9.00,
    "net_flow": 237.64,
    "final_balance": 800.00
  }
]
```

### 4. Obtener Resultados de Valuación
**GET** `/bonds/{bond_id}/results`

**Respuesta:**
```json
{
  "bond_id": 1,
  "TCEA": 0.1234,
  "TREA": 0.1156,
  "Precio_Maximo": 1180.50
}
```

## 📊 Estructura del Proyecto

```
Fijanzas-API/
├── main.py                     # Aplicación FastAPI principal
├── models.py                   # Modelos de base de datos (SQLAlchemy)
├── database.py                 # Configuración de base de datos
├── germanAmortizationMethod.py # Lógica de cálculo de bonos
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Documentación del proyecto
├── classes/                    # Clases auxiliares
│   ├── bond.py                 # Clase Bond
│   ├── flow.py                 # Clase Flow
│   └── results.py              # Clase Results
└── __pycache__/                # Cache de Python
```

## 🧪 Pruebas

### Ejecutar todas las pruebas:
```bash
python -m pytest test_api.py -v
```

### Probar conexión a la base de datos:
```bash
python test_connection.py
```

### Ejemplo de prueba manual con curl:

1. **Crear usuario:**
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com", 
    "password": "password123"
  }'
```

2. **Hacer login:**
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

3. **Crear bono:**
```bash
curl -X POST "http://localhost:8000/bonds" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "nominal_value": 1200,
    "commercial_value": 1200,
    "coupon_rate": 0.028635700,
    "market_rate": 0.002004008,
    "payment_frequency": 3,
    "duration": 6,
    "bonus": 0.009,
    "flotation": 0.0045,
    "cavali": 0.005,
    "structuration": 0.008,
    "colocation": 0.009,
    "total_grace_period": 1,
    "partial_grace_period": 1
  }'
```

## 🔧 Comandos Útiles

### Desarrollo:
```bash
# Instalar en modo desarrollo
pip install -e .

# Ejecutar con auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Ver logs detallados
uvicorn main:app --reload --log-level debug
```

### Base de datos:
```bash
# Reinicializar base de datos
python setup_database.py

# Verificar conexión
python test_connection.py
```

## ⚙️ Variables de Entorno

Puedes configurar las siguientes variables de entorno:

```bash
# .env file
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 📝 Notas Técnicas

- **Método de Amortización**: Se utiliza el método alemán para el cálculo de flujos de caja
- **Precisión**: Los valores monetarios se redondean a 2 decimales, los indicadores financieros a 4 decimales
- **Base de Datos**: MySQL con SQLAlchemy ORM
- **Autenticación**: Sistema básico con bcrypt para hashing de contraseñas
- **Validación**: Pydantic para validación de datos de entrada y salida

## 🚀 Deploy en Producción

Para producción, considera:

1. **Usar un servidor ASGI como Gunicorn:**
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. **Configurar variables de entorno para producción**
3. **Usar una base de datos externa (no local)**
4. **Implementar logging apropiado**
5. **Configurar CORS si es necesario**

## 🐛 Troubleshooting

### Error de conexión a MySQL:
- Verificar que MySQL esté ejecutándose
- Comprobar credenciales en `database.py`
- Asegurar que la base de datos existe

### Error de dependencias:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Error de puertos ocupados:
```bash
# Usar otro puerto
uvicorn main:app --reload --port 8001
```

## 📄 Licencia

Este proyecto es para fines educativos y de demostración.