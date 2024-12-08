from neo4j import GraphDatabase

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "12345678")
DATABASE_NAME = "twitter"


def execute_query(query, params=None):
    """Execute a Cypher query and return the results."""
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            with driver.session(database=DATABASE_NAME) as session:
                try:
                    result = session.run(query, params)
                    return [record for record in result]
                except Exception as e:
                    print(f"Erreur lors de l'exécution de la requête : {e}")
                    return None
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None


# Fonctionnalités utilisateur

def get_user_attributes(screen_name):
    """Affiche les attributs d'un utilisateur spécifique."""
    try:
        query = """
        MATCH (u:User {screen_name: $screen_name})
        RETURN u
        """
        result = execute_query(query, {"screen_name": screen_name})
        if result:
            user = result[0]["u"]
            print(f"Attributs de l'utilisateur '{screen_name}':")
            for key, value in user.items():
                print(f" - {key}: {value}")
            return user
        else:
            print(f"Aucun utilisateur trouvé avec le screen_name '{screen_name}'.")
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération des attributs de l'utilisateur '{screen_name}': {e}")


def create_user(screen_name, name, followers=0, following=0, profile_image_url=None, location=None, url=None):
    """Crée un utilisateur avec les attributs fournis."""
    try:
        query = """
        CREATE (u:User {
            screen_name: $screen_name,
            name: $name,
            followers: $followers,
            following: $following,
            profile_image_url: $profile_image_url,
            location: $location,
            url: $url
        })
        RETURN u
        """
        execute_query(query, {
            "screen_name": screen_name,
            "name": name,
            "followers": followers,
            "following": following,
            "profile_image_url": profile_image_url,
            "location": location,
            "url": url
        })
        print(f"Utilisateur '{screen_name}' créé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création de l'utilisateur '{screen_name}': {e}")


def delete_user(screen_name):
    """Supprime un utilisateur et toutes ses relations."""
    try:
        query = """
        MATCH (u:User {screen_name: $screen_name})
        DETACH DELETE u
        """
        execute_query(query, {"screen_name": screen_name})
        print(f"Utilisateur '{screen_name}' supprimé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression de l'utilisateur '{screen_name}': {e}")


def follow_user(follower, followee):
    """Ajoute une relation FOLLOWS entre deux utilisateurs."""
    try:
        query = """
        MATCH (u1:User {screen_name: $follower}), (u2:User {screen_name: $followee})
        MERGE (u1)-[:FOLLOWS]->(u2)
        RETURN u1, u2
        """
        execute_query(query, {"follower": follower, "followee": followee})
        print(f"L'utilisateur '{follower}' suit maintenant '{followee}'.")
    except Exception as e:
        print(f"Erreur lors de la relation FOLLOWS entre '{follower}' et '{followee}': {e}")


def unfollow_user(follower, followee):
    """Supprime une relation FOLLOWS entre deux utilisateurs."""
    try:
        query = """
        MATCH (u1:User {screen_name: $follower})-[r:FOLLOWS]->(u2:User {screen_name: $followee})
        DELETE r
        RETURN u1, u2
        """
        execute_query(query, {"follower": follower, "followee": followee})
        print(f"L'utilisateur '{follower}' ne suit plus '{followee}'.")
    except Exception as e:
        print(f"Erreur lors de la suppression de la relation FOLLOWS entre '{follower}' et '{followee}': {e}")


def post_tweet(user, tweet_id, content, source=None):
    """Crée un tweet pour un utilisateur."""
    try:
        query = """
        MATCH (u:User {screen_name: $user})
        CREATE (t:Tweet {
            id_str: $tweet_id,
            text: $content,
            favorites: 0,
            created_at: datetime()
        })
        MERGE (u)-[:POSTS]->(t)
        WITH t
        OPTIONAL MATCH (s:Source {name: $source})
        MERGE (t)-[:USING]->(s)
        RETURN t
        """
        execute_query(query, {"user": user, "tweet_id": tweet_id, "content": content, "source": source})
        print(f"Tweet '{tweet_id}' créé avec succès pour l'utilisateur '{user}'.")
    except Exception as e:
        print(f"Erreur lors de la création du tweet '{tweet_id}' pour l'utilisateur '{user}': {e}")


def delete_tweet(tweet_id):
    """Supprime un tweet et ses relations."""
    try:
        query = """
        MATCH (t:Tweet {id_str: $tweet_id})
        DETACH DELETE t
        """
        execute_query(query, {"tweet_id": tweet_id})
        print(f"Tweet '{tweet_id}' supprimé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression du tweet '{tweet_id}': {e}")


def like_tweet(tweet_id):
    """Incrémente le compteur de likes d'un tweet."""
    try:
        query = """
        MATCH (t:Tweet {id_str: $tweet_id})
        SET t.favorites = t.favorites + 1
        RETURN t.favorites AS likes
        """
        result = execute_query(query, {"tweet_id": tweet_id})
        if result:
            print(f"Le tweet '{tweet_id}' a maintenant {result[0]['likes']} likes.")
    except Exception as e:
        print(f"Erreur lors de l'ajout d'un like au tweet '{tweet_id}': {e}")


def update_user_profile(screen_name, name=None, location=None, url=None, profile_image_url=None):
    """Met à jour le profil d'un utilisateur."""
    try:
        query = """
        MATCH (u:User {screen_name: $screen_name})
        SET u.name = COALESCE($name, u.name),
            u.location = COALESCE($location, u.location),
            u.url = COALESCE($url, u.url),
            u.profile_image_url = COALESCE($profile_image_url, u.profile_image_url)
        RETURN u
        """
        execute_query(query, {
            "screen_name": screen_name,
            "name": name,
            "location": location,
            "url": url,
            "profile_image_url": profile_image_url
        })
        print(f"Profil de l'utilisateur '{screen_name}' mis à jour avec succès.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour du profil de l'utilisateur '{screen_name}': {e}")


# Statistiques et analyses

def get_user_followers_count(screen_name):
    """Affiche le nombre de followers d'un utilisateur spécifique."""
    try:
        query = """
        MATCH (u:User {screen_name: $screen_name})
        RETURN u.followers AS followers
        """
        result = execute_query(query, {"screen_name": screen_name})
        if result:
            followers = result[0]["followers"]
            print(f"L'utilisateur '{screen_name}' a {followers} followers.")
            return followers
        else:
            print(f"Aucun utilisateur trouvé avec le screen_name '{screen_name}'.")
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération des followers de l'utilisateur '{screen_name}': {e}")


def user_statistics():
    """Affiche des statistiques globales sur les utilisateurs."""
    try:
        query = """
        MATCH (u:User)-[:FOLLOWS]->(f)
        WITH u, COUNT(f) AS following_count
        RETURN 
            COUNT(u) AS user_count, 
            AVG(following_count) AS avg_following,
            AVG(u.followers) AS avg_followers
        """
        result = execute_query(query)
        if result:
            stats = result[0]
            print(f"Nombre total d'utilisateurs : {stats['user_count']}")
            print(f"Nombre moyen d'abonnements par utilisateur : {stats['avg_following']:.2f}")
            print(f"Nombre moyen de followers par utilisateur : {stats['avg_followers']:.2f}")
    except Exception as e:
        print(f"Erreur lors du calcul des statistiques utilisateurs : {e}")


def tweet_statistics():
    """Affiche des statistiques globales sur les tweets."""
    try:
        query = """
        MATCH (t:Tweet)
        RETURN COUNT(t) AS tweet_count, 
               AVG(t.favorites) AS avg_favorites
        """
        result = execute_query(query)
        if result:
            stats = result[0]
            print(f"Nombre total de tweets : {stats['tweet_count']}")
            print(f"Nombre moyen de likes par tweet : {stats['avg_favorites']:.2f}")
    except Exception as e:
        print(f"Erreur lors du calcul des statistiques des tweets : {e}")


def calculate_handshakes(user1, user2):
    """Calcule à combien de poignées de main deux utilisateurs sont l'un de l'autre et affiche le chemin."""
    try:
        query = """
        MATCH (u1:User {screen_name: $user1}), (u2:User {screen_name: $user2})
        MATCH path = shortestPath((u1)-[:FOLLOWS*]-(u2))
        RETURN [n IN nodes(path) | n.screen_name] AS path,
               length(path) AS handshakes
        """
        result = execute_query(query, {"user1": user1, "user2": user2})
        if result and result[0]["handshakes"] is not None:
            path = result[0]["path"]
            handshakes = result[0]["handshakes"]
            print(f"{user1} et {user2} sont à {handshakes} poignées de main l'un de l'autre.")
            print(f"Chemin : {' -> '.join(path)}")
        else:
            print(f"Aucun chemin trouvé entre {user1} et {user2}.")
    except Exception as e:
        print(f"Erreur lors du calcul des poignées de main entre '{user1}' et '{user2}': {e}")


# Exemple d'utilisation
if __name__ == "__main__":
    user_statistics()
    tweet_statistics()
    #follow_user("new_user123", "NASAPersevere")
    calculate_handshakes("new_user123", "pranitahakim1")
    get_user_attributes("new_user123")
    get_user_followers_count("NASAPersevere")



"""
    create_user(
        screen_name="new_user123",
        name="New User",
        followers=100,
        following=50,
        profile_image_url="http://example.com/profile.jpg",
        location="Somewhere",
        url="http://example.com"
    )
 """   

