from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import CheckboxInput, ListWidget

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class DepartamentoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])

class FuncaoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])

class FuncionarioForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=200)])
    cpf = StringField('CPF', validators=[DataRequired(), Length(max=14)])
    rg = StringField('RG', validators=[DataRequired(), Length(max=20)])
    ctps = StringField('CTPS', validators=[DataRequired(), Length(max=20)])
    pis = StringField('PIS', validators=[DataRequired(), Length(max=15)])
    serie = StringField('Série', validators=[DataRequired(), Length(max=10)])
    secao_setor = StringField('Seção/Setor', validators=[DataRequired(), Length(max=100)])
    data_admissao = DateField('Data de Admissão', validators=[DataRequired()])
    departamento_id = SelectField('Departamento', coerce=int, validators=[DataRequired()])
    funcao_id = SelectField('Função', coerce=int, validators=[DataRequired()])

class FornecedorForm(FlaskForm):
    cnpj = StringField('CNPJ', validators=[DataRequired(), Length(max=18)])
    nome = StringField('Nome da Empresa', validators=[DataRequired(), Length(max=200)])

class EPIForm(FlaskForm):
    nome = StringField('Nome do EPI', validators=[DataRequired(), Length(max=200)])
    marca = StringField('Marca', validators=[DataRequired(), Length(max=100)])
    periodicidade_dias = IntegerField('Periodicidade (dias)', validators=[DataRequired()])
    ca = StringField('CA', validators=[DataRequired(), Length(max=20)])
    meses = MultiCheckboxField('Meses de Troca', coerce=int)

class EntradaEPIForm(FlaskForm):
    fornecedor_id = SelectField('Fornecedor', coerce=int, validators=[DataRequired()])
    data_recebimento = DateField('Data de Recebimento', validators=[DataRequired()])
    numero_nf = StringField('Número da NF', validators=[DataRequired(), Length(max=50)])
    recebido_por = StringField('Recebido por', validators=[DataRequired(), Length(max=200)])
    observacoes = TextAreaField('Observações')

class LiberacaoEPIForm(FlaskForm):
    mes_id = SelectField('Mês', coerce=int, validators=[DataRequired()])
    departamento_id = SelectField('Departamento', coerce=int, validators=[DataRequired()])
    funcao_id = SelectField('Função', coerce=int, validators=[DataRequired()])
    funcionario_id = SelectField('Funcionário', coerce=int, validators=[DataRequired()])
