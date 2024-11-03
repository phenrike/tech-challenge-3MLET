from infra.db_connection import db

class PostgresRepository:

    @staticmethod
    def save_data(model, data):
        """
        Salva uma lista de dicionários no banco de dados usando o modelo fornecido.
        
        :param model: O modelo SQLAlchemy no qual os dados serão inseridos.
        :param data: Uma lista de dicionários contendo os dados a serem inseridos.
        """
        try:
            # Itera sobre os dados e cria instâncias do modelo
            for row in data:
                record = model(**row)  # Cria uma instância do modelo com os dados de cada linha
                db.session.add(record)  # Adiciona o registro à sessão

            # Comita todas as mudanças
            db.session.commit()
        
        except Exception as e:
            # Faz rollback em caso de erro
            db.session.rollback()
            print(f"Erro ao salvar dados: {e}")
        
        finally:
            # Fecha a sessão para liberar recursos
            db.session.close()

    @staticmethod
    def clear_data(model):
        """
        Limpa as tabelas do banco de dados.        
        """
        try:
            # Delete all records from the model's table
            db.session.query(model).delete()
            # Commit the changes to the database
            db.session.commit()
            print("Data cleared successfully.")
        
        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            print(f"Error while clearing data: {e}")
        
        finally:
            # Close the session to free resources
            db.session.close()