from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Departamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Funcao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DepartamentoFuncao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'), nullable=False)
    funcao_id = db.Column(db.Integer, db.ForeignKey('funcao.id'), nullable=False)
    departamento = db.relationship('Departamento', backref='funcoes')
    funcao = db.relationship('Funcao', backref='departamentos')

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    rg = db.Column(db.String(20), nullable=False)
    ctps = db.Column(db.String(20), nullable=False)
    pis = db.Column(db.String(15), nullable=False)
    serie = db.Column(db.String(10), nullable=False)
    secao_setor = db.Column(db.String(100), nullable=False)
    data_admissao = db.Column(db.Date, nullable=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'), nullable=False)
    funcao_id = db.Column(db.Integer, db.ForeignKey('funcao.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    departamento = db.relationship('Departamento', backref='funcionarios')
    funcao = db.relationship('Funcao', backref='funcionarios')

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Mes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    numero = db.Column(db.Integer, nullable=False)

class EPI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    periodicidade_dias = db.Column(db.Integer, nullable=False)
    ca = db.Column(db.String(20), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EPIMes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    epi_id = db.Column(db.Integer, db.ForeignKey('epi.id'), nullable=False)
    mes_id = db.Column(db.Integer, db.ForeignKey('mes.id'), nullable=False)
    epi = db.relationship('EPI', backref='meses')
    mes = db.relationship('Mes', backref='epis')

class DepartamentoFuncaoEPI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'), nullable=False)
    funcao_id = db.Column(db.Integer, db.ForeignKey('funcao.id'), nullable=False)
    epi_id = db.Column(db.Integer, db.ForeignKey('epi.id'), nullable=False)
    departamento = db.relationship('Departamento')
    funcao = db.relationship('Funcao')
    epi = db.relationship('EPI')

class EntradaEPI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)
    data_recebimento = db.Column(db.Date, nullable=False)
    numero_nf = db.Column(db.String(50), nullable=False)
    recebido_por = db.Column(db.String(200), nullable=False)
    observacoes = db.Column(db.Text)
    fornecedor = db.relationship('Fornecedor', backref='entradas')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EntradaEPIItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entrada_epi_id = db.Column(db.Integer, db.ForeignKey('entrada_epi.id'), nullable=False)
    epi_id = db.Column(db.Integer, db.ForeignKey('epi.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    entrada = db.relationship('EntradaEPI', backref='itens')
    epi = db.relationship('EPI')

class LiberacaoEPI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'), nullable=False)
    epi_id = db.Column(db.Integer, db.ForeignKey('epi.id'), nullable=False)
    mes_id = db.Column(db.Integer, db.ForeignKey('mes.id'), nullable=False)
    quantidade = db.Column(db.Integer, default=1)
    data_liberacao = db.Column(db.Date, nullable=False)
    funcionario = db.relationship('Funcionario')
    epi = db.relationship('EPI')
    mes = db.relationship('Mes')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
