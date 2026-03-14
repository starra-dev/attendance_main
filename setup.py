from setuptools import find_packages, setup

setup(
    name="attendance_main",
    version="0.1.0",
    description="Attendance tracking FastAPI application",
    packages=find_packages(include=["attendance_main", "app", "app.*"]),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "pydantic-settings",
        "PyJWT",
        "pwdlib",
    ],
    python_requires=">=3.9",
)
