This branch consists of Python programs:
 * to populate PostgreSQL database
   * directly
   * using Django
 * to read from PostgreSQL database
   * directly
   * using Django

How to run: 
* Django project
  * install requirements in django_project/requirements.txt
  * customize settings:
  	* open django_project/django_project/settings.py
  	* update information in DATABASES field to reflect your database
  * cd django_project/
  * to populate run "python manage.py populate <absolute path to parameter json>"
  * to query run "python manage.py query"

* Python only
  * cd python_only
  * install requirements in requirements.txt
  * modify config.py to reflect your database information
  * python create_tables.py
  * python populate.py <parameter json here>
    * sample_parameters.json is included: python populate.py sample_parameters.json
  * python query.py