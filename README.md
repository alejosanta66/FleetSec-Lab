# FleetSec-Lab

## Descripción

Laboratorio DevSecOps desarrollado como prueba técnica para un cargo de Ingeniería/Ciberseguridad.

El proyecto implementa una API REST desarrollada en FastAPI protegida mediante JWT y control de acceso basado en roles (RBAC), integrada con un pipeline de análisis de seguridad utilizando herramientas SAST, SCA, Secret Scanning, SBOM y DAST.

---

## Tecnologías

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- RBAC
- Docker
- SonarQube
- Semgrep
- Gitleaks
- Syft
- Trivy
- OWASP ZAP
- GitHub Actions

---

## Configuración local

Para asegurar que el código cumpla con los estándares de seguridad antes de hacer un commit, el proyecto utiliza `pre-commit`. Para configurarlo, ejecuta los siguientes comandos en tu entorno local:

```bash
pip install pre-commit
pre-commit install

---

## Arquitectura

```text
                Cliente
                   │
                   ▼
            FastAPI REST API
                   │
         JWT Authentication
                   │
         Role Based Access
                   │
              SQLAlchemy
                   │
             PostgreSQL
                   │
               Docker
```

---

## Pipeline DevSecOps

```text
Developer

    │
    ▼

GitHub Repository

    │
    ▼

GitHub Actions

    │
    ├───────────── SonarQube
    │
    ├───────────── Semgrep
    │
    ├───────────── Gitleaks
    │
    ├───────────── Syft (SBOM)
    │
    ├───────────── Trivy
    │
    ├───────────── Docker Build
    │
    └───────────── OWASP ZAP
```

---

## Controles implementados

### Seguridad de la aplicación

- JWT Authentication
- Role Based Access Control (RBAC)
- Password Hashing (bcrypt)
- Validación de usuarios activos

### Análisis estático

- SonarQube
- Semgrep

### Secret Scanning

- Gitleaks

### Software Bill of Materials

- Syft

### Vulnerability Scanning

- Trivy

### Dynamic Application Security Testing

- OWASP ZAP

---

## Evidencias

Los reportes se encuentran en:

```
reports/
```

Incluyen:

- SonarQube
- Semgrep
- Gitleaks
- Syft SBOM
- Trivy
- OWASP ZAP

---

## Estado del proyecto

✔ API funcional

✔ Docker

✔ JWT

✔ RBAC

✔ SonarQube

✔ Semgrep

✔ Gitleaks

✔ Syft

✔ Trivy

✔ OWASP ZAP

✔ GitHub Actions

---

## Autor

José Alejandro Pardo Martínez