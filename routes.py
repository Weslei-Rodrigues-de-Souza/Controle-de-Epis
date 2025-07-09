from flask import render_template, request, jsonify, redirect, url_for, flash
from models import *
from forms import *
from datetime import datetime

def register_routes(app):
    
    @app.route('/')
    def index():
        return render_template('index.html')

    # ==================== ROTAS PARA DEPARTAMENTOS ====================
    @app.route('/departamentos')
    def departamentos():
        try:
            departamentos = Departamento.query.filter_by(ativo=True).all()
            result = []
            for d in departamentos:
                result.append({
                    'id': d.id, 
                    'nome': d.nome,
                    'created_at': d.created_at.strftime('%Y-%m-%d %H:%M:%S') if d.created_at else None
                })
            return jsonify(result)
        except Exception as e:
            print(f"Erro ao buscar departamentos: {e}")
            return jsonify([])

    @app.route('/departamento', methods=['GET', 'POST'])
    def departamento():
        form = DepartamentoForm()
        if form.validate_on_submit():
            dept = Departamento(nome=form.nome.data)
            db.session.add(dept)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Departamento cadastrado com sucesso!'})
        return render_template('modals/departamento_modal.html', form=form)

    @app.route('/departamento/<int:id>', methods=['PUT', 'DELETE', 'POST'])
    def departamento_edit_delete(id):
        dept = Departamento.query.get_or_404(id)
        if request.method == 'PUT':
            data = request.get_json()
            dept.nome = data['nome']
            db.session.commit()
            return jsonify({'success': True, 'message': 'Departamento atualizado!'})
        elif request.method == 'DELETE':
            dept.ativo = False
            db.session.commit()
            return jsonify({'success': True, 'message': 'Departamento removido!'})

    # ==================== ROTAS PARA FUNÇÕES ====================
    @app.route('/funcoes')
    def funcoes():
        try:
            funcoes = Funcao.query.filter_by(ativo=True).all()
            result = []
            for f in funcoes:
                result.append({
                    'id': f.id, 
                    'nome': f.nome,
                    'created_at': f.created_at.strftime('%Y-%m-%d %H:%M:%S') if f.created_at else None
                })
            return jsonify(result)
        except Exception as e:
            print(f"Erro ao buscar funções: {e}")
            return jsonify([])

    @app.route('/funcao', methods=['GET', 'POST'])
    def funcao():
        form = FuncaoForm()
        if form.validate_on_submit():
            func = Funcao(nome=form.nome.data)
            db.session.add(func)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Função cadastrada com sucesso!'})
        return render_template('modals/funcao_modal.html', form=form)

    @app.route('/funcao/<int:id>', methods=['PUT', 'DELETE'])
    def funcao_edit_delete(id):
        func = Funcao.query.get_or_404(id)
        if request.method == 'PUT':
            data = request.get_json()
            func.nome = data['nome']
            db.session.commit()
            return jsonify({'success': True, 'message': 'Função atualizada!'})
        elif request.method == 'DELETE':
            func.ativo = False
            db.session.commit()
            return jsonify({'success': True, 'message': 'Função removida!'})

    # ==================== ROTAS PARA FUNCIONÁRIOS ====================
    @app.route('/funcionarios')
    def funcionarios():
        try:
            funcionarios = Funcionario.query.filter_by(ativo=True).all()
            result = []
            for f in funcionarios:
                result.append({
                    'id': f.id, 
                    'nome': f.nome, 
                    'cpf': f.cpf,
                    'departamento': f.departamento.nome if f.departamento else 'N/A',
                    'funcao': f.funcao.nome if f.funcao else 'N/A',
                    'data_admissao': f.data_admissao.strftime('%Y-%m-%d') if f.data_admissao else None
                })
            return jsonify(result)
        except Exception as e:
            print(f"Erro ao buscar funcionários: {e}")
            return jsonify([])

    @app.route('/funcionario', methods=['GET', 'POST'])
    def funcionario():
        form = FuncionarioForm()
        form.departamento_id.choices = [(d.id, d.nome) for d in Departamento.query.filter_by(ativo=True).all()]
        form.funcao_id.choices = [(f.id, f.nome) for f in Funcao.query.filter_by(ativo=True).all()]
        
        if form.validate_on_submit():
            func = Funcionario(
                nome=form.nome.data,
                cpf=form.cpf.data,
                rg=form.rg.data,
                ctps=form.ctps.data,
                pis=form.pis.data,
                serie=form.serie.data,
                secao_setor=form.secao_setor.data,
                data_admissao=form.data_admissao.data,
                departamento_id=form.departamento_id.data,
                funcao_id=form.funcao_id.data
            )
            db.session.add(func)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Funcionário cadastrado com sucesso!'})
        return render_template('modals/funcionario_modal.html', form=form)

    @app.route('/funcionario/<int:id>', methods=['PUT', 'DELETE', 'POST'])
    def funcionario_edit_delete(id):
        func = Funcionario.query.get_or_404(id)
        if request.method == 'PUT':
            data = request.get_json()
            func.nome = data.get('nome', func.nome)
            func.cpf = data.get('cpf', func.cpf)
            func.rg = data.get('rg', func.rg)
            func.ctps = data.get('ctps', func.ctps)
            func.pis = data.get('pis', func.pis)
            func.serie = data.get('serie', func.serie)
            func.secao_setor = data.get('secao_setor', func.secao_setor)
            func.departamento_id = data.get('departamento_id', func.departamento_id)
            func.funcao_id = data.get('funcao_id', func.funcao_id)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Funcionário atualizado!'})
        elif request.method == 'DELETE':
            func.ativo = False
            db.session.commit()
            return jsonify({'success': True, 'message': 'Funcionário removido!'})

    # ==================== ROTAS PARA FORNECEDORES ====================
    @app.route('/fornecedores')
    def fornecedores():
        try:
            fornecedores = Fornecedor.query.filter_by(ativo=True).all()
            result = []
            for f in fornecedores:
                result.append({
                    'id': f.id, 
                    'nome': f.nome, 
                    'cnpj': f.cnpj,
                    'created_at': f.created_at.strftime('%Y-%m-%d %H:%M:%S') if f.created_at else None
                })
            return jsonify(result)
        except Exception as e:
            print(f"Erro ao buscar fornecedores: {e}")
            return jsonify([])

    @app.route('/fornecedor', methods=['GET', 'POST'])
    def fornecedor():
        form = FornecedorForm()
        if form.validate_on_submit():
            forn = Fornecedor(cnpj=form.cnpj.data, nome=form.nome.data)
            db.session.add(forn)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Fornecedor cadastrado com sucesso!'})
        return render_template('modals/fornecedor_modal.html', form=form)

    @app.route('/fornecedor/<int:id>', methods=['PUT', 'DELETE', 'POST'])
    def fornecedor_edit_delete(id):
        forn = Fornecedor.query.get_or_404(id)
        if request.method == 'PUT':
            data = request.get_json()
            forn.nome = data.get('nome', forn.nome)
            forn.cnpj = data.get('cnpj', forn.cnpj)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Fornecedor atualizado!'})
        elif request.method == 'DELETE':
            forn.ativo = False
            db.session.commit()
            return jsonify({'success': True, 'message': 'Fornecedor removido!'})

    # ==================== ROTAS PARA EPIs ====================
    @app.route('/epis')
    def epis():
        try:
            epis = EPI.query.filter_by(ativo=True).all()
            result = []
            for e in epis:
                result.append({
                    'id': e.id, 
                    'nome': e.nome, 
                    'marca': e.marca,
                    'periodicidade_dias': e.periodicidade_dias, 
                    'ca': e.ca,
                    'created_at': e.created_at.strftime('%Y-%m-%d %H:%M:%S') if e.created_at else None
                })
            return jsonify(result)
        except Exception as e:
            print(f"Erro ao buscar EPIs: {e}")
            return jsonify([])

    @app.route('/epi', methods=['GET', 'POST'])
    def epi():
        form = EPIForm()
        form.meses.choices = [(m.id, m.nome) for m in Mes.query.all()]
        
        if form.validate_on_submit():
            epi_obj = EPI(
                nome=form.nome.data,
                marca=form.marca.data,
                periodicidade_dias=form.periodicidade_dias.data,
                ca=form.ca.data
            )
            db.session.add(epi_obj)
            db.session.flush()
            
            # Associar meses selecionados
            for mes_id in form.meses.data:
                epi_mes = EPIMes(epi_id=epi_obj.id, mes_id=mes_id)
                db.session.add(epi_mes)
            
            db.session.commit()
            return jsonify({'success': True, 'message': 'EPI cadastrado com sucesso!'})
        return render_template('modals/epi_modal.html', form=form)

    @app.route('/epi/<int:id>', methods=['PUT', 'DELETE', 'POST'])
    def epi_edit_delete(id):
        epi_obj = EPI.query.get_or_404(id)
        if request.method == 'PUT':
            data = request.get_json()
            epi_obj.nome = data.get('nome', epi_obj.nome)
            epi_obj.marca = data.get('marca', epi_obj.marca)
            epi_obj.periodicidade_dias = data.get('periodicidade_dias', epi_obj.periodicidade_dias)
            epi_obj.ca = data.get('ca', epi_obj.ca)
            db.session.commit()
            return jsonify({'success': True, 'message': 'EPI atualizado!'})
        elif request.method == 'DELETE':
            epi_obj.ativo = False
            db.session.commit()
            return jsonify({'success': True, 'message': 'EPI removido!'})

    # ==================== ROTAS PARA ENTRADA DE EPIs ====================
    @app.route('/entradas_epi')
    def entradas_epi():
        try:
            entradas = EntradaEPI.query.all()
            result = []
            for e in entradas:
                result.append({
                    'id': e.id,
                    'fornecedor': e.fornecedor.nome,
                    'data_recebimento': e.data_recebimento.strftime('%d/%m/%Y'),
                    'numero_nf': e.numero_nf,
                    'recebido_por': e.recebido_por
                })
            return jsonify(result)
        except Exception as e:
            print(f"Erro ao buscar entradas de EPI: {e}")
            return jsonify([])

    @app.route('/entrada_epi', methods=['GET', 'POST'])
    def entrada_epi():
        form = EntradaEPIForm()
        form.fornecedor_id.choices = [(f.id, f.nome) for f in Fornecedor.query.filter_by(ativo=True).all()]
        
        if form.validate_on_submit():
            entrada = EntradaEPI(
                fornecedor_id=form.fornecedor_id.data,
                data_recebimento=form.data_recebimento.data,
                numero_nf=form.numero_nf.data,
                recebido_por=form.recebido_por.data,
                observacoes=form.observacoes.data
            )
            db.session.add(entrada)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Entrada de EPI registrada!', 'entrada_id': entrada.id})
        return render_template('modals/entrada_epi_modal.html', form=form)

    # ==================== ROTAS PARA LIBERAÇÃO DE EPIs ====================
    @app.route('/liberacoes_epi')
    def liberacoes_epi():
        try:
            liberacoes = LiberacaoEPI.query.all()
            result = []
            for l in liberacoes:
                result.append({
                    'id': l.id,
                    'funcionario': l.funcionario.nome,
                    'epi': l.epi.nome,
                    'mes': l.mes.nome,
                    'data_liberacao': l.data_liberacao.strftime('%d/%m/%Y'),
                    'quantidade': l.quantidade
                })
            return jsonify(result)
        except Exception as e:
            print(f"Erro ao buscar liberações de EPI: {e}")
            return jsonify([])

    @app.route('/liberacao_epi', methods=['GET', 'POST'])
    def liberacao_epi():
        form = LiberacaoEPIForm()
        form.mes_id.choices = [(m.id, m.nome) for m in Mes.query.all()]
        form.departamento_id.choices = [(d.id, d.nome) for d in Departamento.query.filter_by(ativo=True).all()]
        form.funcao_id.choices = [(f.id, f.nome) for f in Funcao.query.filter_by(ativo=True).all()]
        form.funcionario_id.choices = []
        
        if form.validate_on_submit():
            # Processar múltiplos EPIs se selecionados
            epi_ids = request.form.getlist('epi_ids')
            for epi_id in epi_ids:
                liberacao = LiberacaoEPI(
                    funcionario_id=form.funcionario_id.data,
                    epi_id=epi_id,
                    mes_id=form.mes_id.data,
                    quantidade=1,
                    data_liberacao=datetime.now().date()
                )
                db.session.add(liberacao)
            db.session.commit()
            return jsonify({'success': True, 'message': 'EPIs liberados com sucesso!'})
        return render_template('modals/liberacao_epi_modal.html', form=form)

    # ==================== APIs AUXILIARES ====================
    @app.route('/api/funcionarios/<int:dept_id>/<int:func_id>')
    def api_funcionarios(dept_id, func_id):
        funcionarios = Funcionario.query.filter_by(
            departamento_id=dept_id, 
            funcao_id=func_id, 
            ativo=True
        ).all()
        return jsonify([{'id': f.id, 'nome': f.nome} for f in funcionarios])

    @app.route('/api/epis/<int:mes_id>/<int:dept_id>/<int:func_id>')
    def api_epis_liberacao(mes_id, dept_id, func_id):
        epis = db.session.query(EPI).join(EPIMes).join(DepartamentoFuncaoEPI).filter(
            EPIMes.mes_id == mes_id,
            DepartamentoFuncaoEPI.departamento_id == dept_id,
            DepartamentoFuncaoEPI.funcao_id == func_id,
            EPI.ativo == True
        ).all()
        return jsonify([{'id': e.id, 'nome': e.nome, 'marca': e.marca} for e in epis])

    # ==================== ROTAS PARA EDIÇÃO ====================
    @app.route('/departamento/<int:id>/edit', methods=['GET'])
    def departamento_edit_form(id):
        dept = Departamento.query.get_or_404(id)
        form = DepartamentoForm(obj=dept)
        return render_template('modals/edit_departamento_modal.html', form=form, departamento=dept)

    @app.route('/funcao/<int:id>/edit', methods=['GET'])
    def funcao_edit_form(id):
        func = Funcao.query.get_or_404(id)
        form = FuncaoForm(obj=func)
        return render_template('modals/edit_funcao_modal.html', form=form, funcao=func)

    @app.route('/funcionario/<int:id>/edit', methods=['GET'])
    def funcionario_edit_form(id):
        func = Funcionario.query.get_or_404(id)
        form = FuncionarioForm(obj=func)
        form.departamento_id.choices = [(d.id, d.nome) for d in Departamento.query.filter_by(ativo=True).all()]
        form.funcao_id.choices = [(f.id, f.nome) for f in Funcao.query.filter_by(ativo=True).all()]
        return render_template('modals/edit_funcionario_modal.html', form=form, funcionario=func)

    @app.route('/fornecedor/<int:id>/edit', methods=['GET'])
    def fornecedor_edit_form(id):
        forn = Fornecedor.query.get_or_404(id)
        form = FornecedorForm(obj=forn)
        return render_template('modals/edit_fornecedor_modal.html', form=form, fornecedor=forn)

    @app.route('/epi/<int:id>/edit', methods=['GET'])
    def epi_edit_form(id):
        epi_obj = EPI.query.get_or_404(id)
        form = EPIForm(obj=epi_obj)
        form.meses.choices = [(m.id, m.nome) for m in Mes.query.all()]
        
        # Pré-selecionar meses associados
        meses_selecionados = [em.mes_id for em in EPIMes.query.filter_by(epi_id=id).all()]
        form.meses.data = meses_selecionados
        
        return render_template('modals/edit_epi_modal.html', form=form, epi=epi_obj)