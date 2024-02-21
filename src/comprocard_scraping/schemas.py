import marshmallow as mm


class ResultSchema(mm.Schema):
    nome = mm.fields.String(load_default=None)
    endereco = mm.fields.String(load_default=None)
    cidade = mm.fields.String(load_default=None)
    uf = mm.fields.String(load_default=None)
    bairro = mm.fields.String(load_default=None)
    atividade = mm.fields.String(load_default=None)
    telefone = mm.fields.String(load_default=None)
    latitude = mm.fields.String(load_default=None)
    longitude = mm.fields.String(load_default=None)
