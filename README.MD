# Pokedex - Backend

Aplicación construida con **Django**.

## Requisitos

- **Python** versión 3.8.3 o superior.
- **Postgres** versión 13 o superior.

## Instalación

Cree y active el entorno **Python**:

```bash
python -m venv env
source env/bin/activate # En Windows utilice `env\Scripts\activate`
```

Instale las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

Cree el archivo de entorno `mo/.env`. Puede guiarse por el archivo de ejemplo en `mo/.env.sample`. Cree la base de datos y añada los parámetros de conexión al archivo.

Por último, ejecute las migraciones:

```bash
python manage.py migrate
```

## Uso

Ponga en marcha el servidor de desarrollo:

```bash
python manage.py runserver
```

Abra una pestaña en su navegador y vaya a la dirección [localhost:8000](http://localhost:8000) (o el puerto que haya indicado en el comando `runserver`).

## LLenado de base de datos

Para obtener información de un pokémon desde el api de *PokeApi* ejecute el siguiente comando

```bash
python manage.py collect {id}
```

Donde _id_ es el identificador de la cadena de evolución. Este comando obtiene información para cada pokémon incluido en la cadena.
