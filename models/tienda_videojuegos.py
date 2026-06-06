from odoo import models, fields, api

from odoo.exceptions import ValidationError

class Tiendavideojuegos(models.Model):
    _name='tienda.videojuegos'
    _description='Una tienda de juegos ingreso de productos'

    #Info del producto
    name=fields.Char(string='Nombre del juego',required=True)
    precio=fields.Float(string='Precio por unidad',required=True)
    stock=fields.Integer(string='Unidades compradas',required=True)
    codigo=fields.Char(string='Código del producto:',store=True,copy=False,default='nuevo')
    
    Tipo_estado=[('disponible','Disponible'),
                 ('proximo_en_stock','Proximo en Stock'),
                 ('retirado','Retirado')]
    
    estado=fields.Selection(Tipo_estado,string='Estado',required=True)

    Generos=[('novela_visual','Novela Visual'),('accion','Acción'),('indie','Empresa Independiente'),('exploracion','Exploración')
             ,('familiar','Familiar'),('cooperativo','Cooperativo'),('shooter','Shooter'),
             ('rpg_tactico','RPG tactico')]

    #Info del videojuego
    topic=fields.Selection(Generos,string='Género del videojuego:',required=True)
    sinopsis=fields.Text(string='Breve sinopsis del videojuego',required=True)

    distribuidoras_marcas= [('switch', 'Nintendo Switch'),
                            ('pc', 'PC'),
                            ('ps4', 'Playstation 4'),
                            ('ps3', 'Playstation 3')]
    distribuidoras_compatibles=fields.Selection(distribuidoras_marcas,string='Marcas compatibles',required=True)

    notas_del_administrador=fields.Text(string='Notas del administrador')

    _sql_constraints = [
    (
        'codigo_unico',
        'unique(codigo)',
        'El código del producto debe ser único.'
    )]


    @api.model
    def create(self, vals):

        if vals.get('codigo', 'nuevo') == 'nuevo':

            genero = vals.get('topic', '')

            prefijo = genero.replace('_', '')[:4].upper()

            ultimo = self.search(
                [('codigo', 'like', prefijo)],
                order='codigo desc',
                limit=1
            )

            numero = 1

            if ultimo:
                try:
                    numero = int(
                        ultimo.codigo.split('-')[1]
                    ) + 1
                except:
                    numero = 1

            vals['codigo'] = f"{prefijo}-{numero:04d}"

        return super().create(vals)
        
    @api.constrains('precio')
    def _check_precio(self):
        for record in self:
            if record.precio:
                if record.precio <= 0:
                    raise ValidationError("El precio debe ser mayor a 0")
        


    



