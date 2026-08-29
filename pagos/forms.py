from django import forms
from .models import Pago
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

class PagoForm(forms.ModelForm):
    # Select banco with common options
    BANCOS_OPCIONES = [
        ('', '— Selecciona el banco o medio de pago —'),
        ('Nequi', 'Nequi'),
        ('Daviplata', 'Daviplata'),
        ('Bancolombia', 'Bancolombia'),
        ('Banco de Bogotá', 'Banco de Bogotá'),
        ('Davivienda', 'Davivienda'),
        ('BBVA', 'BBVA'),
        ('Banco de Occidente', 'Banco de Occidente'),
        ('Lulo Bank', 'Lulo Bank'),
        ('RappiPay', 'RappiPay'),
        ('Otro', 'Otro (Especificar en descripción)'),
    ]

    banco_origen = forms.ChoiceField(
        choices=BANCOS_OPCIONES,
        required=True,
        label='Banco o Medio de Pago'
    )

    fecha_pago = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Fecha y Hora Exacta del Pago',
        required=True
    )

    class Meta:
        model = Pago
        fields = ['reserva', 'referencia', 'banco_origen', 'monto', 'fecha_pago', 'imagen_comprobante', 'descripcion']
        labels = {
            'reserva': 'Reserva o Penalidad a Vincular',
            'referencia': 'Nº de Referencia / Transacción',
            'monto': 'Monto Exacto Pagado',
            'imagen_comprobante': 'Imagen o Captura del Comprobante',
            'descripcion': 'Notas o Detalles Adicionales',
        }
        help_texts = {
            'imagen_comprobante': 'Sube un archivo legible (PNG, JPG, JPEG, WebP).',
            'descripcion': 'Si seleccionaste "Otro" en banco, especifícalo aquí.',
        }
        widgets = {
            'monto': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        # We need to receive the user's reservations to populate the 'reserva' field
        reservas = kwargs.pop('reservas', None)
        super().__init__(*args, **kwargs)

        if reservas is not None:
            # Format the options cleanly
            self.fields['reserva'].queryset = reservas
            # Customizing the label from the queryset
            self.fields['reserva'].label_from_instance = lambda obj: (
                f"[Multa] {obj.paquete.nombre} — Valor: COP ${obj.multa:,.0f}" if getattr(obj, 'multa', None)
                else f"[Reserva] {obj.paquete.nombre} — Valor: COP ${obj.monto_total:,.0f} (Fecha: {obj.fecha})"
            )

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'formComprobante'
        self.helper.layout = Layout(
            Row(
                Column('reserva', css_class='form-group col-md-12 mb-3'),
                css_class='row'
            ),
            Row(
                Column('referencia', css_class='form-group col-md-6 mb-3'),
                Column('banco_origen', css_class='form-group col-md-6 mb-3'),
                css_class='row'
            ),
            Row(
                Column('monto', css_class='form-group col-md-4 mb-3'),
                Column('fecha_pago', css_class='form-group col-md-4 mb-3'),
                Column('imagen_comprobante', css_class='form-group col-md-4 mb-3'),
                css_class='row'
            ),
            Row(
                Column('descripcion', css_class='form-group col-md-12 mb-3'),
                css_class='row'
            ),
            HTML('<hr>'),
            Row(
                Column(
                    Submit('submit', 'Enviar Reporte', css_class='btn btn-success w-100 rounded-pill py-3 fw-bold shadow-sm'),
                    css_class='col-md-5 ms-auto mt-3'
                )
            )
        )

class RevisarComprobanteForm(forms.ModelForm):
    """
    Formulario para que el Administrador/Tesorero revise y tome decisiones sobre un pago.
    """
    class Meta:
        model = Pago
        fields = ['banco_origen', 'monto', 'estado_transaccion', 'nota_admin']
        labels = {
            'banco_origen': 'Banco / Medio de Pago',
            'monto': 'Monto Verificado (COP)',
            'estado_transaccion': 'Estado del Pago',
            'nota_admin': 'Nota del Administrador',
        }
        widgets = {
            'banco_origen': forms.TextInput(attrs={'class': 'form-control rounded-4 shadow-sm', 'placeholder': 'Banco o Medio de Pago'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control rounded-4 shadow-sm', 'placeholder': 'Monto Verificado', 'step': '0.01', 'min': '0'}),
            'estado_transaccion': forms.Select(attrs={'class': 'form-select rounded-4 shadow-sm'}),
            'nota_admin': forms.Textarea(attrs={'class': 'form-control rounded-4 shadow-sm', 'rows': 3, 'placeholder': 'Motivo de rechazo o nota aclaratoria...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos que estos campos no sean estrictamente requeridos a nivel de HTML
        # para que la lógica de validación interna (Pago.clean) sea la que decida según el estado.
        self.fields['banco_origen'].required = False
        self.fields['monto'].required = False
        self.fields['nota_admin'].required = False
