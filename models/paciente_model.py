#-*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

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
    fotoEjercicios=fields.Binary(string="Ejercicios")
    visita=fields.One2many("pacientes.visitas_model","paciente_id",string="visita")


    numVisitas=fields.Integer(string="Numero de visitas",compute="calcVisitas",store=True)

    @api.depends("visita")
    def calcVisitas(self):
        self.numVisitas=len(self.visita)

    def limpiaHistorial(self):
        for i in self.visita:
            i.unlink()
    

    @api.constrains("fechaNacimiento")
    def _mayorEdad(self):
        hoy = datetime.today()
        fechanacimiento=self.fechaNacimiento
        edad = hoy.year - fechanacimiento.year - ((hoy.month, hoy.day) < (fechanacimiento.month, fechanacimiento.day))
        if edad<18:
            raise ValidationError("No puede ser menor de edad")

    @api.constrains("email")
    def es_correo_valido(self):
        expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        comprueba= re.match(expresion_regular, self.email) is not None
        if comprueba==False:
            raise ValidationError("Formato de correo no valido")

        

    @api.constrains("dni")
    def _validacionDNI(self):
        
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        letra = self.dni[-1]
        num = self.dni[:-1]
        posi = int(num) % 23
        
        if letra != letras[posi]:
            raise ValidationError("DNI no valido")
    
	