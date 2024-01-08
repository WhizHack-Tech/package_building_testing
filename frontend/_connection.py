#  ============================================================================
#  File Name: _connection.py
#  Description: It contains API to create index, index body in OpenSearch.

#  ----------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  =============================================================================

from opensearchpy import OpenSearch
from .opensearch_config import host, port, db_username, db_password


# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = (db_username,db_password),
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    #ca_certs = ca_certs_path
)

# Create an index with non-default settings.
# index_name = 'api-data-test'
index_body = {
  'settings': {
    "index": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    }
  }
}

def save_data(data,index_name):

    if client.indices.exists(index=index_name) is False:
        client.indices.create(index_name, body=index_body)

    client_res = client.index(
    index = index_name,
    body = data,
    refresh = True
    )

    if client_res.get("result") is None:
      return {"msg":"Oops! something is wrong with OpenSearch connection.","error":"s_is_w"}


    return {
      "_id" : client_res.get("_id"),
      "result" : client_res.get("result")
    }