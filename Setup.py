from distutils.core import setup
#no puedo instalar setuptools por permisos
#from setuptools import setup

asterisco = ["*"]


setup(
    name = "Proyecto Farmacia DI",
    version = "0.3",
    description = "Interfaz de gestión de una farmacia",
    long_description = """Interfaz de usuario y conexion con base de datos para la
        gestión de una farmacia""",
    author = "Omar Torrado Míguez",
    author_email = "otorradomiguez@danielcastelao.org",
    url = "www.miFakeURL.fake",
    keywords = "farmacia, gestión",
    platforms = "linux,windows",
    packages = ["modulos","database","ficheros"],
    package_data = {"ficheros":asterisco, "database":asterisco},
    scripts = ["Launcher.py"]
)