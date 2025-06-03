import os
import click
from sqlalchemy import text
from app.db.database import engine
from app.core.security import get_password_hash
from app.models import User

@click.group()
def cli():
    pass

@cli.command()
def init_database():
    """Initialize the database with tables."""
    click.echo("Creating database tables...")
    
    # Read and execute SQL file
    sql_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'init_db.sql')
    with open(sql_file_path, 'r') as file:
        sql_commands = file.read()
        
    with engine.connect() as connection:
        connection.execute(text(sql_commands))
        connection.commit()
    
    click.echo("Database tables created successfully!")

@cli.command()
@click.option('--email', prompt='Email', help='Admin email')
@click.option('--password', prompt='Password', hide_input=True, help='Admin password')
@click.option('--name', prompt='Name', help='Admin name')
def create_admin(email, password, name):
    """Create an admin user."""
    db = SessionLocal()
    try:
        user = User(
            email=email,
            password=get_password_hash(password),
            name=name
        )
        db.add(user)
        db.commit()
        click.echo(f"Admin user {email} created successfully!")
    except Exception as e:
        click.echo(f"Error creating admin user: {str(e)}")
    finally:
        db.close()

if __name__ == '__main__':
    cli() 