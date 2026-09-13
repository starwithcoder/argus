"""
Test configuration settings
"""
from backend.app.core.config import settings



"""
测试Mysql url获取
"""
def test_get_db_url():
    db_url: str | None = settings.database_uri
    #assert db_url is not None
    print(db_url)

"""
测试Redis url获取
"""
def test_get_redis_url():
    redis_url: str | None = settings.redis_uri
    #assert db_url is not None
    print(redis_url)


"""
测试应用基础配置
"""
def test_app_config():
    app_name = settings.PROJECT_NAME
    assert app_name == "argus-backend"



if __name__ == "__main__":
    #test_get_db_connection()
    #test_app_config()
    #test_get_db_url()
    test_get_redis_url()