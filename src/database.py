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
        self.connection.commit()

    def db_get(self, sql):
        self.connection.commit()
        return self._execute_query(sql=sql, get_result=True)

    def db_get_dict(self, sql):
        self.connection.commit()
        result = self._execute_query(sql=sql, get_result=True)
        return self._convert_in_dict(result)

    def _convert_in_dict(self, result):
        base_object = []
        for arg in self.cursor.description:
            base_object.append(arg.name)
        result_obj = []
        for item in result:
            objeto_dict = {}
            for i in range(len(base_object)):
                objeto_dict[base_object[i]] = item[i]
            result_obj.append(objeto_dict)
        return result_obj

    def _execute_query(self, sql: str, get_result: bool):
        self.cursor.execute(sql)
        if get_result:
            return self.cursor.fetchall()
