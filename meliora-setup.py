import os
import subprocess
subprocess.run(["pip", "install", 'click'])
import click

@click.command()
def install_choice():
    os.chdir("./meliora")
    subprocess.run(["pip", "install", "-r", "requirements.txt"])
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_md"])
    os.chdir("..")
    if click.confirm(click.style("Do you want to install it globally", fg='yellow')):
        subprocess.run(["pip", "install", "."])
    else:
        subprocess.run(["pip", "install", "-e", "."])
    click.echo(click.style("meliora is ready! use python -m meliora <DIRECTORY_PATH> to run it.", fg='green'))

install_choice()
