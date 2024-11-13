<!-- Initializing the project -->
In this section, you are going to explore how to use sam init to initialize the Unicorn Properties service.

In the terminal, go to the unicorn folder (root folder). Run the sam init command terminal, and specify the --location option as follows:

    sam init --location 'https://ws-assets-prod-iad-r-iad-ed304a55c2ca1aee.s3.us-east-1.amazonaws.com/9a27e484-7336-4ed0-8f90-f2747e4ac65c/init/python_unicorn_properties.zip'

When cookiecutter asks for a project name, e.g. project_name [unicorn_properties]: keep default value.

Open the Unicorn Properties folder in your terminal, and explore the project source and test projects.

    cd unicorn_properties/
    poetry install
    poetry export --without-hashes --format=requirements.txt --output=src/requirements.txt    

