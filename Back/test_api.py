from neo4j import GraphDatabase
from neo4j_graphrag.experimental.components.kg_writer import Neo4jWriter
from neo4j_graphrag.experimental.pipeline import Pipeline

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "12345678")
DATABASE_NAME = "twitter"


def request_database(request):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print("Connexion réussie à la base de données Neo4j.")

        with driver.session(database=DATABASE_NAME) as session:
            print("Connection Established")

            try:
                result = session.run(request)
                records = [record for record in result]
                summary = result.consume()

                print("la requête à retoruné {records_count} résultats en {time} ms.".format(
                        records_count=len(records),
                        time=summary.result_available_after,
                    ))
                
                for record in records:
                    print(record)


            except Exception as e:
                print("Erreur lors de la connexion ou de l'exécution de la requête :", e)


request_database("match(n:User {name:'Holly'}) return n.followers")    

