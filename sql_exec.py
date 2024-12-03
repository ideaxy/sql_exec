import pymysql
import cx_Oracle
from prettytable import PrettyTable


class DatabaseConnector:
    def __init__(self, database_type, conn_dict):
        self.database_type = database_type
        self.conn_dict = conn_dict
        self.connection = None

    def connect(self):
        if self.database_type == "mysql":
            self.connect_mysql()
        elif self.database_type == "oracle":
            self.connect_oracle()
        else:
            raise ValueError(f"不支持的数据库类型: {self.database_type}")

    def connect_mysql(self):
        try:
            self.connection = pymysql.connect(
                host=self.conn_dict["ip"],
                user=self.conn_dict["username"],
                password=self.conn_dict["password"],
                port=self.conn_dict["port"],
                database=self.conn_dict["servername"]
            )
        except pymysql.Error as e:
            print(f"数据库连接失败，错误原因: {e}")
            exit(1)
        except Exception as e:
            print(f"发生其他未知错误: {e}")
            exit(1)

    def connect_oracle(self):
        try:
            dsn = cx_Oracle.makedsn(self.conn_dict["ip"], self.conn_dict["port"], service_name=self.conn_dict["servername"])
            self.connection = cx_Oracle.connect(
                user=self.conn_dict["username"],
                password=self.conn_dict["password"],
                dsn=dsn
            )
        except cx_Oracle.DatabaseError as e:
            print(f"数据库连接失败，错误原因: {e}")
            exit(1)
        except Exception as e:
            print(f"发生其他未知错误: {e}")
            exit(1)

    def execute_query(self, sql):
        if sql.lower().startswith("select"):
            sql = sql.replace(";","")
            cursor = self.connection.cursor()
            print(f"sql:{sql}")
            cursor.execute(sql)
            results = cursor.fetchall()

            # 使用PrettyTable来美化结果输出
            table = PrettyTable()
            # 获取列名作为表头
            columns = [desc[0] for desc in cursor.description]
            table.field_names = columns

            for row in results:
                table.add_row(row)

            # 将美化后的表格内容写入文件
            with open("select_results.txt", "w", encoding="utf-8") as f:
                f.write("SQL:" + sql + "\n")
                f.write(str(table) + "\n")

            cursor.close()
            self.connection.close()
            return "查询结果已输出到select_results.txt文件"
        else:
            self.connection.close()
            raise ValueError("无效的SQL语句类型")
