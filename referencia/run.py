from app import create_app
import schedule
import time
from threading import Thread
from app.services.data_sync import sync_data

app = create_app()

def run_scheduler():
    # Agenda a função 'scheduled_sync_data' em vez de 'sync_data'
    schedule.every().day.at("00:00").do(scheduled_sync_data)
    while True:
        schedule.run_pending()
        time.sleep(1)

def scheduled_sync_data():
    with app.app_context():
        sync_data()

if __name__ == '__main__':
    # Inicie o agendador em uma thread separada
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    #carregar pela primeira vez, remover depois
    scheduled_sync_data()

    # Execute a aplicação Flask
    app.run(debug=True)