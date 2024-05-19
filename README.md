# django-base-template

Project Setup/ Install
<ul>
<li> Clone the project `https://github.com/sylnoviait/django-base-template`</li>
<li> create virtuat environment `python -m venv venv` </li>
<li> activate virtual environment `venv\Scripts\activate`</li>
<li> pip install -r requirements.txt</li>
<li> copy .env.example to .env</li>



<li> Setup the database in settings.py</li>
<li> After setup run `python manage.py migrate`</li>
<li> now run `python manage.py runserver`</li>
</ul>

<h2>Few Essential Commands</h2>

## After install any package please run below commands

pip freeze > requirements.txt

## To create app 

<ul>
<li> First, Create a folder inside apps folder `mkdir apps\folder_name`</li>
<li> then run below commands `python manage.py startapp app_name apps/app_name` </li>
</ul>


## To create app 

<ul>
<li> TO, Create a Migrations</li>
<li> then run below commands `python manage.py makemigrations` </li>
<li>To apply a migration</li>
<li> then run below commands `python manage.py migrate` </li>

</ul>
