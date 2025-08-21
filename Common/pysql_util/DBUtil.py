import pymysql


class DBUtil(object):
    # 添加类属性
    connect = None

    @classmethod  # 类方法、__私有方法
    def __get_connection(self):
        if self.connect is None:
            self.connect = pymysql.connect()
        return self.connect

    @classmethod
    def __close_connection(self):
        if self.connect is not None:
            self.connect.close()
            self.connect = None

    @classmethod
    def select_one(cls, sql):
        cursor = None
        result = None
        try:
            # 获取链接
            cls.connect = cls.__get_connection()
            # 获取游标
            cursor = cls.connect.cursor()
            # 执行查询语句
            cursor.execute(sql)
            # 提取一条数据
            result = cursor.fetchone()
        except Exception as e:
            print(str(e))
        finally:
            # 关闭游标
            cursor.close()
            # 关闭连接
            cls.__close_connection()
            return result

    @classmethod
    def update_db(cls, sql):
        cursor = None
        result = None
        try:
            # 获取链接
            cls.connect = cls.__get_connection()
            # 获取游标
            cursor = cls.connect.cursor()
            # 执行查询语句
            cursor.execute(sql)
            #提交事务
            cls.connect.commit()
        except Exception as e:
            print(str(e))
            #回滚事务
            cls.connect.rollback()
        finally:
            # 关闭游标
            cursor.close()
            # 关闭连接
            cls.__close_connection()
            return result
