import weaviate
from sentence_transformers import SentenceTransformer
from weaviate.classes.query import MetadataQuery
from weaviate.classes.config import Configure, VectorDistances
from weaviate.util import generate_uuid5 
import warnings
warnings.filterwarnings("ignore")


class VectorMain:
    def __init__(self, collection_name, model_name) :
        self.collection_name = collection_name
        self.client = weaviate.connect_to_local( host="weaviate",
            port=8080)        
        self.collection = None
        self.model  = SentenceTransformer(model_name, 
                            trust_remote_code=True,
                           device ="cpu"
                            )
        try:
            self.collection = self.client.collections.get(self.collection_name)
        except weaviate.RequestError:
            # Collection does not exist, create a new one
            self.collection = self.client.collections.create(
                self.collection_name,
                vector_index_config=Configure.VectorIndex.hnsw(
                    distance_metric=VectorDistances.COSINE
                ),
            )
            print("Collection created successfully.", self.collection)
    
    def insert_data(self, json_values):
       
        counter = 0
        # Insert data into the collection
        if self.collection is not None:
            for document in json_values:
                document_embedding = self.model.encode(document['query'])
                try:
                    self.collection.data.insert(
                        properties=document,
                        vector=document_embedding.tolist(),
                        uuid=generate_uuid5(document['guid'])
                        
                    )
                    counter+=1
                except Exception as E: 
                    value = "Error in inserting data  E"
        else:
            value = "Collection not initialized. Please create a collection first."
        value = f"The total data inserted is {counter}"
        
        
        return value

    def db_query_data(self, query):
        
        """
        Query the collection.

        Args:
            query (str): The query string.

        Returns:
            list: A list of response data.
        """
        # start_time = time.time()
        # Encode the query
        result =[]
        query_vector = self.model.encode(query)
        
        response =self.collection.query.hybrid(
                query=query,
                vector=query_vector.tolist(),
                query_properties=["query"],
                alpha=0.5,  # Adjust the alpha parameter as needed
                return_metadata=MetadataQuery(score=True, explain_score=True),
                limit=20
            )
        

        for o in response.objects:
            result.append(o.properties)

        return result
    
