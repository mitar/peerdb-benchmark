This branch consists of Python programs:
 * to populate PostgreSQL database
   * directly (`python_only/populate.py`)
   * using Django (`populate` Django management command)
 * to read from PostgreSQL database
   * directly:
     * `python_only/query1.py` reads related documents by creating one huge join
     * `python_only/query2.py` reads related documents in bulk, storing all documents in memory and reconstructing them
   * using Django (`query` Django management command)

How to make it work:
* Django project
  * install requirements in `django_project/requirements.txt`
  * customize settings:
  	* open `django_project/django_project/settings.py`
  	* update information in `DATABASES` field to reflect your database
  * cd `django_project/`
  * first create tables in the database: `python syncdb`
  * to populate run `python manage.py populate <absolute path to parameter json>`
  * to query run `python manage.py query`

* Directly using Python
  * cd `python_only`
  * install requirements in `python_only/requirements.txt`
  * modify `config.py` to reflect your database information
  * python `create_tables.py`
  * python `populate.py <parameter json here>`
  * `python query1.py` or `python query2.py`

The queries aggregate content of all posts for each tag name but do not output this data.

`benchmark.py` scripts conveniently run both populate and query for all JSON files in a directory.
