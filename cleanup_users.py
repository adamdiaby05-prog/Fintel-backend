"""
Script pour nettoyer les utilisateurs sans numéro de téléphone
Utilise SQL brut pour éviter les problèmes de relations SQLAlchemy
"""
from app.core.database import engine
from sqlalchemy import text

def cleanup_users():
    try:
        with engine.connect() as conn:
            # Compter les utilisateurs sans numéro de téléphone
            count_result = conn.execute(text("""
                SELECT COUNT(*) FROM users 
                WHERE phone_number IS NULL OR phone_number = '' OR phone_number = ' '
            """))
            count = count_result.scalar()
            print(f"Utilisateurs trouves sans numero de telephone: {count}")
            
            if count > 0:
                # Supprimer les utilisateurs sans numéro de téléphone
                delete_result = conn.execute(text("""
                    DELETE FROM users 
                    WHERE phone_number IS NULL OR phone_number = '' OR phone_number = ' '
                """))
                deleted_count = delete_result.rowcount
                conn.commit()
                print(f"{deleted_count} utilisateur(s) supprime(s)")
            else:
                print("Aucun utilisateur a supprimer")
            
            # Afficher les utilisateurs restants
            remaining_result = conn.execute(text("""
                SELECT id, phone_number, email, 
                       CASE WHEN hashed_password IS NOT NULL THEN 'Oui' ELSE 'Non' END as has_password
                FROM users
                ORDER BY id
            """))
            remaining = remaining_result.fetchall()
            
            print(f"\nUtilisateurs restants: {len(remaining)}")
            if len(remaining) > 0:
                print("\nID | Phone Number | Email | Has Password")
                print("-" * 60)
                for row in remaining:
                    print(f"{row[0]} | {row[1] or '(vide)'} | {row[2] or '(vide)'} | {row[3]}")
            else:
                print("La table users est vide")
                
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    cleanup_users()

