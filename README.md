## Estado de Cuenta API

---

### Descripción del proyecto
Esta API permite analizar los estados de cuenta de los agentes de telecomunicaciones que pueden ser descargados a través de [**Transfermóvil**](https://www.etecsa.cu/es/aplicaciones/transfermovil). Extrae el contenido, filtra las transacciones, resume los datos y proporciona métricas como el total gastado en recargas, depósitos y ganancias

---

### Características
- 📥 Permite subir los archivos PDF y extrae su contenido
- 📊 Filtra las transacciones por estado (Exitosas, Fallidas o Todas)
- 💰 Cálculo del total depositado, gastado en recargas y ganancias obtenidas

---

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/edgarmoya/api-ecuenta.git

# Navegar al directorio del proyecto
cd api-ecuenta

# Crear un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

---

### Uso

```bash
# Ejecutar el servidor de FastAPI
uvicorn app.main:app --reload
```

Visita la documentación interactiva en: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Endpoints

| Método | Endpoint          | Descripción                              |
|--------|-------------------|------------------------------------------|
| `POST`   | `/pdf/transactions/`       | Extrae todas las transacciones del PDF         |
| `POST`   | `/pdf/deposits/`       | Devuelve todos los depósitos realizados |
| `POST`    | `/pdf/sales/`         | Obtiene datos de ventas de recargas      |

> Nota: Todos los endpoints permiten obtener los datos paginados si se desea y filtrarlos por su estado (Exitosas, Fallidas o Todas).

---

### Contribuciones

1. Haz un fork del repositorio  
2. Crea una nueva rama: `git checkout -b nueva-funcionalidad`  
3. Realiza tus cambios y haz commit: `git commit -m 'Agregar nueva funcionalidad'`  
4. Sube los cambios: `git push origin nueva-funcionalidad`  
5. Envía un pull request  

---

### Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.