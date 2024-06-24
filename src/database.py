import psycopg2


class Database():
    def __init__(self, host, user, password, db_name, port) -> None:
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=db_name,
        )
        self.cursor = self.connection.cursor()

    def db_query(self, sql):
        self._execute_query(sql=sql, get_result=False)
        self.conexao.commit()

    def db_get(self, sql):
        self.conexao.commit()
        return self._execute_query(sql=sql, get_result=True)

    def _execute_query(self, sql:str, get_result:bool):
        cursor = self.conexao.cursor()
        cursor.execute(sql)
        if get_result:
            return cursor.fetchall()