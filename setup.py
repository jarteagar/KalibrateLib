from setuptools import setup, find_packages

setup(
    name="KalibrateLib",                # Nombre del paquete
    version="1.1",                      # Versión inicial
    description="Descripción de KalibrateLib",  # Breve descripción
    author="John Arteaga",                 # Autor
    packages=find_packages(),           # Encuentra automáticamente todos los módulos
    install_requires=[],                # Dependencias, si las hay
    python_requires='>=3.6',            # Versión mínima de Python
)