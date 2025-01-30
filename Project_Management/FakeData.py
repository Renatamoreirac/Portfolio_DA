from faker import Faker
import pandas as pd
import random
import sqlite3

# Configurando Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

# Gerar dados para a tabela Projetos
def generate_projects(n=10, managers=[]):
    projects = []
    for _ in range(n):
        projects.append({
            "project_id": fake.uuid4(),
            "name": fake.bs().capitalize(),
            "description": fake.text(max_nb_chars=100),
            "start_date": fake.date_this_decade(before_today=True),
            "end_date": fake.date_this_decade(after_today=True),
            "budget": round(random.uniform(10000, 1000000), 2),
            "manager_id": random.choice(managers) if managers else None
        })
    return pd.DataFrame(projects)

# Gerar dados para a tabela Colaboradores (com gestores)
def generate_collaborators(n=20):
    collaborators = []
    for _ in range(n):
        collaborator_id = fake.uuid4()
        role = random.choice(["Manager", "Developer", "Analyst", "Designer", "QA"])
        collaborators.append({
            "collaborator_id": collaborator_id,
            "name": fake.name(),
            "role": role,
            "email": fake.email(),
            "phone": fake.phone_number(),
            "hire_date": fake.date_this_decade(before_today=True),
            # Gerar URL para imagem com base no ID
            "picture": f"https://robohash.org/{collaborator_id}.png?set=set1",
            # Associar um gestor caso não seja Manager
            "team_manager_id": None if role == "Manager" else random.choice(collaborators)["collaborator_id"] if collaborators else None
        })
    return pd.DataFrame(collaborators)

# Gerar dados para a tabela Metas dos Colaboradores
def generate_goals(collaborators, n=50):
    goals = []
    for _ in range(n):
        goals.append({
            "goal_id": fake.uuid4(),
            "collaborator_id": random.choice(collaborators["collaborator_id"]),
            "description": fake.sentence(nb_words=8),
            "deadline": fake.date_this_decade(after_today=True),
            "status": random.choice(["Not Started", "In Progress", "Completed"])
        })
    return pd.DataFrame(goals)

# Gerar dados para a tabela Tarefas
def generate_tasks(projects, n=50):
    tasks = []
    for _ in range(n):
        tasks.append({
            "task_id": fake.uuid4(),
            "project_id": random.choice(projects["project_id"]),
            "name": fake.catch_phrase(),
            "status": random.choice(["Not Started", "In Progress", "Completed"]),
            "start_date": fake.date_this_decade(before_today=True),
            "end_date": fake.date_this_decade(after_today=True),
            "priority": random.choice(["Low", "Medium", "High"])
        })
    return pd.DataFrame(tasks)

# Gerar dados para a tabela Alocações
def generate_allocations(collaborators, projects, n=30):
    allocations = []
    for _ in range(n):
        allocations.append({
            "allocation_id": fake.uuid4(),
            "project_id": random.choice(projects["project_id"]),
            "collaborator_id": random.choice(collaborators["collaborator_id"]),
            "allocation_percentage": random.choice([25, 50, 75, 100])
        })
    return pd.DataFrame(allocations)

# Gerar dados para a tabela Horas Trabalhadas
def generate_hours_worked(collaborators, tasks, n=100):
    hours_worked = []
    for _ in range(n):
        hours_worked.append({
            "entry_id": fake.uuid4(),
            "task_id": random.choice(tasks["task_id"]),
            "collaborator_id": random.choice(collaborators["collaborator_id"]),
            "date": fake.date_this_year(),
            "hours": random.uniform(1, 8)
        })
    return pd.DataFrame(hours_worked)

# Criar as tabelas
collaborators_df = generate_collaborators()
managers = collaborators_df[collaborators_df["role"] == "Manager"]["collaborator_id"].tolist()
projects_df = generate_projects(managers=managers)
tasks_df = generate_tasks(projects_df)
allocations_df = generate_allocations(collaborators_df, projects_df)
hours_worked_df = generate_hours_worked(collaborators_df, tasks_df)
goals_df = generate_goals(collaborators_df)

# Salvar os DataFrames como arquivos CSV
collaborators_df.to_csv('Collaborators.csv', index=False, encoding='utf-8-sig')
projects_df.to_csv('Projects.csv', index=False, encoding='utf-8-sig')
tasks_df.to_csv('Tasks.csv', index=False, encoding='utf-8-sig')
allocations_df.to_csv('Allocations.csv', index=False, encoding='utf-8-sig')
hours_worked_df.to_csv('HoursWorked.csv', index=False, encoding='utf-8-sig')
goals_df.to_csv('Goals.csv', index=False, encoding='utf-8-sig')
