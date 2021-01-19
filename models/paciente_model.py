#-*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
class paciente_model(models.Model):
    _name = 'pacientes.paciente_model'
    _description = 'Modelo de Pacientes'
    _sql_constraints = [
        ("dni_dniUnico","UNIQUE (dni)","DNI ya esta en uso!!"),]
    _sql_constraints = [
        ("telefono_telefonoUnico","UNIQUE (telefono)","Telefono ya utilizado!!"),]

    dni=fields.Char(string="DNI",required=True,index=True)
    name=fields.Char(string="Nombre",required=True)
    apellidos=fields.Char(string="Apellidos",required=True)
    telefono=fields.Integer(string="Telefono",required=True)
    fechaNacimiento=fields.Date(string="FechaNac",required=True)
    email=fields.Char(string="Email",required=True)
    foto=fields.Binary(string="Foto")
    visita=fields.One2many("pacientes.visitas_model","paciente_id",string="visita")

    numVisitas=fields.Integer(string="Numero de visitas",compute="calcVisitas",store=True)

    @api.depends("visita")
    def calcVisitas(self):
        self.numVisitas=len(self.visita)




    @api.constrains("dni")
    def _validacionDNI(self):
        
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        letra = self.dni[-1]
        num = self.dni[:-1]
        posi = int(num) % 23
        
        if letra != letras[posi]:
            raise ValidationError("DNI no valido")
    
	