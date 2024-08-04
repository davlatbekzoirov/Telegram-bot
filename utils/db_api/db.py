from typing import Union
import asyncpg
from asyncpg import Connection, Pool
from data import config

class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command: str, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
                return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INTEGER NOT NULL,
            phone_number VARCHAR(20),
            role VARCHAR(10) NOT NULL CHECK (role IN ('applicant', 'student'))
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql: str, parameters: dict) -> tuple:
        sql += " AND ".join([f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)])
        return sql, tuple(parameters.values())

    async def add_user(self, name: str, age: int, phone_number: str, role: str):
        sql = "INSERT INTO Users (name, age, phone_number, role) VALUES($1, $2, $3, $4) RETURNING *"
        return await self.execute(sql, name, age, phone_number, role, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user(self, user_id: int, **kwargs):
        sql = "UPDATE Users SET " + ", ".join([f"{key} = ${idx}" for idx, key in enumerate(kwargs.keys(), start=2)]) + " WHERE id = $1"
        return await self.execute(sql, user_id, *kwargs.values(), execute=True)

    async def delete_user(self, user_id: int):
        sql = "DELETE FROM Users WHERE id = $1"
        return await self.execute(sql, user_id, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    # Applicants
    async def create_table_applicants(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Applicants (
            id BIGINT PRIMARY KEY,
            selected_option_id INT NOT NULL,
            FOREIGN KEY (selected_option_id) REFERENCES ApplicantOptions (id) ON DELETE CASCADE
        );
        """
        await self.execute(sql, execute=True)

    async def add_applicant(self, applicant_id: int, selected_option_id: int):
        sql = "INSERT INTO Applicants (id, selected_option_id) VALUES($1, $2) RETURNING *"
        return await self.execute(sql, applicant_id, selected_option_id, fetchrow=True)

    async def select_all_applicants(self):
        sql = "SELECT * FROM Applicants"
        return await self.execute(sql, fetch=True)
    
    async def delete_applicants(self):
        await self.execute("DELETE FROM Applicants WHERE TRUE", execute=True)

    # Applicant questions
    async def create_table_applicant_questions(self):
        sql = """
        CREATE TABLE IF NOT EXISTS ApplicantQuestions (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def add_applicant_question(self, text: str):
        sql = "INSERT INTO ApplicantQuestions (text) VALUES($1) RETURNING *"
        return await self.execute(sql, text, fetchrow=True)
    
    async def select_all_applicant_questions(self):
        sql = "SELECT * FROM ApplicantQuestions"
        return await self.execute(sql, fetch=True)
    
    # Applicant options
    async def create_table_applicant_options(self):
        sql = """
        CREATE TABLE IF NOT EXISTS ApplicantOptions (
            id SERIAL PRIMARY KEY,
            question_id INT NOT NULL,
            text VARCHAR(255) NOT NULL,
            FOREIGN KEY (question_id) REFERENCES ApplicantQuestions (id) ON DELETE CASCADE
        );
        """
        await self.execute(sql, execute=True)

    async def add_applicant_option(self, question_id: int, text: str):
        sql = "INSERT INTO ApplicantOptions (question_id, text) VALUES($1, $2) RETURNING *"
        return await self.execute(sql, question_id, text, fetchrow=True)
    
    async def select_all_applicant_options(self):
        sql = "SELECT * FROM ApplicantOptions"
        return await self.execute(sql, fetch=True)

    async def drop_applicant_tables(self):
        await self.execute("DROP TABLE IF EXISTS Applicants", execute=True)
        await self.execute("DROP TABLE IF EXISTS ApplicantOptions", execute=True)
        await self.execute("DROP TABLE IF EXISTS ApplicantQuestions", execute=True)

    # Students
    async def create_table_students(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Students (
            id BIGINT PRIMARY KEY,
            selected_option_id INT NOT NULL,
            FOREIGN KEY (selected_option_id) REFERENCES StudentOptions (id) ON DELETE CASCADE
        );
        """
        await self.execute(sql, execute=True)

    async def add_student(self, student_id: int, selected_option_id: int):
        sql = "INSERT INTO Students (id, selected_option_id) VALUES($1, $2) RETURNING *"
        return await self.execute(sql, student_id, selected_option_id, fetchrow=True)

    async def select_all_students(self):
        sql = "SELECT * FROM Students"
        return await self.execute(sql, fetch=True)
    
    async def delete_students(self):
        await self.execute("DELETE FROM Students WHERE TRUE", execute=True)

    # Student questions
    async def create_table_student_questions(self):
        sql = """
        CREATE TABLE IF NOT EXISTS StudentQuestions (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def add_student_question(self, text: str):
        sql = "INSERT INTO StudentQuestions (text) VALUES($1) RETURNING *"
        return await self.execute(sql, text, fetchrow=True)
    
    async def select_all_student_questions(self):
        sql = "SELECT * FROM StudentQuestions"
        return await self.execute(sql, fetch=True)
    
    # Student options
    async def create_table_student_options(self):
        sql = """
        CREATE TABLE IF NOT EXISTS StudentOptions (
            id SERIAL PRIMARY KEY,
            question_id INT NOT NULL,
            text VARCHAR(255) NOT NULL,
            FOREIGN KEY (question_id) REFERENCES StudentQuestions (id) ON DELETE CASCADE
        );
        """
        await self.execute(sql, execute=True)

    async def add_student_option(self, question_id: int, text: str):
        sql = "INSERT INTO StudentOptions (question_id, text) VALUES($1, $2) RETURNING *"
        return await self.execute(sql, question_id, text, fetchrow=True)
    
    async def select_all_student_options(self):
        sql = "SELECT * FROM StudentOptions"
        return await self.execute(sql, fetch=True)

    async def drop_student_tables(self):
        await self.execute("DROP TABLE IF EXISTS Students", execute=True)
        await self.execute("DROP TABLE IF EXISTS StudentOptions", execute=True)
        await self.execute("DROP TABLE IF EXISTS StudentQuestions", execute=True)
