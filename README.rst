Aircraft Manufacturing Application
==================================

Setup and Installation
======================

A full-stack Django web application to manage aircraft manufacturing workflows, including parts inventory, aircraft assembly tracking, user profiles, and role-based access control.

This project uses Poetry for dependency management and virtual environment handling. (Checkout the notes section before start.)

Key Features
------------

- RESTful API endpoints for parts, aircrafts, and users using Django REST Framework
- User authentication and profile management with team association
- Bootstrap-based frontend templates for dashboards, inventory, and detailed views
- Aircraft assembly details with relations to parts like wings, fuselage, avionics, tail
- Secure login/logout and session management
- Clear project structure following Django best practices

Technology Stack
----------------

- Python 3.13
- Django 5.2.1
- Django REST Framework
- PostgreSQL (or any relational DB)
- Bootstrap 5 for frontend styling

Prerequisites
-------------

- Python 3.10 or later installed on your system
- Poetry installed (https://python-poetry.org/docs/#installation)

Installation Steps
------------------

1. **Clone the repository**

   .. code-block:: bash

      git clone https://github.com/Mimakk/aircraft-manufacturing-app.git
      cd aircraft-manufacturing-app

2. **Install dependencies and create virtual environment**

   .. code-block:: bash

      poetry install

   This command will create a virtual environment and install all required dependencies.

3. **Activate the virtual environment**

   - To activate manually, run:

     .. code-block:: bash

        source $(poetry env info --path)/bin/activate

   - On Windows (PowerShell), run:

     .. code-block:: powershell

        & "$(poetry env info --path)\Scripts\Activate.ps1"

   Alternatively, you can install the Poetry shell plugin to use `poetry shell`:

   .. code-block:: bash

      poetry self add poetry-plugin-shell
      poetry shell

4. **Run Django migrations**

   .. code-block:: bash

      python manage.py migrate

5. **Create a superuser**

   .. code-block:: bash

      python manage.py createsuperuser

6. **Run the development server**

   .. code-block:: bash

      python manage.py runserver

   

Project Structure Highlights
----------------------------

- `aircrafts/`: Models, serializers, views, and templates for aircraft management
- `parts/`: Parts inventory models and API
- `users/`: User profiles, authentication, and permissions
- `templates/`: Bootstrap-based HTML templates extending `base.html`


Notes
-----

- To run Django commands without manually activating the environment, prefix them with `poetry run`, for example:

  .. code-block:: bash

     poetry run python manage.py runserver

- To prepare local development settings, you may need to create a local settings file:

  .. code-block:: bash

     mkdir -p local
     cp core/project/settings/templates/settings.dev.py ./local/settings.dev.py
