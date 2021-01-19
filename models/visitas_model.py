#-*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
class visitas_model(models.Model):
    _name = 'pacientes.visitas_model'
    _description = 'Modelo de Visitas'

    fecha=fields.Date(string="Fecha",required=True,default=datetime.today())
    detalle=fields.Html(string="Detalle",required=True)
    paciente_id=fields.Many2one("pacientes.paciente_model","paciente")
    