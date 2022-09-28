# Online-Food-Delivery-Django

Add templates out of the main folder and add template path in the setting file.

make static folder in the main file and add add static url root and staticfiles_dirs path in the settings.py file.

static_root is used for the production to create a folder in the base_dir to get all the static files at one place.

to configure postgres database install pip install psycopg2

add info in the database section of settings folder

install python-decouple to hide sensitive information. refer  website for more information

message framework to show any message. We don't need to import it using context in any html page to show because it is in the context_processor (settings->context_preprocessor) which make it available globally in all the html files.

make some changes in the settings to use messages see at the last of setting page where tags to add class dynamically on different message status.

