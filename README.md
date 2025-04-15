# Restaurants API

API RESTful para gestionar restaurantes y sus reseñas utilizando Django y Django Rest Framework.

## Características

- CRUD completo para restaurantes y reseñas
- Generación automática de slugs
- Cálculo automático del rating de restaurantes
- Documentación con Swagger/OpenAPI
- Validación de datos según esquemas
- Filtrado y paginación
- Contenerización con Docker

## Estructura del Proyecto

```
restaurants_api/
│
├── restaurant_api/         # Configuración principal del proyecto
│   ├── settings.py         # Configuración de Django
│   ├── urls.py             # URLs principales
│   └── ...
│
├── reviews/                # Aplicación principal 
│   ├── models.py           # Modelos de datos
│   ├── serializers.py      # Serializadores de DRF
│   ├── views.py            # Vistas y ViewSets
│   ├── urls.py             # URLs de la API
│   └── ...
│
├── Dockerfile              # Configuración de Docker
├── docker-compose.yml      # Configuración de Docker Compose
├── requirements.txt        # Dependencias del proyecto
└── .env.example            # Ejemplo de variables de entorno
```

## Modelos

### Restaurant
- `slug`: Generado automáticamente, sólo lectura
- `name`: Obligatorio, máximo 128 caracteres
- `url`: Opcional, formato URI, máximo 256 caracteres
- `image`: Obligatorio, formato URI
- `rating`: Sólo lectura, calculado automáticamente como promedio de reseñas

### Review
- `slug`: Generado automáticamente, sólo lectura
- `restaurant`: Referencia al restaurante, obligatorio
- `name`: Obligatorio, máximo 128 caracteres
- `description`: Obligatorio
- `rating`: Obligatorio, entero entre 1 y 5
- `created`: Fecha/hora automática, sólo lectura

## Endpoints

- `/api/reviews/restaurant/` (GET, POST)
- `/api/reviews/restaurant/{slug}/` (GET, PUT, PATCH, DELETE)
- `/api/reviews/review/` (GET, POST) con filtro por restaurant__slug
- `/api/reviews/review/{slug}/` (GET, PUT, PATCH, DELETE)
- `/swagger/` - Documentación Swagger
- `/redoc/` - Documentación ReDoc

## Requisitos

- Docker y Docker Compose

## Instalación y Ejecución

1. Clonar el repositorio:
   ```
   git clone <repo-url>
   cd restaurants_api
   ```

2. Crear archivo .env a partir de .env.example:
   ```
   cp .env.example .env
   ```

3. Construir y levantar los contenedores:
   ```
   docker-compose up -d --build
   ```

4. Ejecutar las migraciones:
   ```
   docker-compose exec -it <container-id> python manage.py makemigrations
   docker-compose exec -it <container-id> python manage.py migrate
   ```


4. Crear un superusuario (opcional):
   ```
   docker-compose exec web python manage.py createsuperuser
   ```

5. Acceder a la API:
   - API: http://localhost:8000/api/reviews/
   - Documentación: http://localhost:8000/swagger/
   - Admin: http://localhost:8000/admin/

## Ejemplos de Uso

### Crear un Restaurante
```
POST /api/reviews/restaurant/
{
    "name": "Restaurant Example",
    "url": "https://example.com",
    "image": "https://example.com/image.jpg"
}
```

### Crear una Reseña
```
POST /api/reviews/review/
{
    "restaurant_slug": "restaurant-example-abcd1234",
    "name": "Great Experience",
    "description": "The food was delicious and the service was excellent.",
    "rating": 5
}
```

### Obtener Restaurantes
```
GET /api/reviews/restaurant/
```

### Obtener Reseñas de un Restaurante Específico
```
GET /api/reviews/review/?restaurant__slug=restaurant-example-abcd1234
```
