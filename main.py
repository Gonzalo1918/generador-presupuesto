# import flet as ft
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# import datetime
# import os
# import webbrowser

# # ---------------------------------------------------------
# # FUNCIÓN PARA GENERAR Y GUARDAR EL PDF
# # ---------------------------------------------------------
# def generar_pdf(empresa, tipo_id, numero_id, direccion, fecha_emision, fecha_validez,
#                 cliente, descripcion, items, subtotal, iva, total):
#     archivo = os.path.join(os.getcwd(), "presupuesto.pdf")
#     c = canvas.Canvas(archivo, pagesize=A4)
#     width, height = A4

#     # Encabezado empresa
#     c.setFont("Helvetica-Bold", 14)
#     c.drawString(30, height - 50, empresa)
#     c.setFont("Helvetica", 10)
#     c.drawString(30, height - 65, f"{tipo_id}: {numero_id}")
#     c.drawString(30, height - 80, f"Dirección: {direccion}")

#     # Título y fechas
#     c.setFont("Helvetica-Bold", 16)
#     c.drawCentredString(width / 2, height - 110, "PRESUPUESTO")
#     c.setFont("Helvetica", 10)
#     c.drawString(30, height - 130, f"Fecha de emisión: {fecha_emision}")
#     c.drawString(30, height - 145, f"Válido hasta: {fecha_validez}")

#     # Cliente
#     c.setFont("Helvetica-Bold", 12)
#     c.drawString(30, height - 180, "CLIENTE")
#     c.setFont("Helvetica", 10)
#     c.drawString(30, height - 195, cliente)
#     c.drawString(30, height - 210, descripcion)

#     # Tabla de ítems
#     y = height - 250
#     c.setFont("Helvetica-Bold", 10)
#     c.drawString(30, y, "DESCRIPCIÓN")
#     c.drawString(250, y, "CANTIDAD")
#     c.drawString(330, y, "PRECIO UNIT.")
#     c.drawString(450, y, "SUBTOTAL")

#     y -= 20
#     c.setFont("Helvetica", 10)
#     for item in items:
#         c.drawString(30, y, str(item["descripcion"]))
#         c.drawString(260, y, str(item["cantidad"]))
#         c.drawString(340, y, f"$ {item['precio']:,.2f}")
#         c.drawString(460, y, f"$ {item['subtotal']:,.2f}")
#         y -= 20

#     # Totales
#     y -= 20
#     c.setFont("Helvetica-Bold", 10)
#     c.drawString(350, y, f"Subtotal: $ {subtotal:,.2f}")
#     y -= 15
#     c.drawString(350, y, f"IVA (0%): $ {iva:,.2f}")
#     y -= 15
#     c.setFont("Helvetica-Bold", 12)
#     c.drawString(350, y, f"TOTAL: $ {total:,.2f}")

#     c.showPage()
#     c.save()
#     return archivo

# # ---------------------------------------------------------
# # APLICACIÓN FLET
# # ---------------------------------------------------------
# def main(page: ft.Page):
#     page.title = "Generador de Presupuestos"
#     page.scroll = "adaptive"

#     # -------- Encabezado de empresa editable --------
#     empresa = ft.TextField(label="Nombre de la empresa", value="Ayrton Neumáticos")

#     tipo_id = ft.Dropdown(
#         label="Tipo de identificación",
#         options=[ft.dropdown.Option("CUIT"), ft.dropdown.Option("DNI")],
#         value="CUIT",
#         width=150
#     )

#     numero_id = ft.TextField(label="Número", value="20-42888111-0", width=200)
#     direccion = ft.TextField(label="Dirección", value="Córdoba", width=300)

#     fecha_emision = ft.TextField(
#         label="Fecha de emisión",
#         value=datetime.date.today().strftime("%d/%m/%Y"),
#         width=150
#     )

#     fecha_validez = ft.TextField(
#         label="Válido hasta",
#         value=(datetime.date.today() + datetime.timedelta(days=30)).strftime("%d/%m/%Y"),
#         width=150
#     )

#     # -------- Datos del cliente --------
#     cliente = ft.TextField(label="Cliente", width=300)
#     descripcion = ft.TextField(label="Descripción general", width=400)

#     # -------- Ítems --------
#     desc_item = ft.TextField(label="Descripción del ítem", width=250)
#     cant = ft.TextField(label="Cantidad", width=100)
#     precio = ft.TextField(label="Precio Unitario", width=150)
#     items = []
#     tabla = ft.Column()

#     # -------- Funciones --------
#     def agregar_item(e):
#         try:
#             cantidad = int(cant.value)
#             precio_unit = float(precio.value)
#             subtotal_item = cantidad * precio_unit
#             item = {
#                 "descripcion": desc_item.value,
#                 "cantidad": cantidad,
#                 "precio": precio_unit,
#                 "subtotal": subtotal_item
#             }
#             items.append(item)

#             tabla.controls.append(
#                 ft.Row([
#                     ft.Text(item["descripcion"], width=200),
#                     ft.Text(str(item["cantidad"]), width=100),
#                     ft.Text(f"$ {item['precio']:,.2f}", width=120),
#                     ft.Text(f"$ {item['subtotal']:,.2f}", width=120)
#                 ])
#             )
#             desc_item.value = ""
#             cant.value = ""
#             precio.value = ""
#             page.update()
#         except:
#             page.snack_bar = ft.SnackBar(ft.Text("⚠️ Ingresá valores numéricos válidos en cantidad y precio."))
#             page.snack_bar.open = True
#             page.update()

#     def exportar_pdf(e):
#         if not cliente.value or len(items) == 0:
#             page.snack_bar = ft.SnackBar(ft.Text("⚠️ Faltan datos del cliente o ítems."))
#             page.snack_bar.open = True
#             page.update()
#             return

#         subtotal = sum(i["subtotal"] for i in items)
#         iva = 0
#         total = subtotal + iva

#         archivo = generar_pdf(
#             empresa.value,
#             tipo_id.value,
#             numero_id.value,
#             direccion.value,
#             fecha_emision.value,
#             fecha_validez.value,
#             cliente.value,
#             descripcion.value,
#             items,
#             subtotal,
#             iva,
#             total
#         )

#         # Abrir PDF generado
#         webbrowser.open(f"file://{archivo}")
#         page.snack_bar = ft.SnackBar(ft.Text(f"✅ PDF generado correctamente: {archivo}"))
#         page.snack_bar.open = True
#         page.update()

#     # -------- Layout visual --------
#     page.add(
#         ft.Text("Generador de Presupuestos", size=24, weight="bold"),
#         ft.Divider(),
#         ft.Text("Datos de la empresa", size=16, weight="bold"),
#         empresa,
#         ft.Row([tipo_id, numero_id, direccion]),
#         ft.Row([fecha_emision, fecha_validez]),
#         ft.Divider(),
#         ft.Text("Datos del cliente", size=16, weight="bold"),
#         cliente,
#         descripcion,
#         ft.Divider(),
#         ft.Text("Ítems", size=16, weight="bold"),
#         ft.Row([desc_item, cant, precio, ft.ElevatedButton("Agregar", on_click=agregar_item)]),
#         ft.Text("Lista de ítems agregados:", size=14, weight="bold"),
#         tabla,
#         ft.Divider(),
#         ft.ElevatedButton("Generar y abrir PDF", on_click=exportar_pdf, bgcolor="blue", color="white")
#     )

# # Ejecutar la app
# ft.app(target=main)

# generador_presupuesto_ok.py

# generador_presupuesto_profesional.py

# import flet as ft
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from PIL import Image
# import datetime, os, webbrowser


# # ----------------- Helpers -----------------
# def parse_float_tol(s):
#     if not s:
#         raise ValueError("Valor vacío")
#     s = str(s).strip().replace("$", "").replace("ARS", "").replace("USD", "").replace(" ", "")
#     if s.count(".") > 0 and s.count(",") > 0:
#         s = s.replace(".", "").replace(",", ".")
#     elif "," in s and "." not in s:
#         s = s.replace(",", ".")
#     return float(s)


# def parse_int_tol(s):
#     return int(round(parse_float_tol(s)))


# # ----------------- PDF -----------------
# def generar_pdf(empresa, logo_path, fecha_emision, fecha_validez,
#                 cliente, tipo_id, numero_id, direccion, descripcion,
#                 items, subtotal, descuento, tipo_descuento, iva, total):
#     archivo = os.path.join(os.getcwd(), f"Presupuesto_{cliente.replace(' ', '_')}_{datetime.date.today()}.pdf")
#     c = canvas.Canvas(archivo, pagesize=A4)
#     width, height = A4

#     # Logo
#     if logo_path and os.path.exists(logo_path):
#         img = Image.open(logo_path)
#         img.thumbnail((100, 100))
#         tmp = "temp_logo.png"
#         img.save(tmp)
#         c.drawImage(tmp, width - 130, height - 130, width=100, preserveAspectRatio=True, mask="auto")
#         try:
#             os.remove(tmp)
#         except:
#             pass

#     # Encabezado
#     c.setFont("Helvetica-Bold", 16)
#     c.drawString(30, height - 50, empresa)
#     c.setFont("Helvetica-Bold", 18)
#     c.drawCentredString(width / 2, height - 100, "PRESUPUESTO")

#     # Fechas
#     c.setFont("Helvetica", 10)
#     c.drawString(30, height - 120, f"Fecha de emisión: {fecha_emision}")
#     c.drawString(30, height - 135, f"Válido hasta: {fecha_validez}")

#     # Cliente
#     c.setFont("Helvetica-Bold", 12)
#     c.drawString(30, height - 165, "CLIENTE")
#     c.setFont("Helvetica", 10)
#     c.drawString(30, height - 180, cliente)
#     c.drawString(30, height - 195, f"{tipo_id}: {numero_id}")
#     c.drawString(30, height - 210, f"Dirección: {direccion}")

#     if descripcion.strip():
#         c.setFont("Helvetica-Oblique", 10)
#         c.drawString(30, height - 230, descripcion)

#     # Tabla
#     y = height - 260
#     c.setFont("Helvetica-Bold", 10)
#     c.drawString(30, y, "DESCRIPCIÓN")
#     c.drawString(260, y, "CANT.")
#     c.drawString(330, y, "PRECIO UNIT.")
#     c.drawString(450, y, "SUBTOTAL")
#     y -= 15

#     c.setFont("Helvetica", 10)
#     for it in items:
#         if y < 100:
#             c.showPage()
#             c.setFont("Helvetica-Bold", 10)
#             c.drawString(30, height - 50, "DESCRIPCIÓN")
#             c.drawString(260, height - 50, "CANT.")
#             c.drawString(330, height - 50, "PRECIO UNIT.")
#             c.drawString(450, height - 50, "SUBTOTAL")
#             y = height - 70
#             c.setFont("Helvetica", 10)

#         c.drawString(30, y, it["descripcion"])
#         c.drawString(260, y, str(it["cantidad"]))
#         c.drawRightString(420, y, f"$ {it['precio']:,.2f}")
#         c.drawRightString(520, y, f"$ {it['subtotal']:,.2f}")
#         y -= 15

#     # Totales
#     y -= 20
#     c.setFont("Helvetica-Bold", 10)
#     c.drawRightString(520, y, f"Subtotal: $ {subtotal:,.2f}")
#     y -= 14

#     if tipo_descuento == "%":
#         c.drawRightString(520, y, f"Descuento ({descuento}%): -$ {subtotal * descuento / 100:,.2f}")
#     else:
#         c.drawRightString(520, y, f"Descuento: -$ {descuento:,.2f}")

#     y -= 14
#     iva_monto = (subtotal - (subtotal * descuento / 100 if tipo_descuento == "%" else descuento)) * iva / 100
#     c.drawRightString(520, y, f"IVA ({iva}%): $ {iva_monto:,.2f}")

#     y -= 16
#     c.setFont("Helvetica-Bold", 12)
#     c.drawRightString(520, y, f"TOTAL: $ {total:,.2f}")

#     c.save()
#     return archivo


# # ----------------- APP -----------------
# def main(page: ft.Page):
#     page.title = "Generador de Presupuestos"
#     page.theme_mode = "light"
#     page.scroll = "adaptive"
#     page.padding = 20
#     page.bgcolor = "#f9f9f9"

#     items, logo_path = [], None

#     primary_color = "#FF0000"
#     text_color = "#000000"

#     def estilo_titulo(txt):
#         return ft.Text(txt, size=22, weight="bold", color=text_color)

#     def estilo_subtitulo(txt):
#         return ft.Text(txt, size=16, weight="bold", color=primary_color)

#     # ----------------- Tema -----------------
#     def toggle_tema(e):
#         if page.theme_mode == "light":
#             page.theme_mode = "dark"
#             theme_btn.icon = ft.Icons.DARK_MODE
#         else:
#             page.theme_mode = "light"
#             theme_btn.icon = ft.Icons.LIGHT_MODE
#         page.update()

#     theme_btn = ft.IconButton(icon=ft.Icons.LIGHT_MODE, tooltip="Cambiar tema", on_click=toggle_tema)

#     # ----------------- Datos Generales -----------------
#     empresa = ft.TextField(label="Empresa", value="Ayrton Neumáticos", width=350)
#     cliente = ft.TextField(label="Cliente", width=350)
#     tipo_id = ft.Dropdown(
#         label="Tipo ID",
#         options=[ft.dropdown.Option(x) for x in ["CUIT", "DNI", "CUIL"]],
#         value="CUIT", width=120
#     )
#     numero_id = ft.TextField(label="Número", width=200)
#     direccion = ft.TextField(label="Dirección / Ubicación", width=400)
#     descripcion = ft.TextField(label="Descripción / Nota", multiline=True, width=400)
#     fecha_emision = ft.TextField(label="Fecha de emisión", value=datetime.date.today().strftime("%d/%m/%Y"), width=160)
#     fecha_validez = ft.TextField(label="Válido hasta", value=(datetime.date.today() + datetime.timedelta(days=30)).strftime("%d/%m/%Y"), width=160)
#     iva_input = ft.TextField(label="IVA %", value="0", width=100)

#     # ----------------- Descuento -----------------
#     tipo_descuento = ft.Dropdown(
#         label="Tipo de descuento",
#         options=[ft.dropdown.Option("%"), ft.dropdown.Option("Monto")],
#         value="%",
#         width=120
#     )
#     descuento_input = ft.TextField(label="Descuento", value="0", width=100)

#     # ----------------- Logo -----------------
#     logo_preview = ft.Image(width=100, height=100, fit=ft.ImageFit.CONTAIN)

#     def on_logo_pick(e: ft.FilePickerResultEvent):
#         nonlocal logo_path
#         if e.files:
#             logo_path = e.files[0].path
#             logo_preview.src = f"file://{logo_path}"
#             page.update()

#     fp = ft.FilePicker(on_result=on_logo_pick)
#     page.overlay.append(fp)
#     btn_logo = ft.ElevatedButton(
#         "Subir logo", color="white", bgcolor=primary_color,
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#         on_click=lambda _: fp.pick_files(allow_multiple=False)
#     )

#     # ----------------- Tabla Items -----------------
#     tabla = ft.Column(scroll="auto", expand=True)

#     def render_tabla():
#         tabla.controls = []
#         for idx, it in enumerate(items):
#             fila = ft.Container(
#                 ft.Row([
#                     ft.Text(it["descripcion"], width=250),
#                     ft.Text(str(it["cantidad"]), width=80),
#                     ft.Text(f"$ {it['precio']:,.2f}", width=120),
#                     ft.Text(f"$ {it['subtotal']:,.2f}", width=120),
#                     ft.IconButton(icon=ft.Icons.EDIT, icon_color=primary_color, tooltip="Editar", on_click=lambda e, i=idx: editar_item(i)),
#                     ft.IconButton(icon=ft.Icons.DELETE, icon_color="#444444", tooltip="Eliminar", on_click=lambda e, i=idx: eliminar_item(i)),
#                 ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
#                 bgcolor="#ffffff", padding=10, border_radius=8,
#                 shadow=ft.BoxShadow(blur_radius=4, spread_radius=1, color="#dddddd")
#             )
#             tabla.controls.append(fila)
#         page.update()

#     desc_item = ft.TextField(label="Descripción", width=250)
#     cant_item = ft.TextField(label="Cantidad", width=80)
#     precio_item = ft.TextField(label="Precio Unitario", width=100)

#     def agregar_item(e):
#         try:
#             desc = desc_item.value.strip()
#             if not desc:
#                 raise ValueError("Descripción vacía.")
#             cantidad = parse_int_tol(cant_item.value)
#             precio = parse_float_tol(precio_item.value)
#             items.append({"descripcion": desc, "cantidad": cantidad, "precio": precio, "subtotal": cantidad * precio})
#             desc_item.value = cant_item.value = precio_item.value = ""
#             render_tabla()
#         except Exception as ex:
#             page.snack_bar = ft.SnackBar(ft.Text(f"⚠️ {ex}"))
#             page.snack_bar.open = True
#             page.update()

#     def eliminar_item(i):
#         items.pop(i)
#         render_tabla()

#     def editar_item(i):
#         it = items.pop(i)
#         desc_item.value, cant_item.value, precio_item.value = it["descripcion"], str(it["cantidad"]), str(it["precio"])
#         render_tabla()

#     # ----------------- Generar PDF -----------------
#     def generar_pdf_click(e):
#         if not cliente.value.strip():
#             page.snack_bar = ft.SnackBar(ft.Text("⚠️ Ingresá el nombre del cliente."))
#             page.snack_bar.open = True
#             return
#         if not items:
#             page.snack_bar = ft.SnackBar(ft.Text("⚠️ Agregá al menos un ítem."))
#             page.snack_bar.open = True
#             return

#         subtotal = sum(it["subtotal"] for it in items)
#         try:
#             iva = parse_float_tol(iva_input.value)
#         except:
#             iva = 0.0
#         try:
#             descuento = parse_float_tol(descuento_input.value)
#         except:
#             descuento = 0.0

#         # Cálculo del total
#         if tipo_descuento.value == "%":
#             subtotal_desc = subtotal - (subtotal * descuento / 100)
#         else:
#             subtotal_desc = subtotal - descuento

#         total = subtotal_desc + subtotal_desc * iva / 100

#         archivo = generar_pdf(
#             empresa.value, logo_path, fecha_emision.value, fecha_validez.value,
#             cliente.value, tipo_id.value, numero_id.value, direccion.value,
#             descripcion.value, items, subtotal, descuento, tipo_descuento.value, iva, total
#         )

#         webbrowser.open(f"file://{archivo}")
#         page.snack_bar = ft.SnackBar(ft.Text(f"✅ PDF generado correctamente."))
#         page.snack_bar.open = True
#         page.update()

#     # ----------------- Layout principal -----------------
#     contenido = ft.ResponsiveRow(
#         [
#             ft.Container(
#                 ft.Column([
#                     estilo_titulo("Generador de Presupuestos"),
#                     ft.Row([ft.Container(expand=True), theme_btn]),
#                     ft.Divider(),
#                     estilo_subtitulo("Datos de la empresa"),
#                     empresa,
#                     ft.Row([btn_logo, logo_preview]),
#                     ft.Divider(),
#                     estilo_subtitulo("Datos del cliente"),
#                     cliente,
#                     ft.Row([tipo_id, numero_id]),
#                     direccion,
#                     descripcion,
#                     ft.Row([fecha_emision, fecha_validez, iva_input]),
#                     ft.Row([tipo_descuento, descuento_input]),
#                     ft.Divider(),
#                     estilo_subtitulo("Ítems del presupuesto"),
#                     ft.ResponsiveRow([
#                         desc_item, cant_item, precio_item,
#                         ft.ElevatedButton("Agregar", bgcolor=primary_color, color="white", on_click=agregar_item)
#                     ]),
#                     tabla,
#                     ft.Divider(),
#                     ft.ElevatedButton(
#                         "Generar y abrir PDF",
#                         on_click=generar_pdf_click,
#                         bgcolor=primary_color,
#                         color="white",
#                         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
#                     )
#                 ]),
#                 col={"xs": 12, "sm": 12, "md": 10, "lg": 8},
#                 padding=20,
#                 bgcolor="#ffffff",
#                 border_radius=10,
#                 shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color="#cccccc")
#             )
#         ],
#         alignment=ft.MainAxisAlignment.CENTER,
#         run_spacing=10,
#         spacing=10,
#     )

#     page.add(contenido)


# if __name__ == "__main__":
#     ft.app(target=main)

# archivo: presupuesto_app.py


# import flet as ft
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from PIL import Image
# import datetime, os, webbrowser, tempfile


# # ----------------- Helpers -----------------
# def parse_float_tol(s):
#     if s is None or str(s).strip() == "":
#         raise ValueError("Valor vacío")
#     s = str(s).strip().replace("$", "").replace("ARS", "").replace("USD", "").replace(" ", "")
#     if s.count(".") > 0 and s.count(",") > 0:
#         s = s.replace(".", "").replace(",", ".")
#     elif "," in s and "." not in s:
#         s = s.replace(",", ".")
#     return float(s)


# def parse_int_tol(s):
#     if s is None or str(s).strip() == "":
#         raise ValueError("Valor vacío")
#     return int(round(parse_float_tol(s)))


# def format_currency_ar(value):
#     try:
#         v = float(value)
#     except:
#         v = 0.0
#     entero = int(abs(v))
#     dec = abs(v) - entero
#     entero_str = f"{entero:,}".replace(",", ".")
#     dec_str = f"{dec:.2f}"[1:].replace(".", ",")
#     sign = "-" if v < 0 else ""
#     return f"{sign}$ {entero_str}{dec_str}"


# def format_currency_usd(value):
#     try:
#         v = float(value)
#     except:
#         v = 0.0
#     entero = int(abs(v))
#     dec = abs(v) - entero
#     entero_str = f"{entero:,}".replace(",", ".")
#     dec_str = f"{dec:.2f}"[1:].replace(".", ",")
#     sign = "-" if v < 0 else ""
#     return f"{sign}U$D {entero_str}{dec_str}"


# # ----------------- Número correlativo -----------------
# LAST_FILE = "last_presupuesto.txt"


# def obtener_proximo_numero():
#     try:
#         if not os.path.exists(LAST_FILE):
#             with open(LAST_FILE, "w") as f:
#                 f.write("1")
#                 return 1
#         with open(LAST_FILE, "r+") as f:
#             n = int(f.read().strip() or 0) + 1
#             f.seek(0)
#             f.truncate()
#             f.write(str(n))
#             return n
#     except:
#         return int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))


# def numero_a_formato(n):
#     return str(n).zfill(4)


# # ----------------- PDF Helpers -----------------
# def draw_wrapped_text(c, text, x, y, max_width, line_height, font_name="Helvetica", font_size=10):
#     words = text.split()
#     lines, current = [], ""
#     for w in words:
#         test = current + (" " if current else "") + w
#         if c.stringWidth(test, font_name, font_size) <= max_width:
#             current = test
#         else:
#             lines.append(current)
#             current = w
#     if current:
#         lines.append(current)
#     for i, line in enumerate(lines):
#         c.drawString(x, y - i * line_height, line)
#     return len(lines)


# # ----------------- PDF -----------------
# def generar_pdf(empresa, cuit, direccion, correo, logo_path,
#                 nro_presupuesto, fecha_emision, fecha_validez,
#                 cliente, tipo_id, numero_id, descripcion,
#                 items, subtotal, descuento_total, iva, total,
#                 mostrar_logo, mostrar_cuit, mostrar_dir, mostrar_correo,
#                 moneda="ARS", cotizacion_dolar=0.0):

#     nombre_archivo = f"Presupuesto_{numero_a_formato(nro_presupuesto)}_{cliente.replace(' ', '_')}.pdf"
#     archivo = os.path.join(os.getcwd(), nombre_archivo)
#     c = canvas.Canvas(archivo, pagesize=A4)
#     width, height = A4
#     left_x = 40
#     right_x_total = 520

#     # Logo
#     if mostrar_logo and logo_path and os.path.exists(logo_path):
#         try:
#             img = Image.open(logo_path)
#             img.thumbnail((120, 120))
#             tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
#             img.save(tmp.name)
#             c.drawImage(tmp.name, width - 150, height - 110, width=110, preserveAspectRatio=True, mask="auto")
#             os.remove(tmp.name)
#         except:
#             pass

#     # Encabezado
#     c.setFont("Helvetica-Bold", 16)
#     c.drawString(left_x, height - 50, empresa.upper())
#     c.line(40, height - 60, width - 40, height - 60)

#     c.setFont("Helvetica", 10)
#     y = height - 80
#     if mostrar_cuit and cuit:
#         c.drawString(left_x, y, f"CUIT/CUIL: {cuit}")
#         y -= 14
#     if mostrar_dir and direccion:
#         c.drawString(left_x, y, f"Dirección: {direccion}")
#         y -= 14
#     if mostrar_correo and correo:
#         c.drawString(left_x, y, f"Correo electrónico: {correo}")
#         y -= 18

#     # Moneda info
#     c.setFont("Helvetica-Oblique", 9)
#     if moneda == "USD":
#         c.drawString(left_x, y, f"Moneda: Dólar Estadounidense (USD) - Cotización: {format_currency_ar(cotizacion_dolar)} USD")
#     else:
#         c.drawString(left_x, y, f"Moneda: Peso Argentino (ARS)")
#     y -= 25

#     # Título
#     c.setFont("Helvetica-Bold", 18)
#     c.drawCentredString(width / 2, y, f"PRESUPUESTO N° {numero_a_formato(nro_presupuesto)}")
#     y -= 45

#     # Fechas
#     c.setFont("Helvetica", 10)
#     c.drawString(left_x, y, f"Fecha de emisión: {fecha_emision}")
#     c.drawString(left_x, y - 15, f"Válido hasta: {fecha_validez}")
#     y -= 40

#     # Cliente
#     c.setFont("Helvetica-Bold", 12)
#     c.drawString(left_x, y, "CLIENTE")
#     y -= 15
#     c.setFont("Helvetica", 10)
#     c.drawString(left_x, y, cliente)
#     y -= 15
#     c.drawString(left_x, y, f"{tipo_id}: {numero_id}")
#     y -= 30

#     # Descripción general
#     if descripcion.strip():
#         c.setFont("Helvetica-Oblique", 9)
#         c.drawString(left_x, y, descripcion.strip())
#         y -= 25

#     # Tabla encabezados
#     c.setFont("Helvetica-Bold", 10)
#     c.drawString(40, y, "#  DESCRIPCIÓN")
#     c.drawString(300, y, "CANT.")
#     c.drawString(340, y, "P.UNIT. (ARS)")
#     c.drawString(430, y, "TOTAL (ARS)")
#     y -= 18
#     c.setFont("Helvetica", 10)

#     contador = 1
#     for it in items:
#         if y < 110:
#             c.showPage()
#             y = height - 70
#             c.setFont("Helvetica-Bold", 10)
#             c.drawString(40, y, "#  DESCRIPCIÓN")
#             c.drawString(300, y, "CANT.")
#             c.drawString(340, y, "P.UNIT. (ARS)")
#             c.drawString(430, y, "TOTAL (ARS)")
#             y -= 18
#             c.setFont("Helvetica", 10)

#         lines_used = draw_wrapped_text(c, it["descripcion"], 60, y, 220, 12)
#         row_height = max(12, lines_used * 12)
#         c.drawString(40, y, f"{contador}")
#         c.drawString(300, y, str(it["cantidad"]))
#         c.drawRightString(410, y, format_currency_ar(it["precio"]))
#         c.drawRightString(510, y, format_currency_ar(it["subtotal"]))
#         y -= row_height + 6
#         contador += 1

#     # Totales
#     y -= 25
#     if moneda == "ARS":
#         # Mostrar totales solo en pesos
#         c.setFont("Helvetica-Bold", 10)
#         c.drawRightString(right_x_total, y, f"Subtotal: {format_currency_ar(subtotal)}")
#         y -= 16
#         if descuento_total:
#             c.drawRightString(right_x_total, y, f"Descuentos aplicados: -{format_currency_ar(descuento_total)}")
#             y -= 16
#         if iva:
#             iva_calc = total - (subtotal - descuento_total)
#             c.drawRightString(right_x_total, y, f"IVA ({iva}%): {format_currency_ar(iva_calc)}")
#             y -= 18

#         c.setFont("Helvetica-Bold", 12)
#         c.drawRightString(right_x_total, y, f"TOTAL: {format_currency_ar(total)}")
#         y -= 22

#     elif moneda == "USD":
#         # Mostrar resumen en pesos + conversión a USD
#         c.setFont("Helvetica-Bold", 10)
#         c.drawRightString(right_x_total, y, f"Monto original (ARS): {format_currency_ar(subtotal)}")
#         y -= 16
#         if descuento_total:
#             c.drawRightString(right_x_total, y, f"Descuento aplicado (ARS): -{format_currency_ar(descuento_total)}")
#             y -= 16
#         c.drawRightString(right_x_total, y, f"Cotización dólar: {format_currency_ar(cotizacion_dolar)} ARS")
#         y -= 18

#         total_usd = total / cotizacion_dolar if cotizacion_dolar else 0
#         c.setFont("Helvetica-Bold", 12)
#         c.drawRightString(right_x_total, y, f"TOTAL (USD): {format_currency_usd(total_usd)}")
#         y -= 22

#     c.save()
#     return archivo

# # ----------------- APP -----------------
# def main(page: ft.Page):
#     page.title = "Generador de Presupuestos"
#     page.theme_mode = "light"
#     page.scroll = "adaptive"
#     page.padding = 20

#     items = []
#     edit_index = None
#     logo_path = None
#     primary = "#A81A1A"
#     dark_bg = "#000000"

#     def style_field(field):
#         field.border_color = primary if page.theme_mode == "dark" else None
#         return field

#     # --- Campos principales ---
#     empresa = style_field(ft.TextField(label="Empresa", value="Ayrton Neumáticos", width=420))
#     cuit = style_field(ft.TextField(label="CUIT", value="20-42693588-1", width=240))
#     direccion = style_field(ft.TextField(label="Dirección", value="Av. Ejemplo 123, Córdoba", width=420))
#     correo = style_field(ft.TextField(label="Correo electrónico", value="ventas@ayrtonneumaticos.com", width=420))
#     cliente = style_field(ft.TextField(label="Cliente", width=360))
#     tipo_id = style_field(ft.Dropdown(label="Tipo ID", options=[ft.dropdown.Option(x) for x in ["CUIT", "DNI", "CUIL"]], value="CUIT", width=120))
#     numero_id = style_field(ft.TextField(label="Número", width=220))
#     descripcion = style_field(ft.TextField(label="Descripción / Nota", multiline=True, width=420))
#     fecha_emision = style_field(ft.TextField(label="Fecha de emisión", value=datetime.date.today().strftime("%d/%m/%Y"), width=150))
#     fecha_validez = style_field(ft.TextField(label="Válido hasta", value=(datetime.date.today() + datetime.timedelta(days=30)).strftime("%d/%m/%Y"), width=150))
#     iva_input = style_field(ft.TextField(label="IVA %", value="21", width=100))

#     # Moneda & cotización
#     moneda_dropdown = ft.Dropdown(label="Moneda", options=[ft.dropdown.Option("ARS"), ft.dropdown.Option("USD")], value="ARS", width=140)
#     cotizacion_input = style_field(ft.TextField(label="Cotización USD (ARS)", value="0", width=140))
#     cotizacion_input.visible = False

#     def moneda_change(e):
#         cotizacion_input.visible = (moneda_dropdown.value == "USD")
#         page.update()

#     moneda_dropdown.on_change = moneda_change

#     # Switches
#     mostrar_logo = ft.Switch(label="Mostrar logo", value=True)
#     mostrar_cuit = ft.Switch(label="Mostrar CUIT/CUIL", value=True)
#     mostrar_dir = ft.Switch(label="Mostrar dirección", value=True)
#     mostrar_correo = ft.Switch(label="Mostrar correo", value=True)

#     # Logo
#     logo_preview = ft.Image(width=120, height=100, fit=ft.ImageFit.CONTAIN)
#     def on_logo_pick(e: ft.FilePickerResultEvent):
#         nonlocal logo_path
#         if e.files:
#             logo_path = e.files[0].path
#             logo_preview.src = f"file://{logo_path}"
#             page.update()
#     fp = ft.FilePicker(on_result=on_logo_pick)
#     page.overlay.append(fp)
#     btn_logo = ft.ElevatedButton("Subir logo", color="white", bgcolor=primary, on_click=lambda _: fp.pick_files(allow_multiple=False))

#     # Ítems
#     tabla = ft.Column(scroll="auto", expand=True)
#     desc_item = style_field(ft.TextField(label="Descripción", width=260))
#     cant_item = style_field(ft.TextField(label="Cantidad", width=80))
#     precio_item = style_field(ft.TextField(label="Precio Unitario (ARS)", width=140))
#     desc_tipo_item = style_field(ft.Dropdown(label="Tipo desc.", options=[ft.dropdown.Option("%"), ft.dropdown.Option("$")], value="$", width=90))
#     desc_val_item = style_field(ft.TextField(label="Valor desc.", value="0", width=90))

#     btn_agregar = ft.ElevatedButton("Agregar", bgcolor=primary, color="white")

#     def render_tabla():
#         tabla.controls.clear()
#         for idx, it in enumerate(items):
#             fila = ft.Row([
#                 ft.Text(it["descripcion"], width=240, overflow=ft.TextOverflow.ELLIPSIS),
#                 ft.Text(str(it["cantidad"]), width=50),
#                 ft.Text(format_currency_ar(it["precio"]), width=120),
#                 ft.Text(f"{it['valor_desc']}{it['tipo_desc']}", width=70),
#                 ft.Text(format_currency_ar(it["subtotal"]), width=100),
#                 ft.IconButton(icon=ft.Icons.EDIT, icon_color=primary, on_click=lambda e, i=idx: editar_item(i)),
#                 ft.IconButton(icon=ft.Icons.DELETE, icon_color="#666", on_click=lambda e, i=idx: eliminar_item(i))
#             ])
#             tabla.controls.append(fila)
#         calcular_totales()
#         page.update()

#     def agregar_o_guardar_item(e):
#         nonlocal edit_index
#         try:
#             desc = desc_item.value.strip()
#             if not desc:
#                 raise ValueError("Descripción vacía")
#             cant = parse_int_tol(cant_item.value)
#             prec = parse_float_tol(precio_item.value)
#             val_desc = parse_float_tol(desc_val_item.value or 0)
#             tipo_desc = desc_tipo_item.value or "$"
#             if tipo_desc == "%":
#                 desc_val_calc = (prec * cant) * (val_desc / 100)
#             else:
#                 desc_val_calc = val_desc
#             subtotal = (prec * cant) - desc_val_calc
#             item = {"descripcion": desc, "cantidad": cant, "precio": prec, "tipo_desc": tipo_desc, "valor_desc": val_desc, "subtotal": subtotal}
#             if edit_index is None:
#                 items.append(item)
#             else:
#                 items[edit_index] = item
#                 edit_index = None
#                 btn_agregar.text = "Agregar"
#             desc_item.value = cant_item.value = precio_item.value = desc_val_item.value = ""
#             render_tabla()
#         except Exception as ex:
#             page.snack_bar = ft.SnackBar(ft.Text(f"⚠️ {ex}"))
#             page.snack_bar.open = True

#     def editar_item(i):
#         nonlocal edit_index
#         edit_index = i
#         it = items[i]
#         desc_item.value, cant_item.value, precio_item.value = it["descripcion"], str(it["cantidad"]), str(it["precio"])
#         desc_tipo_item.value, desc_val_item.value = it["tipo_desc"], str(it["valor_desc"])
#         btn_agregar.text = "Guardar cambios"
#         page.update()

#     def eliminar_item(i):
#         if 0 <= i < len(items):
#             items.pop(i)
#         render_tabla()

#     subtotal_txt, desc_txt, iva_txt, total_txt, equiv_txt = ft.Text(), ft.Text(), ft.Text(), ft.Text(size=18, weight="bold", color=primary), ft.Text()

#     def calcular_totales(e=None):
#         subtotal_general = 0
#         descuento_total = 0
#         try:
#             iva = float(iva_input.value or 0)
#         except:
#             iva = 0
#         for it in items:
#             base = it["precio"] * it["cantidad"]
#             if it["tipo_desc"] == "%":
#                 desc_item_val = base * (it["valor_desc"] / 100)
#             else:
#                 desc_item_val = it["valor_desc"]
#             it["subtotal"] = base - desc_item_val
#             subtotal_general += base
#             descuento_total += desc_item_val
#         iva_total = (subtotal_general - descuento_total) * iva / 100
#         total_general = subtotal_general - descuento_total + iva_total

#         subtotal_txt.value = f"Subtotal: {format_currency_ar(subtotal_general)}"
#         desc_txt.value = f"Descuentos aplicados: -{format_currency_ar(descuento_total)}" if descuento_total else ""
#         iva_txt.value = f"IVA total: {format_currency_ar(iva_total)}" if iva_total else ""
#         total_txt.value = f"TOTAL: {format_currency_ar(total_general)}"

#         # Equivalente en USD (solo si se selecciona USD y la cotización es válida)
#         try:
#             cot = float(cotizacion_input.value) if cotizacion_input.value else 0
#         except:
#             cot = 0
#         if moneda_dropdown.value == "USD" and cot > 0:
#             total_usd = total_general / cot
#             equiv_txt.value = f"Equivalente: {format_currency_usd(total_usd)}  (Cotización: {format_currency_ar(cot)})"
#         else:
#             equiv_txt.value = ""

#         page.update()

#     btn_agregar.on_click = agregar_o_guardar_item
#     iva_input.on_change = calcular_totales

#     def generar_pdf_click(e):
#         if not cliente.value.strip() or not items:
#             page.snack_bar = ft.SnackBar(ft.Text("⚠️ Completar cliente e ítems."))
#             page.snack_bar.open = True
#             return

#         subtotal_general = sum(it["precio"] * it["cantidad"] for it in items)
#         descuento_total = sum(
#             (it["precio"] * it["cantidad"] * it["valor_desc"] / 100 if it["tipo_desc"] == "%" else it["valor_desc"])
#             for it in items
#         )
#         try:
#             iva_val = float(iva_input.value or 0)
#         except:
#             iva_val = 0
#         iva_total = (subtotal_general - descuento_total) * iva_val / 100
#         total_general = subtotal_general - descuento_total + iva_total

#         nro = obtener_proximo_numero()
#         cot = 0.0
#         if moneda_dropdown.value == "USD":
#             try:
#                 cot = float(cotizacion_input.value or 0)
#                 if cot <= 0:
#                     raise ValueError("Cotización inválida")
#             except Exception as ex:
#                 page.snack_bar = ft.SnackBar(ft.Text(f"⚠️ Ingresá una cotización válida para el dólar."))
#                 page.snack_bar.open = True
#                 return

#         archivo = generar_pdf(
#             empresa.value, cuit.value, direccion.value, correo.value, logo_preview.src[7:] if logo_preview.src else None,
#             nro, fecha_emision.value, fecha_validez.value, cliente.value,
#             tipo_id.value, numero_id.value, descripcion.value, items,
#             subtotal_general, descuento_total, iva_val, total_general,
#             mostrar_logo.value, mostrar_cuit.value, mostrar_dir.value, mostrar_correo.value,
#             moneda=moneda_dropdown.value, cotizacion_dolar=cot
#         )
#         webbrowser.open(f"file://{archivo}")
#         page.snack_bar = ft.SnackBar(ft.Text(f"✅ PDF generado: {archivo}"))
#         page.snack_bar.open = True

#     # Tema
#     theme_btn = ft.IconButton(icon=ft.Icons.LIGHT_MODE, tooltip="Cambiar tema")

#     def toggle_tema(e):
#         if page.theme_mode == "light":
#             page.theme_mode = "dark"
#             page.bgcolor = dark_bg
#             theme_btn.icon = ft.Icons.DARK_MODE
#         else:
#             page.theme_mode = "light"
#             page.bgcolor = "#f9f9f9"
#             theme_btn.icon = ft.Icons.LIGHT_MODE
#         for f in [empresa, cuit, direccion, correo, cliente, tipo_id, numero_id,
#                   descripcion, fecha_emision, fecha_validez, iva_input,
#                   desc_item, cant_item, precio_item, desc_val_item, desc_tipo_item]:
#             f.border_color = primary if page.theme_mode == "dark" else None
#         page.update()

#     theme_btn.on_click = toggle_tema

#     contenido = ft.Container(
#         content=ft.Column([
#             ft.Row([ft.Text("Generador de Presupuestos", size=22, weight="bold"),
#                     ft.Container(expand=True), theme_btn]),
#             ft.Divider(),
#             ft.Text("Datos de la empresa", size=16, weight="bold", color=primary),
#             ft.Row([empresa, cuit]), direccion, correo,
#             ft.Row([btn_logo, logo_preview]),
#             ft.Row([mostrar_logo, mostrar_cuit, mostrar_dir, mostrar_correo]),
#             ft.Divider(),
#             ft.Text("Datos del cliente", size=16, weight="bold", color=primary),
#             ft.Row([cliente, tipo_id, numero_id]), descripcion,
#             ft.Row([fecha_emision, fecha_validez, iva_input, moneda_dropdown, cotizacion_input]),
#             ft.Divider(),
#             ft.Text("Ítems del presupuesto", size=16, weight="bold", color=primary),
#             ft.Row([desc_item, cant_item, precio_item, desc_tipo_item, desc_val_item,
#                     ft.ElevatedButton("Agregar", on_click=agregar_o_guardar_item, bgcolor=primary, color="white")]),
#             tabla,
#             ft.Container(ft.Column([subtotal_txt, desc_txt, iva_txt, equiv_txt, ft.Divider(), total_txt],
#                 horizontal_alignment=ft.CrossAxisAlignment.END),
#                 alignment=ft.alignment.center_right, padding=10, border_radius=6, width=420),
#             ft.Divider(),
#             ft.Row([ft.ElevatedButton("Generar y abrir PDF", on_click=generar_pdf_click, bgcolor=primary, color="white"),
#                     ft.Container(expand=True),
#                     ft.ElevatedButton("Limpiar", on_click=lambda e: (items.clear(), render_tabla()), bgcolor="#666", color="white")])
#         ]),
#         border_radius=10,
#         shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color="#333"),
#         padding=20,
#         expand=True,
#         alignment=ft.alignment.center
#     )

#     page.add(contenido)
#     page.bgcolor = "#f9f9f9"


# if __name__ == "__main__":
#     import os
#     port = int(os.environ.get("PORT", 8085))
#     ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0", port=port)



