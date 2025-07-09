from flask import Flask
from models import db, Mes
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///epi_control.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões
    db.init_app(app)
    
    # Registrar blueprints/rotas
    from routes import register_routes
    register_routes(app)
    
    # Favicon route
    @app.route('/favicon.ico')
    def favicon():
        return app.send_static_file('favicon.ico')
    
    # Substituir @app.before_first_request por with app.app_context()
    with app.app_context():
        db.create_all()
        # Criar meses se não existirem
        if not Mes.query.first():
            meses = [
                ('Janeiro', 1), ('Fevereiro', 2), ('Março', 3), ('Abril', 4),
                ('Maio', 5), ('Junho', 6), ('Julho', 7), ('Agosto', 8),
                ('Setembro', 9), ('Outubro', 10), ('Novembro', 11), ('Dezembro', 12)
            ]
            for nome, numero in meses:
                mes = Mes(nome=nome, numero=numero)
                db.session.add(mes)
            db.session.commit()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
