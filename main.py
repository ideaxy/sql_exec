from sql_exec import DatabaseConnector
import sys
import re


def parse_connect_string(connect_string):
    pattern = re.compile(r'([^/]+)/([^@]+)@([^:]+):(\d+)/([^/]+)')
    match = pattern.match(connect_string)
    if match:
        return {
            "username": match.group(1),
            "password": match.group(2),
            "ip": match.group(3),
            "port": int(match.group(4)),
            "servername": match.group(5)
        }
    else:
        raise ValueError("无效的连接串格式")



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("请提供数据库连接串作为命令行参数。")
        sys.exit(1)
    connect_string = sys.argv[1]
    try:
        with open("exec.sql", "r") as file:
            sql = file.read()
            if not sql.strip():
                raise ValueError("SQL文件内容为空，请检查文件。")
    except FileNotFoundError as e:
        print(f"文件未找到错误：{e}")
    except PermissionError as e:
        print(f"权限错误：{e}")
    except UnicodeDecodeError as e:
        print(f"Unicode解码错误：{e}")
    except ValueError as e:
        print(f"值错误：{e}")
    except Exception as e:
        print(f"其他未知错误：{e}")

    connect_dict = {}
    connect_dict = parse_connect_string(connect_string)

    database_type = sys.argv[2]

    connector = DatabaseConnector(database_type, connect_dict)
    connector.connect()

    result = connector.execute_query(sql)
    print(result)
