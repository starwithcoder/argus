from pymilvus import MilvusClient  

from backend.app.core.config import settings


def get_milvus_client() -> MilvusClient:
   
    return MilvusClient(uri=settings.milvus_uri)



# if __name__ == "__main__":
#     client = get_milvus_client()
    

#     databases:list[str] = client.list_databases()
#     print("Milvus 连接成功！")
#     print("当前数据库列表：", databases)
